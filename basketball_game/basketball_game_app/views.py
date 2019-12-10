from django.shortcuts import render
from django.views import View
from basketball_game_app.models import (Teams,
                                        Players,
                                        Games,
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
