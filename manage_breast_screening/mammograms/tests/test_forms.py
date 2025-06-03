import pytest
from pytest_django.asserts import assertFormError

from manage_breast_screening.participants.tests.factories import AppointmentFactory

from ..forms import AppointmentCannotGoAheadForm, ScreeningAppointmentForm


class TestScreeningAppointmentForm:
    def test_decision_cannot_be_left_blank(self):
        form = ScreeningAppointmentForm({})
        assertFormError(form, "decision", ["This field is required."])


@pytest.mark.django_db
class TestAppointmentCannotGoAheadForm:
    @pytest.mark.parametrize(
        "decision,reinvite_value", [("True", True), ("False", False)]
    )
    def test_reinvite_reflects_form_data(self, decision, reinvite_value):
        appointment = AppointmentFactory()
        assert appointment.reinvite == False

        form_data = {
            "stopped_reasons": ["failed_identity_check"],
            "decision": decision,
        }
        form = AppointmentCannotGoAheadForm(form_data, instance=appointment)
        form.is_valid()
        form.save()
        appointment.refresh_from_db()
        assert appointment.reinvite == reinvite_value
