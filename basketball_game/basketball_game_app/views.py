from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from basketball_game_app.models import (Teams,
                                        Players,
                                        Games,
                                        Group,
                                        )
from django.views.generic import (FormView,
                                  ListView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView,
                                  CreateView,
                                  )


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
