from django.db import models


class Professional(models.Model):
    nome_social = models.CharField(max_length=150)
    profissao = models.CharField(max_length=120)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.nome_social


class Appointment(models.Model):
    data = models.DateTimeField()
    profissional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="consultas",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["data"]

    def __str__(self):
        return f"Consulta em {self.data} - {self.profissional.nome_social}"
