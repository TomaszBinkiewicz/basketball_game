from datetime import date

from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (DetailView,
                                  DeleteView,
                                  UpdateView,
                                  CreateView,
                                  )

from basketball_game_app.forms import NewGameForm
from basketball_game_app.validators import validate_positive_int
from basketball_game_app.models import (Teams,
                                        Players,
                                        Games,
                                        Group,
                                        Part,
                                        TeamStats,
                                        )


class Base(View):
    def get(self, request):
        return render(request, 'basketball_game_app/base.html')


class AllTeamsView(View):
    def get(self, request):
        eastern_conference = Teams.objects.filter(conference_id=1).order_by("-games_won", "games_played")
        western_conference = Teams.objects.filter(conference_id=2).order_by("-games_won", "games_played")
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
        all_games = Games.objects.all().order_by('-date', '-id')
        return render(request, 'basketball_game_app/all_games.html', context={'games': all_games})


class GameDetailView(DetailView):
    model = Games


class SaveTeamStats(View):
    def get(self, request):
        pass

    def post(self, request):
        game_id = request.POST.get("game_id")
        if not (validate_positive_int(game_id)):
            return False
        game_id = int(game_id)
        game = Games.objects.get(id=game_id)
        update_team = request.POST.get('team')
        if update_team == "home":
            team = Teams.objects.get(id=game.team_home_id)
        elif update_team == "away":
            team = Teams.objects.get(id=game.team_away_id)
        stat_name = request.POST.get('stat_name')
        try:
            stats_obj = get_object_or_404(TeamStats, game_id=game_id, team=team)
        except Http404:
            stats_obj = TeamStats.objects.create(game=game, team=team)
        finally:
            if stat_name == "3Pm":
                stats_obj.three_pointers_attempted += 1
                stats_obj.three_pointers_made += 1
            elif stat_name == "2Pm":
                stats_obj.two_pointers_attempted += 1
                stats_obj.two_pointers_made += 1
            elif stat_name == "FTm":
                stats_obj.free_throws_attempted += 1
                stats_obj.free_throws_made += 1
            elif stat_name == "3Pa":
                stats_obj.three_pointers_attempted += 1
            elif stat_name == "2Pa":
                stats_obj.two_pointers_attempted += 1
            elif stat_name == "FTa":
                stats_obj.free_throws_attempted += 1
            elif stat_name == "OffReb":
                stats_obj.off_rebounds += 1
            elif stat_name == "DefReb":
                stats_obj.def_rebounds += 1
            elif stat_name == "Ast":
                stats_obj.assists += 1
            elif stat_name == "Stl":
                stats_obj.steals += 1
            elif stat_name == "Blk":
                stats_obj.blocks += 1
            elif stat_name == "Tov":
                stats_obj.turnovers += 1
            elif stat_name == "PF":
                stats_obj.personal_fouls += 1
            elif stat_name == "TF":
                stats_obj.technical_fouls += 1
            stats_obj.save()
            data = {'stats_obj': 'saved'}
        return JsonResponse(data)


class GetTeamStats(View):
    def get(self, request):
        game_id = request.GET.get("game_id")
        game = Games.objects.get(id=game_id)
        update_team = request.GET.get('team')
        if update_team == "home":
            team = game.team_home
        elif update_team == "away":
            team = game.team_away
        try:
            stats_obj = get_object_or_404(TeamStats, game_id=game_id, team=team)
        except Http404:
            stats_obj = TeamStats.objects.create(game=game, team=team)
        else:
            data = {"team": team.name, "3Pm": stats_obj.three_pointers_made, "2Pm": stats_obj.two_pointers_made,
                    "FTm": stats_obj.free_throws_made, "3Pa": stats_obj.three_pointers_attempted,
                    "2Pa": stats_obj.two_pointers_attempted, "FTa": stats_obj.free_throws_attempted,
                    "OffReb": stats_obj.off_rebounds, "DefReb": stats_obj.def_rebounds, "Ast": stats_obj.assists,
                    "Stl": stats_obj.steals, "Blk": stats_obj.blocks, "Tov": stats_obj.turnovers,
                    "PF": stats_obj.personal_fouls, "TF": stats_obj.technical_fouls}

        return JsonResponse(data)
