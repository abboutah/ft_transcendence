from django import forms
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width: 100%;', 'class': 'input-box'}))
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

class CodeForm(forms.Form):
    code = forms.CharField(max_length=6)




