from django import forms
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = Profile 
        fields = ['email','username','password1', 'password2']
    def clean_email(self): 
        email = self.cleaned_data["email"] 
        if Profile.objects.filter(email=email).exists():
            return None
        return email




