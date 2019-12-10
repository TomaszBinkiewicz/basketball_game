from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from basketball_game_app.validators import validate_positive_int
from basketball_game_app.models import (Teams,
                                        Players,
                                        Games,
                                        Group,
                                        Part,
                                        )
from django.views.generic import (FormView,
                                  ListView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView,
                                  CreateView,
                                  )
from basketball_game_app.forms import NewGameForm


class AllTeamsView(View):
    def get(self, request):
        eastern_conference = Teams.objects.filter(conference_id=1)
        western_conference = Teams.objects.filter(conference_id=2)
        return render(request, 'basketball_game_app/all_teams.html',
                      context={'east': eastern_conference, 'west': western_conference})


class TeamDetailView(DetailView):
    model = Teams


class TeamCreate(CreateView):
    model = Teams
    fields = '__all__'
    template_name = 'basketball_game_app/add_team.html'


class TeamUpdate(UpdateView):
    model = Teams
    fields = '__all__'
    template_name_suffix = '_update_form'


class TeamDelete(DeleteView):
    model = Teams
    template_name = 'basketball_game_app/delete_form.html'
    success_url = reverse_lazy('all-teams')


class PlayerDetailView(DetailView):
    model = Players


class PlayerCreate(CreateView):
    model = Players
    fields = '__all__'
    template_name = 'basketball_game_app/add_player.html'


class PlayerUpdate(UpdateView):
    model = Players
    fields = '__all__'
    template_name_suffix = '_update_form'


class AllPlayersView(View):
    def get(self, request):
        all_players = Players.objects.all()
        teams = Teams.objects.all()
        groups = Group.objects.all()
        return render(request, 'basketball_game_app/all_players.html',
                      context={'players': all_players, 'teams': teams, 'groups': groups})


class PlayerDelete(DeleteView):
    model = Players
    template_name = 'basketball_game_app/delete_form.html'
    success_url = reverse_lazy('all-players')


class NewGameView(View):

    def get(self, request):
        today = date.today()
        form = NewGameForm(initial={'date': today})
        return render(request, 'basketball_game_app/new_game_form.html', {'form': form})

    def post(self, request):
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.save()
            return redirect('game-view', game.id, 1)
        return render(request, 'basketball_game_app/new_game_form.html', {'form': form})


class GameView(View):

    def get(self, request, pk, quarter):
        game = Games.objects.get(id=pk)
        return render(request, 'basketball_game_app/game.html', context={'game_data': game})

    def post(self, request, pk, quarter):
        game = Games.objects.get(id=pk)
        team_home_score = request.POST.get('team_home_score')
        team_away_score = request.POST.get('team_away_score')
        if not (validate_positive_int(team_away_score) and validate_positive_int(team_home_score)):
            print('tutaj')
            return self.get(request, pk, quarter)
        team_away_score = int(team_away_score)
        team_home_score = int(team_home_score)
        new_quarter = Part()
        new_quarter.game = game
        new_quarter.name = quarter
        new_quarter.score_team_away = team_away_score
        new_quarter.score_team_home = team_home_score
        new_quarter.save()
        if quarter < 5:
            quarter += 1
        return redirect('game-view', pk, quarter)
