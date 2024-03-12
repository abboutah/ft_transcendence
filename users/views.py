from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.http import HttpResponse, HttpRequest
from django.template import loader
import json
from .models import Profile
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm,SignupForm
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    code = request.GET.get('code')
    if code == None:
        return redirect('login')
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
        username = json.loads(content)['login']
        try:
            user = Profile.objects.get(email=user_email)
        except Profile.DoesNotExist:
            # we can redirect the client to signupform full of his credentiels and delete the instance is_client from profile
            # with the above idea we can give the intra users to login with there email password too .
            user = Profile.objects.create_intrauser(email=user_email, password='', **{'username': username})
        dummy_request = HttpRequest()
        dummy_request.user = user
        dummy_request.session = request.session
        login(dummy_request, user)
        return responsetokens(user)
        # return redirect('home')
    return redirect("login")


# Home page
# @api_view['GET']
# @permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
# @api_view['GET', 'POST']
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_student == True:
                    return render(request, 'login.html', {'form': form, 'message':'You can only authentificate with this acount using your intra profile'})
                login(request, user)
                return responsetokens(user)
    else:
        form = LoginForm()
    if request.user.is_authenticated == False:
        return render(request, 'login.html', {'form': form})
    return redirect('home')


# logout page
# @api_view['POST']
def user_logout(request):
    logout(request)
    return redirect('login')

def responsetokens(user):
    refresh = RefreshToken.for_user(user)
    response = HttpResponse('Login successful. the keys are stored in the cookies of this app')
    response.set_cookie('access_token', str(refresh.access_token))
    response.set_cookie('refresh_token', str(refresh))
    response.status_code = 200
    return response