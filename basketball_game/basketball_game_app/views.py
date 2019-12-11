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
        team_home_score_total = request.session.get('team_home_score_total')
        team_away_score_total = request.session.get('team_away_score_total')
        if team_away_score_total is None or quarter == 1:
            team_away_score_total = 0
        if team_home_score_total is None or quarter == 1:
            team_home_score_total = 0
        return render(request, 'basketball_game_app/game.html',
                      context={'game_data': game, 'quarter': quarter, 'team_home_score_total': team_home_score_total,
                               'team_away_score_total': team_away_score_total})

    def post(self, request, pk, quarter):
        game = Games.objects.get(id=pk)
        team_home = game.team_home
        team_away = game.team_away
        # quarter score
        team_home_score = request.POST.get('team_home_score')
        team_away_score = request.POST.get('team_away_score')
        if not (validate_positive_int(team_away_score) and validate_positive_int(team_home_score)):
            return self.get(request, pk, quarter)
        team_away_score = int(team_away_score)
        team_home_score = int(team_home_score)
        # game score
        team_home_score_total = request.POST.get('team_home_score_total')
        team_away_score_total = request.POST.get('team_away_score_total')
        if not (validate_positive_int(team_away_score_total) and validate_positive_int(team_home_score_total)):
            return self.get(request, pk, quarter)
        team_away_score_total = int(team_away_score_total)
        team_home_score_total = int(team_home_score_total)
        request.session['team_home_score_total'] = team_home_score_total
        request.session['team_away_score_total'] = team_away_score_total
        # team stats
        team_home_score_total = request.POST.get('team_home_score_total')
        team_away_score_total = request.POST.get('team_away_score_total')
        if not (validate_positive_int(team_away_score_total) and validate_positive_int(team_home_score_total)):
            return self.get(request, pk, quarter)
        team_away_score_total = int(team_away_score_total)
        team_home_score_total = int(team_home_score_total)
        request.session['team_home_score_total'] = team_home_score_total
        request.session['team_away_score_total'] = team_away_score_total
        # saving quarter
        new_quarter = Part()
        new_quarter.game = game
        new_quarter.name = quarter
        new_quarter.score_team_away = team_away_score
        new_quarter.score_team_home = team_home_score
        new_quarter.save()
        if quarter < 5:
            quarter += 1
        if quarter > 4 and team_away_score_total != team_home_score_total:
            game.team_away_score = team_away_score_total
            game.team_home_score = team_home_score_total
            game.save()
            team_home.games_played += 1
            team_away.games_played += 1
            if team_home_score_total > team_away_score_total:
                team_home.games_won += 1
            elif team_away_score_total > team_home_score_total:
                team_away.games_won += 1
            team_away.save()
            team_home.save()
            return redirect('all-games')
        return redirect('game-view', pk, quarter)


class AllGamesView(View):
    def get(self, request):
        all_games = Games.objects.all().order_by('-date')
        return render(request, 'basketball_game_app/all_games.html', context={'games': all_games})


class GameDetailView(DetailView):
    model = Games


class SaveTeamStats(View):
    def get(self, request):
        pass

    def post(self, request):
        home_3Pm = request.POST.get("home_3Pm")
        home_2Pm = request.POST.get("home_2Pm")
        home_FTm = request.POST.get("home_FTm")
        home_3Pa = request.POST.get("home_3Pa")
        home_2Pa = request.POST.get("home_2Pa")
        home_FTa = request.POST.get("home_FTa")
        home_OffReb = request.POST.get("home_OffReb")
        home_DefReb = request.POST.get("home_DefReb")
        home_Ast = request.POST.get("home_Ast")
        home_Stl = request.POST.get("home_Stl")
        home_Blk = request.POST.get("home_Blk")
        home_Tov = request.POST.get("home_Tov")
        home_PF = request.POST.get("home_PF")
        home_TF = request.POST.get("home_TF")


"""
data: {
    "home_3Pm": home_3Pm,
    "home_2Pm": home_2Pm,
    "home_FTm": home_FTm,
    "home_3Pa": home_3Pa,
    "home_2Pa": home_2Pa,
    "home_FTa": home_FTa,
    "home_OffReb": home_OffReb,
    "home_DefReb": home_DefReb,
    "home_Ast": home_Ast,
    "home_Stl": home_Stl,
    "home_Blk": home_Blk,
    "home_Tov": home_Tov,
    "home_PF": home_PF,
    "home_TF": home_TF,
}
"""
