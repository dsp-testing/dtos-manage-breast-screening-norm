from django import forms

from .models import Ethnicity


class EthnicityForm(forms.Form):
    ethnic_background_choice = forms.ChoiceField(
        choices=Ethnicity.ethnic_background_ids_with_display_names(),
        required=True,
        error_messages={"required": "Select an ethnic background"},
    )

    def __init__(self, *args, **kwargs):
        if "participant" not in kwargs:
            raise ValueError("EthnicityForm requires a participant")
        self.participant = kwargs.pop("participant")

        # Set initial value for ethnic_background_choice from participant
        initial = kwargs.get("initial", {})
        initial["ethnic_background_choice"] = self.participant.ethnic_background_id
        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        for ethnic_background in self.non_specific_ethnic_backgrounds():
            self.fields[ethnic_background + "_details"] = forms.CharField(
                required=False
            )

    def ethnic_backgrounds_by_category(self):
        return Ethnicity.DATA.items()

    def non_specific_ethnic_backgrounds(self):
        return Ethnicity.non_specific_ethnic_backgrounds()

    def save(self):
        self.participant.ethnic_background_id = self.cleaned_data[
            "ethnic_background_choice"
        ]
        self.participant.save()
