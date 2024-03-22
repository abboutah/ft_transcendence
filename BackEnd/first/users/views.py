from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import api
from .profile import SignupForm 
# from .serializer import apiSerializer, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.views import generic
from .profile import UpdateUserForm, UpdateProfileForm
from .models import Profile
from django.db import models
import pyotp
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
import urllib.request

_DOMAIN = settings._DOMAIN
INTRA_CLIENT_ID = settings.INTRA_CLIENT_ID
INTRA_CLIENT_SECRET = settings.INTRA_CLIENT_SECRET
INTRA_REDIRECTION_URL = settings.INTRA_REDIRECTION_URL
INTRA_ACCES_TOKEN_URL = settings.INTRA_ACCES_TOKEN_URL
INTRA_AUTHORIZATION_URL = settings.INTRA_AUTHORIZATION_URL
INTRA_TOKEN_INFO = settings.INTRA_TOKEN_INFO
INTRA_USER_PASSWORD = settings.INTRA_USER_PASSWORD


# Create your views here.
def index(request):
    # If no user is signed in, return to login page:
    # if "is_online" not in request.session:
    #     # If not, create a new list
    #     request.session["is_online"] = False
    if not request.user.is_authenticated:
        #return HttpResponseRedirect(reverse("login"))
        return render(request, "index.html")
    profile = Profile.objects.get(user=request.user) #querying the database to retrieve a single object from Profile model
    return render(request, "profile.html" ,{
        'profile': profile
        })

def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            #request.session["is_online"] = True
            # request.user.profile.is_online = True
            return HttpResponseRedirect(reverse("index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    #request.session["is_online"] = False
    # request.user.profile.is_online = False
    return render(request, "login.html", {
                "message": "Logged Out"
            })

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save() #save user to the Database
            username = form.cleaned_data.get('username') # Get the username that is submitted
            messages.success(request, f'Account created for {username}!') # Show sucess message
            return redirect('login') #redirect to login
    else: #GET method
        form = SignupForm() #create new instance 
    #print(form)
    return render(request, 'signup.html', {
        'form': form
        }) #render signup html


@login_required(login_url='login') #limit acces to logged in users, it will redirect the user to login url
def profile(request):
    # allu = request.user.objects.all()
    user_id = request.user.id
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='editprofile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_id':user_id,
        # 'allu': allu
          })

@login_required(login_url='login')
def view_profile(request, username):
    # allu = request.user.objects.all()
    useru = request.user.username
    action = 'add_friend'
    #is_online = request.session.get('is_online', 'False')
    user = get_object_or_404(User, username=username) #if user doesn't exist it raises 404
    profile = Profile.objects.get(user=user) # retrieve profile 
    online = profile.is_online
    # if request.method == 'POST':
    #     # action = request.POST.get('action')  # Assuming you have a hidden input in your form indicating the action
    #     if user_id in profile.friends.id:
    #         action = 'add_friend'
    #     else:
    #         action = 'remove_friend'
    #     if action == 'add_friend':
    #         profile.friends.add(request.user)
    #         request.user.profile.friends.add(profile.user)
    #         messages.success(request, f'{profile.user.username} added to your friends list!')
    #     elif action == 'remove_friend':
    #         profile.friends.remove(request.user)
    #         request.user.profile.friends.remove(profile.user)
    #         messages.success(request, f'{profile.user.username} removed from your friends list!')
    if request.method == 'POST':
        if request.user in profile.friends.all():
            action = 'remove_friend'
            profile.friends.remove(request.user)
            request.user.profile.friends.remove(profile.user)
            messages.success(request, f'{profile.user.username} removed from your friends list!')
        else:
            action = 'add_friend'
            profile.friends.add(request.user)
            request.user.profile.friends.add(profile.user)
            messages.success(request, f'{profile.user.username} added to your friends list!')

    elif request.user in profile.friends.all():
        action = 'remove_friend'
    else:
        action = 'add_friend'
    return render(request, 'view_profile.html', {
        'profile': profile,
        'online':online,
        'useru':useru,
        'action': action,
        # 'allu': allu
        })

@login_required(login_url='login')
def list_users(request):
    users = User.objects.all()
    return render(request, 'ausers.html', {'users': users})

@login_required(login_url='login')
def game(request):
    # Logic to play a game and save it to the database
    # Assuming you have retrieved the relevant players and saved the game
    # game = Game.objects.create(player1=request.user, player2=opponent_user, winner=winner_user)
    # Get the current user's profile
    profile = request.user.profile
    # Update wins, losses, and matches for the profile
    profile.calculate_wins_losses()
    # Get all users who are online and not friends
    online_users = User.objects.filter(profile__is_online=True).exclude(id=request.user.id)
    # Redirect to some page after playing the game
    return render(request, 'game.html' , {
        'online_users': online_users
        })


def redirecturi(request):
    #get the code we received from the url
    if request.method == "GET":
        code = request.GET.get('code')
        #if the user authorize the application to access they account
        if code:
            #exchange the code for an  access token
            grant_response = requests.post(INTRA_ACCES_TOKEN_URL, data = {
                'grant_type' : 'authorization_code', 
                'client_id': INTRA_CLIENT_ID,
                'client_secret' : INTRA_CLIENT_SECRET,
                'code' : code, 
                'redirect_uri': INTRA_REDIRECTION_URL,
            })
            if grant_response.status_code == 200:
                access_token = grant_response.json()["access_token"]
                #make api request with the token
                api_request = requests.get(INTRA_TOKEN_INFO, headers = {
                    "Authorization": f"Bearer {access_token}"
                    })
                user_email = api_request.json()['email']
                username = api_request.json()['login']
                first_name = api_request.json()['first_name']
                last_name = api_request.json()['last_name']
                # avatarx = api_request.json()['image']
                # avatar = avatarx['versions']['large']
                # response = urllib.request.urlopen(avatar)
                # Create a file object from the fetched image
                # image_file = File(response)
                # Create an UploadedImage object and save it
                # uploaded_image = UploadedImage()
                # uploaded_image.image.save(url.split("/")[-1], image_file, save=True)  # Save the image with a filename extracted from the URL
                # Optionally, you can return the UploadedImage object or any other response
                # Check if the user already exists
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    # existing_user.first_name = first_name
                    # existing_user.last_name = last_name
                    # existing_user.profile.avatar = "'/media/large_' + username + '.jpg'"
                    # print(avatar)
                    # existing_user.save()
                    usera = authenticate(request, username=username, password=INTRA_USER_PASSWORD)
                    login(request, usera)
                    return HttpResponseRedirect(reverse("index"))
                # User doesn't exist, create a new user
                else:
                    new_user = User.objects.create_user(username=username, email=user_email, password=INTRA_USER_PASSWORD)
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    # new_user.profile.avatar = avatar
                    # print(avatar)
                    new_user.save()
                    usera = authenticate(request, username=username, password=INTRA_USER_PASSWORD)
                    login(request, usera)
                    return HttpResponseRedirect(reverse("index"))
    else:
        return redirect('index')


# @login_required(login_url='login')
# def email_verification(request):
#     key = "SecretKeyHeeere"
#     totp = pyotp.TOTP(key)
#     code = totp.at(30)
#     send_mail(
#         "Subject here",
#         "Here is the message.",
#         settings.EMAIL_HOST_USER,
#         ["boutahriabdelkhalek@gmail.com"],
#         fail_silently=False,
#     )
#     return render(request, 'email.html', {
#         'code':code
#     })
# @api_view(['GET'])  #display the api
# def apix(request):
#     Api = api.objects.all() #retrieve all the data from the database 
#     serializer = apiSerializer(Api, many=True) #serialize the data and returned it as a response in JSON format
#     return Response(serializer.data) #help return sterlized data in JSON

# @api_view(['POST'])
# def apip(request):
#     serializer = apiSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)