from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.http import HttpResponse, HttpRequest
from django.template import loader
import json
from .models import Profile
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm,SignupForm, CodeForm
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from rest_framework import status
import random
import string

_DOMAIN = settings._DOMAIN
INTRA_CLIENT_ID = settings.INTRA_CLIENT_ID
INTRA_CLIENT_SECRET = settings.INTRA_CLIENT_SECRET
INTRA_REDIRECTION_URL = settings.INTRA_REDIRECTION_URL
INTRA_ACCES_TOKEN_URL = settings.INTRA_ACCES_TOKEN_URL
INTRA_AUTHORIZATION_URL = settings.INTRA_AUTHORIZATION_URL
INTRA_TOKEN_INFO = settings.INTRA_TOKEN_INFO
EMAIL_PROVIDER_URL = settings.EMAIL_PROVIDER_URL
EMAIL_PROVIDER_KEY = settings.EMAIL_PROVIDER_KEY
MY_EMAIL = settings.MY_EMAIL
MY_NAME = settings.MY_NAME

def Reset_opt(user):
    user.otp = ''
    user.otp_expiry_time = None
    user.save()

def generate_random_digits(n):
    return ''.join(random.choices(string.digits, k=n))

def responsetokens(user):
    refresh = RefreshToken.for_user(user)
    response = HttpResponse('Login successful. the keys are stored in the cookies of this app')
    response.set_cookie('access_token', str(refresh.access_token))
    response.set_cookie('refresh_token', str(refresh))
    response.status_code = 200
    return response

def send_email(receiver_email, verification_code):
    url = EMAIL_PROVIDER_URL
    payload = {
        "sender": {
        "name": MY_NAME,
        "email": MY_EMAIL,
        },
        "to": [
        {
            "email": receiver_email,
        }
        ],
        "htmlContent": f"<h1> your verification code :{ verification_code } </h1>",
        "subject": "verification code",
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": EMAIL_PROVIDER_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code

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
            user = Profile.objects.create_intrauser(email=user_email, password='', **{'username': username})
        dummy_request = HttpRequest()
        dummy_request.user = user
        dummy_request.session = request.session
        login(dummy_request, user)
        # Generating the opt code and set the expire time to timenow + 1h .
        verification_code = generate_random_digits(n=6)
        user.otp = verification_code
        user.otp_expiry_time = timezone.now() + timedelta(hours=1)
        user.save()

        # Send the code via email (use Django's send_mail function)
        if send_email(user_email, verification_code) == 201:
            # redirect to the verification page
            return HttpResponse({'detail': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)
        return HttpResponse({'detail': 'Error sending the email'}, status=status.HTTP_401_UNAUTHORIZED)
        # send the form to get the code and pass it to the /api/optcode to process it 
        # form = CodeForm()
        # return render(request, 'code.html', {'form': form})
    return redirect("login")

# Home page
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        print(request.body)
        form = LoginForm(request.POST)
        if form.is_valid() == False:
            print(form.errors)
            return HttpResponse("<h1>form is invalide</h1>")
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_student == True:
                # redirect the user to login with his intra .
                return HttpResponse("<h1>You are an intra user , go login with your intra account !</h1>")
            # Generating the opt code and set the expire time to timenow + 1h .
            verification_code = generate_random_digits(n=6)
            user.otp = verification_code
            user.otp_expiry_time = timezone.now() + timedelta(hours=1)
            user.save()
            # Send the code via email (use Django's send_mail function)
            if send_email(email, verification_code) == 201:
                return HttpResponse("<h1>You are logged and this page should be a verification page</h1>")
                # return redirect('api/optcode')
                # return HttpResponse({'detail': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)
            return HttpResponse("<h1>Error sending the email</h1>")
        return HttpResponse("<h1>invalide credentiels</h1>")
    return render(request, 'abas_login.html', {'form': form})

@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return redirect('login')


@permission_classes([AllowAny])
def verifycode(request):
    email = request.data.get('email')
    password = request.data.get('password')
    otp = request.data.get('otp')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user_profile = Profile.objects.get(user=user)

        # Check if the verification code is valid and not expired
        if (user_profile.verification_code == otp):
            if( user_profile.otp_expiry_time is not None and
                user_profile.otp_expiry_time > timezone.now()):
                # Verification successful, generate access and refresh tokens
                login(request, user)
                # generate tokens for the user .
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Reset verification code and expiry time
                Reset_opt(user_profile)
                return HttpResponse({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
            Reset_opt(user_profile)
            return HttpResponse({'detail': 'Expired verification code .'}, status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponse({'detail': 'Invalid verification code .'}, status=status.HTTP_401_UNAUTHORIZED)
    return HttpResponse({'detail': 'Invalid credentiels email or password  .'}, status=status.HTTP_401_UNAUTHORIZED)