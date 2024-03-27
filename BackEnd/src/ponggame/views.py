from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def game(request):
    return render(request, 'game.html')

def profile(request):
    return render(request, 'profile.html')

def twoFactor(request):
    return render(request, 'twoFactor.html')

def RegisterUserBoutstrap(request):
    return render(request, 'RegisterUserBoutstrap.html')

def atats(request):
    return render(request, 'atats.html')


def editeProfileBootstrap(request):
    return render(request, 'editeProfileBootstrap.html')

def invite(request):
    return render(request, 'invite.html')

def join_match(request):
    return render(request, 'join_match.html')

def tournament_lobby(request):
    return render(request, 'tournament_lobby.html')

def tournoi2(request):
    return render(request, 'tournoi2.html')

def tournoi(request):
    return render(request, 'tournoi.html')
