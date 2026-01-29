from rest_framework import serializers
from ..models import Collectes

class FicheCollecteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collectes
        fields = "__all__"
        read_only_fields = ("reference", "created_at", "updated_at")

    def create(self, validated_data):
        documents_data = validated_data.pop("documents")

        fiche = Collectes.objects.create(**validated_data)

        for doc in documents_data:
            Collectes.objects.create(
                fiche=fiche,
                **doc
            )

        return fiche
