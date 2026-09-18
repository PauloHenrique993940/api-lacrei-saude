from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Appointment, Professional
from .serializers import AppointmentSerializer, ProfessionalSerializer


def home(request):
    return render(request, "home.html")


def health(request):
    connection.ensure_connection()
    return JsonResponse({"status": "ok", "database": "ok"})


class ProfessionalListCreateView(generics.ListCreateAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        profession = self.request.query_params.get("profissao")
        search = self.request.query_params.get("q")
        if profession:
            queryset = queryset.filter(profissao__iexact=profession.strip())
        if search:
            queryset = queryset.filter(nome_social__icontains=search.strip())
        return queryset


class ProfessionalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.select_related("profissional").all()
    serializer_class = AppointmentSerializer


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.select_related("profissional").all()
    serializer_class = AppointmentSerializer


class AppointmentByProfessionalView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.filter(profissional_id=self.kwargs.get("professional_id")).select_related("profissional")
        date = self.request.query_params.get("data")
        if date:
            queryset = queryset.filter(data__date=date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Nenhuma consulta encontrada para este profissional."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
