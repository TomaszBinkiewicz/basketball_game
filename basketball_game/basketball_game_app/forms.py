from django import forms
from datetime import date
from basketball_game_app.models import (
    Games,
)

THIS_YEAR = date.today().year
YEARS = range(THIS_YEAR - 2, THIS_YEAR + 3)


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Games
        exclude = ['team_home_score', 'team_away_score']
        widgets = {'date': forms.SelectDateWidget(years=YEARS)}

    def clean(self):
        cleaned_data = super().clean()
        team_1 = cleaned_data.get('team_home')
        team_2 = cleaned_data.get('team_away')
        if team_1 == team_2:
            raise forms.ValidationError('You chose the same team twice')
