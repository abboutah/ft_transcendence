from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponseRedirect
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