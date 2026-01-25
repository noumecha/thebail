from rest_framework import serializers
from ..models import FicheCollecte, DocumentCollecte

class DocumentCollecteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCollecte
        exclude = ("fiche",)

class FicheCollecteSerializer(serializers.ModelSerializer):
    documents = DocumentCollecteSerializer(many=True)

    class Meta:
        model = FicheCollecte
        fields = "__all__"
        read_only_fields = ("reference", "created_at", "updated_at")

    def create(self, validated_data):
        documents_data = validated_data.pop("documents")

        fiche = FicheCollecte.objects.create(**validated_data)

        for doc in documents_data:
            DocumentCollecte.objects.create(
                fiche=fiche,
                **doc
            )

        return fiche
