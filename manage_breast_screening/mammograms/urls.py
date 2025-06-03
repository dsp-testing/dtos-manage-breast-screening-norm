from django.urls import path

from . import views

app_name = "mammograms"

urlpatterns = [
    path(
        "<uuid:id>/check-in/",
        views.check_in,
        name="check_in",
    ),
    path(
        "<uuid:id>/start-screening/",
        views.StartScreening.as_view(),
        name="start_screening",
    ),
    path(
        "<uuid:id>/ask-for-medical-information/",
        views.AskForMedicalInformation.as_view(),
        name="ask_for_medical_information",
    ),
    path(
        "<uuid:id>/record-medical-information/",
        views.RecordMedicalInformation.as_view(),
        name="record_medical_information",
    ),
    path(
        "<uuid:id>/awaiting-images/",
        views.awaiting_images,
        name="awaiting_images",
    ),
    path(
        "<uuid:id>/cannot-go-ahead/",
        views.appointment_cannot_go_ahead,
        name="appointment_cannot_go_ahead",
    ),
]
