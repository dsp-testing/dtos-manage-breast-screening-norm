from ..core.utils.date_formatting import format_date
from ..core.utils.string_formatting import format_age, format_nhs_number, sentence_case


class ParticipantPresenter:
    def __init__(self, participant):
        self._participant = participant

        self.extra_needs = participant.extra_needs
        self.ethnic_group = participant.ethnic_group
        self.full_name = participant.full_name
        self.nhs_number = format_nhs_number(participant.nhs_number)
        self.date_of_birth = format_date(participant.date_of_birth)
        self.age = format_age(participant.age())
        self.risk_level = sentence_case(participant.risk_level)

    @property
    def ethnic_group_category(self):
        category = self._participant.ethnic_group_category()
        if category:
            return category.replace("Any other", "any other")
        else:
            return None

    @property
    def address(self):
        address = self._participant.address
        if not address:
            return {}

        return {"lines": address.lines, "postcode": address.postcode}
