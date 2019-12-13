from django import forms
from basketball_game_app.models import (
    Games,
)


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Games
        exclude = ['team_home_score', 'team_away_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(
            widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        )

    def clean(self):
        cleaned_data = super().clean()
        team_1 = cleaned_data.get('team_home')
        team_2 = cleaned_data.get('team_away')
        if team_1 == team_2:
            raise forms.ValidationError('You chose the same team twice')
