from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Appointment, Professional
from .serializers import AppointmentSerializer, ProfessionalSerializer


def home(request):
    return render(request, "home.html")


class ProfessionalListCreateView(generics.ListCreateAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


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
        professional_id = self.kwargs.get("professional_id")
        return Appointment.objects.filter(profissional_id=professional_id).select_related("profissional")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Nenhuma consulta encontrada para este profissional."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
