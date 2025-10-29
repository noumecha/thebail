from rest_framework import serializers
from .models import Utilisateur, RoleUtilisateur

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUtilisateur
        fields = ['id', 'nom']