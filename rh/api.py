from rest_framework import serializers, viewsets, permissions, authentication, routers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Pointage
from .serializers import PointageSerializer, AgenceSerializer, RoleSerializer
from agences.models import Agence
from roles_permissions.models import Role
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import path
from .api_reporting import ReportingRHAPIView
from institutions.models import Employe

class RoleBasedPointagePermission(BasePermission):
    """
    Permission personnalisée pour filtrer l'accès aux pointages selon le rôle utilisateur.
    """
    def has_permission(self, request, view):
        # Authentification déjà vérifiée par TokenAuthentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin : accès total
        # Agent RH : accès aux employés de son périmètre (à adapter)
        # Employé : accès à ses propres pointages
        try:
            employe = Employe.objects.get(user=request.user)
            role_name = employe.role.nom_role.lower()
        except Employe.DoesNotExist:
            return False
        if role_name == 'administrateur' or request.user.is_superuser:
            return True
        elif role_name == 'agent rh':
            # À adapter selon la logique de périmètre RH
            return True  # Pour l'instant, accès à tout (à restreindre si besoin)
        elif role_name == 'employé':
            return obj.employe.user == request.user
        return False

class PointageViewSet(viewsets.ModelViewSet):

    from rest_framework.permissions import IsAuthenticated

    @action(detail=False, methods=['get'], url_path='employe/me', permission_classes=[IsAuthenticated])
    def employe_me(self, request):
        """
        Renvoie les infos de l'employé connecté (id, nom, prenom, agence, email).
        """
        print("DEBUG HEADERS:", dict(request.headers))
        print("DEBUG USER:", request.user)
        print("DEBUG IS_AUTHENTICATED:", request.user.is_authenticated)
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Non authentifié.'}, status=401)
        try:
            employe = Employe.objects.get(email=user.email)
            data = {
                'id': employe.id,
                'nom': employe.nom,
                'prenom': employe.prenom,
                'agence_id': employe.agence.id if employe.agence else None,
                'agence_nom': employe.agence.nom if employe.agence else None,
                'email': employe.email,
            }
            return Response(data)
        except Employe.DoesNotExist:
            return Response({'detail': 'Employé non trouvé.'}, status=404)

    serializer_class = PointageSerializer
    from rest_framework_simplejwt.authentication import JWTAuthentication
    authentication_classes = [JWTAuthentication]
    permission_classes = [RoleBasedPointagePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employe', 'date', 'type', 'source']

    def _create_pointage_with_validation(self, employe, agence, date_pointage, type_pointage, heure=None, source='automatique', commentaire=None):
        from django.utils import timezone
        import logging
        logger = logging.getLogger('pointage_debug')

        # Forcer la date du pointage à la date du serveur (timezone locale)
        current_date = timezone.localdate()
        date_pointage = current_date
        logger.debug(f"[PointageDebug] Employé: {employe.id} | Agence: {agence.id if agence else None} | Date forcée (serveur): {date_pointage} | Type: {type_pointage}")

        # Chercher un pointage existant pour aujourd'hui
        existing_pointages = Pointage.objects.filter(
            employe=employe,
            agence=agence,
            date=date_pointage,
            type=type_pointage
        )
        logger.debug(f"[PointageDebug] Pointages existants trouvés: {list(existing_pointages.values('id', 'date', 'heure', 'type', 'agence_id'))}")

        if employe.agence != agence:
            raise serializers.ValidationError("Vous ne pouvez pointer que dans votre agence d'affectation.")
        if existing_pointages.exists():
            p = existing_pointages.first()
            raise serializers.ValidationError(
                f"Vous avez déjà effectué un pointage '{type_pointage}' le {p.date} à {p.heure} dans cette agence.")
        return Pointage.objects.create(
            employe=employe,
            agence=agence,
            date=date_pointage,
            heure=heure,
            type=type_pointage,
            source=source,
            commentaire=commentaire
        )

    def perform_create(self, serializer):
        user = self.request.user
        try:
            employe = Employe.objects.get(user=user)
        except Employe.DoesNotExist:
            raise serializers.ValidationError("Employé introuvable pour cet utilisateur.")
        agence = serializer.validated_data['agence']
        type_pointage = serializer.validated_data['type']
        date_pointage = serializer.validated_data['date']
        heure = serializer.validated_data.get('heure')
        # Utilise la méthode factorisée pour la validation et la création
        self._create_pointage_with_validation(
            employe=employe,
            agence=agence,
            date_pointage=date_pointage,
            type_pointage=type_pointage,
            heure=heure,
            source='automatique',
            commentaire=serializer.validated_data.get('commentaire')
        )
        serializer.save(employe=employe)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Pointage.objects.none()
        try:
            employe = Employe.objects.get(user=user)
            role_name = employe.role.nom_role.lower()
        except Employe.DoesNotExist:
            return Pointage.objects.none()
        if role_name == 'administrateur' or user.is_superuser:
            return Pointage.objects.all().order_by('-date', '-heure')
        elif role_name == 'agent rh':
            # TODO : filtrer selon le périmètre RH (ex : agence/établissement)
            return Pointage.objects.all().order_by('-date', '-heure')
        elif role_name == 'employé':
            return Pointage.objects.filter(employe=employe).order_by('-date', '-heure')
        return Pointage.objects.none()

    @action(detail=False, methods=['post'], url_path='scan_qr_code')
    def scan_qr_code(self, request):
        """
        Endpoint POST pour création de pointage via scan QR code.
        Attend : employe_id, type (arrivee/depart), site_identifier (optionnel)
        """
        employe_id = request.data.get('employe_id')
        type_pointage = request.data.get('type')
        agence_id = request.data.get('agence_id')
        site_identifier = request.data.get('site_identifier')
        date_str = request.data.get('date')
        heure_str = request.data.get('heure')
        if not employe_id or not type_pointage or not agence_id:
            return Response({'detail': 'employe_id, agence_id et type sont requis.'}, status=400)
        try:
            employe = Employe.objects.get(id=employe_id)
            agence = Agence.objects.get(id=agence_id)
            # Gestion de la date/heure (auto si non fourni)
            from django.utils import timezone
            from datetime import datetime
            if date_str:
                date_pointage = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_pointage = timezone.localdate()
            if heure_str:
                heure_pointage = datetime.strptime(heure_str, "%H:%M:%S").time()
            else:
                heure_pointage = timezone.localtime().time()
            # Validation stricte via la méthode centrale
            pointage = self._create_pointage_with_validation(
                employe=employe,
                agence=agence,
                date_pointage=date_pointage,
                type_pointage=type_pointage,
                heure=heure_pointage,
                source='qr',
            )
            serializer = self.get_serializer(pointage)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

    @action(detail=False, methods=['post'], url_path='geolocate')
    def geolocate(self, request):
        """
        Endpoint POST pour création de pointage via géolocalisation.
        Attend : employe_id, type, latitude, longitude
        """
        employe_id = request.data.get('employe_id')
        type_pointage = request.data.get('type')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if not employe_id or not type_pointage or not latitude or not longitude:
            return Response({'detail': 'employe_id, type, latitude et longitude sont requis.'}, status=400)
        try:
            employe = Employe.objects.get(id=employe_id)
        except Employe.DoesNotExist:
            return Response({'detail': 'Employé introuvable.'}, status=404)
        # TODO : Ajouter la logique de vérification de la zone géographique autorisée
        pointage = Pointage.objects.create(
            employe=employe,
            date=request.data.get('date') or None,
            heure=request.data.get('heure') or None,
            type=type_pointage,
            commentaire=f'Pointage géolocalisé ({latitude}, {longitude})'
        )
        return Response(PointageSerializer(pointage).data, status=201)

# ViewSets pour les données de référence mobile
class AgenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les agences - utilisé par l'app mobile pour les listes déroulantes
    """
    serializer_class = AgenceSerializer
    
    def get_queryset(self):
        # Retourner seulement les agences actives
        return Agence.objects.filter(statut='active').order_by('nom')

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les rôles/fonctions - utilisé par l'app mobile pour les listes déroulantes
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by('nom_role')

urlpatterns = [
    path('reporting/', ReportingRHAPIView.as_view(), name='api_reporting_rh'),
]
