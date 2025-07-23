from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db import transaction
from institutions.models import Employe
from agences.models import Agence
from roles_permissions.models import Role
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.utils import timezone
from datetime import date

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not username or not password or username.strip() == '' or password.strip() == '':
            raise serializers.ValidationError('Nom d’utilisateur et mot de passe obligatoires.')
        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# =============================================
# Fonctions utilitaires pour l'enregistrement
# =============================================

def validate_username(username):
    """Valide le format du nom d'utilisateur"""
    if not username or len(username) < 3 or len(username) > 30:
        return False
    # Autoriser lettres, chiffres, points, tirets et underscores
    pattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, username))

def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_telephone(telephone):
    """Valide le format du téléphone (8-15 chiffres)"""
    pattern = r'^[0-9]{8,15}$'
    return bool(re.match(pattern, telephone.replace(' ', '').replace('-', '')))

def validate_nom_complet(nom):
    """Valide que le nom contient au moins prénom et nom"""
    if not nom or len(nom.strip()) < 3:
        return False
    mots = nom.strip().split()
    return len(mots) >= 2

def generate_username_suggestions(base_username, max_suggestions=5):
    """Génère des suggestions de nom d'utilisateur si celui demandé est pris"""
    suggestions = []
    
    # Suggestion 1: Ajouter des numéros
    for i in range(1, max_suggestions + 1):
        suggestion = f"{base_username}{i}"
        if not User.objects.filter(username=suggestion).exists():
            suggestions.append(suggestion)
            if len(suggestions) >= max_suggestions:
                break
    
    # Suggestion 2: Ajouter des points ou underscores
    if len(suggestions) < max_suggestions:
        alternatives = [
            base_username.replace('.', '_'),
            base_username.replace('_', '.'),
            f"{base_username}_user",
            f"user_{base_username}"
        ]
        
        for alt in alternatives:
            if not User.objects.filter(username=alt).exists() and alt not in suggestions:
                suggestions.append(alt)
                if len(suggestions) >= max_suggestions:
                    break
    
    return suggestions[:max_suggestions]

def generate_matricule():
    """Génère un matricule unique pour l'employé"""
    year = timezone.now().year
    # Compter les employés créés cette année
    count = Employe.objects.filter(date_creation__year=year).count() + 1
    return f"EMP{year}{str(count).zfill(4)}"


# =============================================
# Endpoints d'enregistrement
# =============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def check_username_availability(request):
    """Vérifie la disponibilité d'un nom d'utilisateur et propose des alternatives"""
    username = request.data.get('username', '').strip().lower()
    
    if not username:
        return Response({
            'error': 'Nom d\'utilisateur requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not validate_username(username):
        return Response({
            'error': 'Format de nom d\'utilisateur invalide (3-30 caractères, lettres, chiffres, ., -, _ autorisés)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    is_available = not User.objects.filter(username=username).exists()
    
    response_data = {
        'username': username,
        'available': is_available
    }
    
    if not is_available:
        suggestions = generate_username_suggestions(username)
        response_data['suggestions'] = suggestions
        response_data['message'] = 'Ce nom d\'utilisateur est déjà pris. Voici quelques suggestions :'
    else:
        response_data['message'] = 'Nom d\'utilisateur disponible'
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Enregistre un nouvel utilisateur et crée automatiquement son profil employé"""
    try:
        # Récupération des données
        data = request.data
        agence_id = data.get('agence')
        nom_complet = data.get('nom', '').strip()
        username = data.get('username', '').strip().lower()
        telephone = data.get('telephone', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        fonction_id = data.get('fonction')
        
        # Validation des champs requis
        errors = {}
        
        if not agence_id:
            errors['agence'] = 'Veuillez sélectionner une agence'
        else:
            try:
                agence = Agence.objects.get(id=agence_id)
            except Agence.DoesNotExist:
                errors['agence'] = 'Agence sélectionnée invalide'
        
        if not nom_complet or not validate_nom_complet(nom_complet):
            errors['nom'] = 'Veuillez entrer votre nom et prénom (au moins 2 mots)'
        
        if not username or not validate_username(username):
            errors['username'] = 'Format de nom d\'utilisateur invalide (3-30 caractères, lettres, chiffres, ., -, _ autorisés)'
        elif User.objects.filter(username=username).exists():
            suggestions = generate_username_suggestions(username)
            errors['username'] = f'Ce nom d\'utilisateur est déjà pris. Suggestions: {", ".join(suggestions[:3])}'
        
        if not telephone or not validate_telephone(telephone):
            errors['telephone'] = 'Format de téléphone invalide (8-15 chiffres)'
        elif Employe.objects.filter(telephone=telephone).exists():
            errors['telephone'] = 'Ce numéro de téléphone est déjà utilisé'
        
        if not email or not validate_email(email):
            errors['email'] = 'Format d\'email invalide'
        elif User.objects.filter(email=email).exists() or Employe.objects.filter(email=email).exists():
            errors['email'] = 'Cette adresse email est déjà utilisée'
        
        if not password or len(password) < 8:
            errors['password'] = 'Le mot de passe doit contenir au moins 8 caractères'
        elif not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password):
            errors['password'] = 'Le mot de passe doit contenir au moins une majuscule, une minuscule et un chiffre'
        
        if password != confirm_password:
            errors['confirmPassword'] = 'Les mots de passe ne correspondent pas'
        
        if not fonction_id:
            errors['fonction'] = 'Veuillez sélectionner une fonction'
        else:
            try:
                role = Role.objects.get(id=fonction_id)
            except Role.DoesNotExist:
                errors['fonction'] = 'Fonction sélectionnée invalide'
        
        if errors:
            return Response({
                'error': 'Données invalides',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Création de l'utilisateur et de l'employé dans une transaction
        with transaction.atomic():
            # Création du User Django
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nom_complet.split()[0],
                last_name=' '.join(nom_complet.split()[1:]) if len(nom_complet.split()) > 1 else ''
            )
            
            # Séparation du nom complet
            nom_parts = nom_complet.split()
            prenom = nom_parts[0]
            nom_famille = ' '.join(nom_parts[1:]) if len(nom_parts) > 1 else prenom
            
            # Création de l'Employé
            employe = Employe.objects.create(
                user=user,
                nom=nom_famille,
                prenom=prenom,
                email=email,
                telephone=telephone,
                agence=agence,
                role=role,
                matricule_interne=generate_matricule(),
                # Valeurs par défaut pour les champs obligatoires
                sexe='M',  # À compléter par le DRH
                date_naissance=date(1990, 1, 1),  # À compléter par le DRH
                lieu_naissance='À compléter',  # À compléter par le DRH
                nationalite='À compléter',  # À compléter par le DRH
                situation_familiale='celibataire',  # À compléter par le DRH
                adresse='À compléter',  # À compléter par le DRH
                numero_cni='À compléter',  # À compléter par le DRH
                date_embauche=date.today(),
                type_contrat='CDI',  # À compléter par le DRH
                horaire_travail='08h00-17h00',  # À compléter par le DRH
                salaire_base=0,  # À compléter par le DRH
                rib_banque='À compléter',  # À compléter par le DRH
                statut='actif'
            )
            
            # Génération du token JWT pour connexion automatique
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                'message': 'Compte créé avec succès',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nom_complet': nom_complet
                },
                'employe': {
                    'id': employe.id,
                    'matricule': employe.matricule_interne,
                    'agence': agence.nom,
                    'fonction': role.nom
                },
                'tokens': {
                    'access': access_token,
                    'refresh': refresh_token
                },
                'info': 'Votre compte a été créé. Le DRH complètera vos informations personnelles ultérieurement.'
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            'error': 'Erreur lors de la création du compte',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
