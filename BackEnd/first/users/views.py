from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponseRedirect
from django.contrib import messages
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



# Create your views here.
def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        #return HttpResponseRedirect(reverse("login"))
        return render(request, "index.html")
    profile = Profile.objects.get(user=request.user) #querying the database to retrieve a single object from Profile model
    return render(request, "profile.html" ,{'profile': profile})

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
    return render(request, "login.html", {
                "message": "Logged Out"
            })

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save() #sve user to the Database
            username = form.cleaned_data.get('username') # Get the username that is submitted
            messages.success(request, f'Account created for {username}!') # Show sucess message 
            return redirect('login') #redirect to login
    else: #GET method
        form = SignupForm() #create new instance 
    #print(form)
    return render(request, 'signup.html', {'form': form}) #render signup html


@login_required(login_url='login') #limit acces to logged in users, it will redirect the user to login url
def profile(request):
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

    return render(request, 'editprofile.html', {'user_form': user_form, 'profile_form': profile_form})
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