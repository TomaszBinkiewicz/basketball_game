from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from basketball_game_app.models import (Teams,
                                        Players,
                                        Group,
                                        Games,
                                        Stats,
                                        )


class NewGameForm(forms.ModelForm):

    class Meta:
        model = Games
        fields = '__all__'
        widgets = {'date': forms.SelectDateWidget}

    def clean(self):
        cleaned_data = super().clean()
        team_1 = cleaned_data.get('team_home')
        team_2 = cleaned_data.get('team_away')
        if team_1 == team_2:
            raise forms.ValidationError('You choose the same team twice')
