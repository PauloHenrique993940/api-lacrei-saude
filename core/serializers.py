from rest_framework import serializers

from .models import Appointment, Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = [
            "id",
            "nome_social",
            "profissao",
            "endereco",
            "contato",
            "created_at",
            "updated_at",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    profissional = serializers.PrimaryKeyRelatedField(queryset=Professional.objects.all())

    class Meta:
        model = Appointment
        fields = ["id", "data", "profissional", "created_at", "updated_at"]

    def validate_data(self, value):
        if value is None:
            raise serializers.ValidationError("A data da consulta é obrigatória.")
        return value

    def validate_profissional(self, value):
        if value is None:
            raise serializers.ValidationError("O profissional vinculado é obrigatório.")
        return value
