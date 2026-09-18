from django.db.models import ProtectedError
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Appointment, Professional


class ProfessionalAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.defaults["HTTP_X_API_KEY"] = settings.API_KEY
        self.professional = Professional.objects.create(
            nome_social="Dr. Ana",
            profissao="Psiquiatra",
            endereco="Rua das Flores, 123",
            contato="(11) 99999-0000",
        )

    def test_list_professionals(self):
        response = self.client.get(reverse("professional-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_create_professional(self):
        payload = {
            "nome_social": "Dr. Bruno",
            "profissao": "Cardiologista",
            "endereco": "Av. Paulista, 456",
            "contato": "(11) 98888-1111",
        }
        response = self.client.post(reverse("professional-list-create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 2)

    def test_update_professional(self):
        response = self.client.patch(
            reverse("professional-detail", args=[self.professional.id]),
            {"profissao": "Neurologista"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.profissao, "Neurologista")

    def test_delete_professional(self):
        response = self.client.delete(reverse("professional-detail", args=[self.professional.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Professional.objects.filter(id=self.professional.id).exists())

    def test_professional_missing_fields(self):
        response = self.client.post(
            reverse("professional-list-create"),
            {"nome_social": "Sem profissão"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_professional_and_request_id(self):
        response = self.client.get(reverse("professional-detail", args=[self.professional.id]), HTTP_X_REQUEST_ID="test-request")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.professional.id)
        self.assertEqual(response["X-Request-ID"], "test-request")

    def test_filters_and_unknown_fields(self):
        response = self.client.get(reverse("professional-list-create"), {"profissao": "Psiquiatra", "q": "Ana OR 1=1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])
        response = self.client.post(
            reverse("professional-list-create"),
            {"nome_social": "Dr. Bia", "profissao": "Clínica", "endereco": "Rua B, 10", "contato": "bia@example.com", "extra": "ignored"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cors_header_and_health_check(self):
        response = self.client.get(reverse("health"), HTTP_ORIGIN="http://localhost:3000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:3000")


class AppointmentAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.defaults["HTTP_X_API_KEY"] = settings.API_KEY
        self.professional = Professional.objects.create(
            nome_social="Dra. Carla",
            profissao="Endocrinologista",
            endereco="Rua B, 22",
            contato="(21) 97777-2222",
        )
        self.appointment = Appointment.objects.create(
            data="2026-10-15T10:00:00Z",
            profissional=self.professional,
        )

    def test_list_appointments(self):
        response = self.client.get(reverse("appointment-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_create_appointment(self):
        payload = {"data": "2026-10-16T09:30:00Z", "profissional": self.professional.id}
        response = self.client.post(reverse("appointment-list-create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_update_appointment(self):
        response = self.client.patch(
            reverse("appointment-detail", args=[self.appointment.id]),
            {"data": "2026-10-20T12:00:00Z"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.data.isoformat(), "2026-10-20T12:00:00+00:00")

    def test_delete_appointment(self):
        response = self.client.delete(reverse("appointment-detail", args=[self.appointment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())

    def test_get_appointments_by_professional(self):
        response = self.client.get(reverse("appointment-by-professional", args=[self.professional.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_appointment_missing_fields(self):
        response = self.client.post(reverse("appointment-list-create"), {"profissional": self.professional.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_appointment_with_unknown_professional(self):
        response = self.client.post(
            reverse("appointment-list-create"),
            {"data": "2026-10-16T09:30:00Z", "profissional": 99999},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_appointment_and_filter_by_date(self):
        response = self.client.get(reverse("appointment-detail", args=[self.appointment.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            reverse("appointment-by-professional", args=[self.professional.id]),
            {"data": "2026-10-15"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_professional_delete_protects_appointment_history(self):
        with self.assertRaises(ProtectedError):
            self.professional.delete()
        self.assertTrue(Appointment.objects.filter(id=self.appointment.id).exists())

    def test_invalid_api_key(self):
        client = APIClient()
        response = client.get(reverse("professional-list-create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
