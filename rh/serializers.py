from rest_framework import serializers
from agences.models import Agence
from roles_permissions.models import Role
from .models import Pointage

class PointageSerializer(serializers.ModelSerializer):
    """Serializer pour les pointages"""
    class Meta:
        model = Pointage
        fields = ['id', 'employe', 'agence', 'date', 'heure', 'type', 'source', 'commentaire', 'created_at']

class AgenceSerializer(serializers.ModelSerializer):
    """Serializer pour les agences - utilisé pour les listes déroulantes mobile"""
    class Meta:
        model = Agence
        fields = ['id', 'nom', 'statut']
        
    def to_representation(self, instance):
        """Format personnalisé pour les dropdowns mobile"""
        return {
            'label': instance.nom,
            'value': instance.id,
            'statut': instance.statut
        }

class RoleSerializer(serializers.ModelSerializer):
    """Serializer pour les rôles/fonctions - utilisé pour les listes déroulantes mobile"""
    class Meta:
        model = Role
        fields = ['id', 'nom_role']
        
    def to_representation(self, instance):
        """Format personnalisé pour les dropdowns mobile"""
        return {
            'label': instance.nom_role,
            'value': instance.id
        }
