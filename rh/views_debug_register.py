from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from institutions.models import Employe
from agences.models import Agence
from roles_permissions.models import Role
from datetime import date
import traceback
import uuid

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def debug_register_user(request):
    """Version debug simplifiée de l'endpoint register"""
    
    print("\n=== DEBUG REGISTER ENDPOINT START ===")
    print(f"Request method: {request.method}")
    print(f"Request content type: {request.content_type}")
    print(f"Raw request data: {request.data}")
    print("=====================================\n")
    
    try:
        # Récupération des données
        data = request.data
        print(f"DEBUG: Données récupérées: {data}")
        print(f"DEBUG: Type de data: {type(data)}")
        
        # Extraction basique des champs
        agence_id = data.get('agence', '0001')
        nom_complet = data.get('nom', 'TEST USER')
        username = data.get('username', f'debug_{uuid.uuid4().hex[:8]}')
        telephone = data.get('telephone', f'077{uuid.uuid4().hex[:7]}')
        email = data.get('email', f'debug_{uuid.uuid4().hex[:8]}@test.com')
        password = data.get('password', '1234')
        fonction_id = data.get('fonction', 1)
        
        print(f"DEBUG: Champs extraits:")
        print(f"  agence_id: {agence_id}")
        print(f"  nom_complet: {nom_complet}")
        print(f"  username: {username}")
        print(f"  email: {email}")
        print(f"  fonction_id: {fonction_id}")
        
        # Récupération des objets de référence
        print(f"DEBUG: Récupération agence...")
        try:
            agence = Agence.objects.get(id=agence_id)
            print(f"DEBUG: Agence trouvée: {agence.nom}")
        except Exception as e:
            print(f"DEBUG: Erreur agence: {e}")
            return Response({
                'error': 'Agence non trouvée',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"DEBUG: Récupération rôle...")
        try:
            role = Role.objects.get(id=int(fonction_id))
            print(f"DEBUG: Rôle trouvé: {role.nom_role}")
        except Exception as e:
            print(f"DEBUG: Erreur rôle: {e}")
            return Response({
                'error': 'Rôle non trouvé',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Création dans une transaction
        print(f"DEBUG: Début transaction...")
        with transaction.atomic():
            # Création User
            print(f"DEBUG: Création User...")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"DEBUG: User créé: {user.username}")
            
            # Création Employé
            print(f"DEBUG: Création Employé...")
            matricule = f"DBG{uuid.uuid4().hex[:6].upper()}"
            print(f"DEBUG: Matricule: {matricule}")
            
            employe = Employe.objects.create(
                user=user,
                nom='DEBUG',
                prenom='USER',
                email=email,
                telephone=telephone,
                agence=agence,
                role=role,
                matricule_interne=matricule,
                sexe='M',
                date_naissance=date(1990, 1, 1),
                lieu_naissance='Debug',
                nationalite='Ivoirienne',
                situation_familiale='celibataire',
                adresse='Debug adresse',
                numero_cni='Debug CNI',
                date_embauche=date.today(),
                type_contrat='CDI',
                horaire_travail='08h00-17h00',
                salaire_base=0.00,
                rib_banque='Debug RIB',
                statut='actif'
            )
            print(f"DEBUG: Employé créé: ID={employe.id}")
        
        print(f"DEBUG: Transaction terminée avec succès")
        
        return Response({
            'message': 'Debug: Compte créé avec succès',
            'user_id': user.id,
            'employe_id': employe.id,
            'matricule': employe.matricule_interne
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"DEBUG: ERREUR CAPTURÉE: {type(e).__name__}: {str(e)}")
        print(f"DEBUG: Traceback:")
        print(traceback.format_exc())
        
        return Response({
            'error': 'Erreur lors de la création du compte (debug)',
            'error_type': type(e).__name__,
            'error_message': str(e),
            'traceback': traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
