from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('game', views.game, name="game"),
    path('twoFactor', views.twoFactor, name="twoFactor"),
    path('RegisterUserBoutstrap', views.RegisterUserBoutstrap, name="RegisterUserBoutstrap"),
    path('atats', views.atats, name="atats"),
    path('editeProfileBootstrap', views.editeProfileBootstrap, name="editeProfileBootstrap"),
    path('invite', views.invite, name="invite"),
    path('join_match', views.join_match, name="join_match"),
    path('tournament_lobby', views.tournament_lobby, name="tournament_lobby"),
    path('tournoi2', views.tournoi2, name="tournoi2"),
    path('tournoi', views.tournoi, name="tournoi"),
]
