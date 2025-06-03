import pytest

from .factories import ParticipantFactory, ScreeningEpisodeFactory


class TestParticipant:
    @pytest.mark.parametrize(
        "category,group",
        [
            ("White", "English, Welsh, Scottish, Northern Irish or British"),
            ("Asian or Asian British", "Pakistani"),
            (None, None),
        ],
    )
    def test_ethnic_group_category(self, category, group):
        assert (
            ParticipantFactory.build(ethnic_group=group).ethnic_group_category()
            == category
        )


@pytest.mark.django_db
class TestScreeningEvent:
    def test_no_previous_screening_episode(self):
        episode = ScreeningEpisodeFactory.create()
        assert episode.previous() is None

    def test_previous_screening_episode(self):
        episode = ScreeningEpisodeFactory.create()
        next_episode = ScreeningEpisodeFactory.create(participant=episode.participant)
        assert next_episode.previous() == episode
