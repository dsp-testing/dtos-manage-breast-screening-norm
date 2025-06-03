from datetime import date

from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from manage_breast_screening.clinics.tests.factories import ClinicSlotFactory

from .. import models


class ParticipantFactory(DjangoModelFactory):
    class Meta:
        model = models.Participant

    first_name = "Janet"
    last_name = "Williams"
    gender = "Female"
    nhs_number = "07700900829"
    phone = "07700900829"
    email = "janet.williams@example.com"
    date_of_birth = date(1959, 7, 22)
    ethnic_group = FuzzyChoice(
        models.Participant.ETHNIC_GROUP_CHOICES, getter=lambda c: c[0]
    )
    risk_level = "Routine"
    extra_needs = []


class ParticipantAddressFactory(DjangoModelFactory):
    lines = ["123 Generic Street", "Townsville"]
    postcode = "SW1A 1AA"
    participant = SubFactory(ParticipantFactory)

    class Meta:
        model = models.ParticipantAddress


class ScreeningEpisodeFactory(DjangoModelFactory):
    class Meta:
        model = models.ScreeningEpisode

    participant = SubFactory(ParticipantFactory)


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = models.Appointment

    clinic_slot = SubFactory(ClinicSlotFactory)
    screening_episode = SubFactory(ScreeningEpisodeFactory)
