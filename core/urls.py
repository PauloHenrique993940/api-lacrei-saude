from django.urls import path

from .views import (
    AppointmentByProfessionalView,
    AppointmentDetailView,
    AppointmentListCreateView,
    ProfessionalDetailView,
    ProfessionalListCreateView,
)

urlpatterns = [
    path("professionals/", ProfessionalListCreateView.as_view(), name="professional-list-create"),
    path("professionals/<int:pk>/", ProfessionalDetailView.as_view(), name="professional-detail"),
    path("appointments/", AppointmentListCreateView.as_view(), name="appointment-list-create"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("professionals/<int:professional_id>/appointments/", AppointmentByProfessionalView.as_view(), name="appointment-by-professional"),
]
