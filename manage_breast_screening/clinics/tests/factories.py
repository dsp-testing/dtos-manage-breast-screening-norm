import datetime

from factory.declarations import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from manage_breast_screening.clinics import models


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = models.Provider
        django_get_or_create = ("name",)

    name = Sequence(lambda n: "provider %d" % n)


class SettingFactory(DjangoModelFactory):
    class Meta:
        model = models.Setting
        django_get_or_create = ("name",)

    name = Sequence(lambda n: "setting %d" % n)
    provider = SubFactory(ProviderFactory)


class ClinicFactory(DjangoModelFactory):
    class Meta:
        model = models.Clinic
        django_get_or_create = ("starts_at", "ends_at")

    type = FuzzyChoice(models.Clinic.TYPE_CHOICES)
    risk_type = FuzzyChoice(models.Clinic.RISK_TYPE_CHOICES)
    state = models.Clinic.State.SCHEDULED
    starts_at = Sequence(
        lambda n: datetime.datetime(2025, 1, 1, 9) + datetime.timedelta(hours=n)
    )
    ends_at = LazyAttribute(lambda o: o.starts_at + datetime.timedelta(minutes=30))
    setting = SubFactory(SettingFactory)


class ClinicSlotFactory(DjangoModelFactory):
    class Meta:
        model = models.ClinicSlot

    clinic = SubFactory(ClinicFactory)
    starts_at = Sequence(
        lambda n: datetime.datetime(2025, 1, 1, 9) + datetime.timedelta(hours=n)
    )
    duration_in_minutes = 15
