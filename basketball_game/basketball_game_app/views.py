from django.shortcuts import render
from django.views import View
from basketball_game_app.models import (Teams,
                                        Players,
                                        Games,
                                        )
from django.views.generic import (FormView,
                                  ListView,
                                  )


class AllTeamsView(View):
    def get(self, request):
        eastern_conference = Teams.objects.filter(conference=0)
        western_conference = Teams.objects.filter(conference=1)
        return render(request, 'basketball_game_app/alll_teams.html',
                      context={'east': eastern_conference, 'west': western_conference})

