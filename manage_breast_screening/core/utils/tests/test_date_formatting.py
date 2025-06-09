from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
import time_machine

from ..date_formatting import format_relative_date


@time_machine.travel(datetime(2025, 5, 2, 10, tzinfo=ZoneInfo("Europe/London")))
@pytest.mark.parametrize(
    ("dateiso", "output"),
    (
        ("2025-05-02T09:00:00", "today"),
        ("2025-05-01T09:00:00", "yesterday"),
        ("2025-05-01T11:59:00", "yesterday"),
        ("2025-04-30T08:00:00", "2 days ago"),
        ("2025-05-03T07:00:00", "tomorrow"),
        ("2025-05-04T12:00:00", "in 2 days"),
        ("2024-05-02T12:00:00", "1 year ago"),
        ("2024-04-02T12:00:00", "1 year, 1 month ago"),
        ("2024-03-31T12:00:00", "1 year, 1 month, 2 days ago"),
        ("2026-03-31T12:00:00", "in 10 months, 29 days"),
    ),
)
def test_relative_dates(dateiso, output):
    assert format_relative_date(datetime.fromisoformat(dateiso)) == output
