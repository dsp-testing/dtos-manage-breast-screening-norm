from datetime import datetime, timezone
from unittest.mock import MagicMock
import uuid

import pytest
from django.urls import reverse

from manage_breast_screening.clinics.presenters import (
    ClinicPresenter,
    AppointmentListPresenter,
)

from manage_breast_screening.clinics.tests.factories import (
    ClinicFactory,
    ClinicSlotFactory,
)
from manage_breast_screening.core.utils.date_formatting import format_time
from manage_breast_screening.participants.tests.factories import AppointmentFactory

from ..models import Clinic


@pytest.fixture
def mock_clinic():
    mock = MagicMock(spec=Clinic)

    mock.starts_at = datetime(2025, 1, 1, 9)
    mock.session_type.return_value = "All day"
    mock.clinic_slots.count.return_value = 10
    mock.setting.name = "Test setting"
    mock.time_range.return_value = {
        "start_time": datetime(2025, 1, 1, 9),
        "end_time": datetime(2025, 1, 1, 15),
    }
    mock.get_type_display.return_value = "Screening"
    mock.get_risk_type_display.return_value = "Routine"

    return mock


def test_clinic_presenter(mock_clinic):
    presenter = ClinicPresenter(mock_clinic)

    assert presenter.starts_at == "1 January 2025"
    assert presenter.session_type == "All day"
    assert presenter.number_of_slots == 10
    assert presenter.location_name == "Test setting"
    assert presenter.time_range == "9am to 3pm"
    assert presenter.type == "Screening"
    assert presenter.risk_type == "Routine"


class TestAppointmentListPresenter:
    @pytest.mark.django_db
    def test_sorts_by_start_time(self):
        clinic = ClinicFactory()
        appointment1 = AppointmentFactory(
            clinic_slot=ClinicSlotFactory(
                clinic=clinic,
                starts_at=datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc),  # 1pm
            )
        )
        appointment2 = AppointmentFactory(
            clinic_slot=ClinicSlotFactory(
                clinic=clinic,
                starts_at=datetime(2025, 1, 1, 9, 0, tzinfo=timezone.utc),  # 9am
            )
        )
        appointment3 = AppointmentFactory(
            clinic_slot=ClinicSlotFactory(
                clinic=clinic,
                starts_at=datetime(2025, 1, 1, 11, 30, tzinfo=timezone.utc),  # 11:30am
            )
        )

        presenter = AppointmentListPresenter(
            clinic.id, [appointment1, appointment2, appointment3], "all", {}
        )

        sorted_times = [
            appointment.clinic_slot.starts_at for appointment in presenter.appointments
        ]

        assert sorted_times == [
            format_time(datetime(2025, 1, 1, 9, 0, tzinfo=timezone.utc)),  # 9am
            format_time(datetime(2025, 1, 1, 11, 30, tzinfo=timezone.utc)),  # 11:30am
            format_time(datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)),  # 1pm
        ]

    @pytest.mark.django_db
    def test_secondary_nav_data(self):
        clinic_id = uuid.uuid4()
        filter_value = "checked_in"
        counts_by_filter = {"remaining": 5, "checked_in": 3, "complete": 2, "all": 10}

        presenter = AppointmentListPresenter(
            clinic_id, [], filter_value, counts_by_filter
        )
        nav_data = presenter.secondary_nav_data

        assert nav_data[0]["label"] == "Remaining"
        assert nav_data[0]["count"] == 5
        expected_remaining_url = reverse(
            "clinics:show_remaining", kwargs={"id": clinic_id, "filter": "remaining"}
        )
        assert nav_data[0]["href"] == expected_remaining_url
        assert not nav_data[0]["current"]

        assert nav_data[1]["label"] == "Checked in"
        assert nav_data[1]["count"] == 3
        expected_checked_in_url = reverse(
            "clinics:show_checked_in", kwargs={"id": clinic_id, "filter": "checked_in"}
        )
        assert nav_data[1]["href"] == expected_checked_in_url
        assert nav_data[1]["current"]

        assert nav_data[2]["label"] == "Complete"
        assert nav_data[2]["count"] == 2
        expected_complete_url = reverse(
            "clinics:show_complete", kwargs={"id": clinic_id, "filter": "complete"}
        )
        assert nav_data[2]["href"] == expected_complete_url
        assert not nav_data[2]["current"]

        assert nav_data[3]["label"] == "All"
        assert nav_data[3]["count"] == 10
        expected_all_url = reverse(
            "clinics:show_all", kwargs={"id": clinic_id, "filter": "all"}
        )
        assert nav_data[3]["href"] == expected_all_url
        assert not nav_data[3]["current"]
