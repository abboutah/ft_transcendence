from django import forms
from django.contrib.auth.models import User
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
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    nickname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname', 'bio']
