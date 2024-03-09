from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.http import HttpResponse
from django.template import loader
import json
from .models import Profile
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm,SignupForm
from django.db import IntegrityError


_DOMAIN = settings._DOMAIN
INTRA_CLIENT_ID = settings.INTRA_CLIENT_ID
INTRA_CLIENT_SECRET = settings.INTRA_CLIENT_SECRET
INTRA_REDIRECTION_URL = settings.INTRA_REDIRECTION_URL
INTRA_ACCES_TOKEN_URL = settings.INTRA_ACCES_TOKEN_URL
INTRA_AUTHORIZATION_URL = settings.INTRA_AUTHORIZATION_URL
INTRA_TOKEN_INFO = settings.INTRA_TOKEN_INFO




def intralogin(request):
    oauth_url = INTRA_AUTHORIZATION_URL
    params = {
        'client_id': INTRA_CLIENT_ID,
        'redirect_uri': INTRA_REDIRECTION_URL,
        'response_type': 'code',
    }
    full_oauth_url = oauth_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
    return redirect(full_oauth_url)


def callback(request):
    # Get the 'code' parameter from the request
    code = request.GET.get('code')
    if code == None:
        return redirect('login')
    # sending the request to exchage the redirection code with the access token
    params = {
        'grant_type' : 'authorization_code',
        'client_id': INTRA_CLIENT_ID,
        'client_secret' : INTRA_CLIENT_SECRET,
        'code' : code,
        'redirect_uri': INTRA_REDIRECTION_URL,
    }
    response = requests.post(INTRA_ACCES_TOKEN_URL, data=params)
    if response.status_code == 200:
        token_data = response.content
        token = json.loads(token_data)['access_token']
        token_type = json.loads(token_data)['token_type']
        meUrl = INTRA_TOKEN_INFO
        headers = {
            'Authorization': f'{token_type} {token}'
        }
        meResponse = requests.get(meUrl, headers=headers)
        content = meResponse.content
        user_email = json.loads(content)['email']
        username = {'username': json.loads(content)['login']}
        try:
            user = Profile.objects.create_user(email=user_email, password='', **username)
        except ValueError as v:
            return render(request, 'template.html', {'content': v})
            # return redirect('home')
    return redirect("login")

# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid() and form.clean_email() is not None:
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if password == '':
                return redirect('login')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user) 
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')