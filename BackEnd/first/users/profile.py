from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

# Create your tests here.
#https://docs.djangoproject.com/fr/5.0/ref/forms/widgets/#django.forms.Widget.attrs
#required': une valeur booléenne indiquant si le champ de ce composant est obligatoire.
#'attrs': les attributs HTML à définir sur le composant final. Combinaison de l’attribut attrs et du paramètre attrs.
#Meta: inner class to provide metadata, ordering options, table name
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    nickname = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    matches = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    losses = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    wins = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname', 'bio', 'matches', 'wins', 'losses']


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

    def clean_email(self): #method provided by Django forms that allows you to perform custom validation on a form field.
        email = self.cleaned_data["email"] #acces to the cleaned validated form data
        if User.objects.filter(email=email).exists(): #check emails
            raise ValidationError("An user with this email already exists!")
        return email   