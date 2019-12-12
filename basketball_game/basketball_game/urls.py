"""basketball_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from basketball_game_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Base.as_view(), name='base'),

    path('all-teams/', views.AllTeamsView.as_view(), name='all-teams'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('add-team/', views.TeamCreate.as_view(), name='add-team'),
    path('edit-team/<int:pk>/', views.TeamUpdate.as_view(), name='edit-team'),
    path('delete-team/<int:pk>/', views.TeamDelete.as_view(), name='delete-team'),

    path('all-players/', views.AllPlayersView.as_view(), name='all-players'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player-detail'),
    path('add-player/', views.PlayerCreate.as_view(), name='add-player'),
    path('edit-player/<int:pk>/', views.PlayerUpdate.as_view(), name='edit-player'),
    path('delete-player/<int:pk>/', views.PlayerDelete.as_view(), name='delete-player'),

    path('new-game/', views.NewGameView.as_view(), name='new-game'),
    path('game/<int:pk>/<int:quarter>', views.GameView.as_view(), name='game-view'),
    path('all-games/', views.AllGamesView.as_view(), name='all-games'),
    path('game-detail/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),

    path('save-team-stats/', views.SaveTeamStats.as_view(), name='save-team-stats'),
    path('get-team-stats/', views.GetTeamStats.as_view(), name='get-team-stats'),
]
