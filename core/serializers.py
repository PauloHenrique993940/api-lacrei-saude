import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import Appointment, Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({field: "Campo não permitido." for field in sorted(unknown)})
        return attrs

    def validate_nome_social(self, value):
        return self._validate_text(value, "nome social", 2)

    def validate_profissao(self, value):
        return self._validate_text(value, "profissão", 2)

    def validate_endereco(self, value):
        return self._validate_text(value, "endereço", 5)

    def validate_contato(self, value):
        value = value.strip()
        phone = re.sub(r"\D", "", value)
        if re.fullmatch(r"(?:\+?55)?\d{10,11}", phone):
            return value
        try:
            EmailValidator()(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Informe um telefone válido ou e-mail válido.")
        return value

    @staticmethod
    def _validate_text(value, field_name, minimum_length):
        normalized = value.strip()
        if len(normalized) < minimum_length or any(ord(char) < 32 for char in normalized):
            raise serializers.ValidationError(f"O campo {field_name} contém texto inválido.")
        return normalized

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

    def validate(self, attrs):
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({field: "Campo não permitido." for field in sorted(unknown)})
        return attrs

    class Meta:
        model = Appointment
        fields = ["id", "data", "profissional", "created_at", "updated_at"]

    def validate_data(self, value):
        if value is None:
            raise serializers.ValidationError("A data da consulta é obrigatória.")
        if value.year < 2000:
            raise serializers.ValidationError("Informe uma data válida.")
        return value

    def validate_profissional(self, value):
        if value is None:
            raise serializers.ValidationError("O profissional vinculado é obrigatório.")
        return value
