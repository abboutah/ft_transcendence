from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from PIL import Image
 

# Create your models here.
class SignupForm(UserCreationForm):
    # Configuration
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class Profile(models.Model):
    #one to one relationship, one record in a table is associated with one and only one record in another table using foreign key
    #related to user, if the user deleted then delete his profile
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    #the default image to use for a user if they don't upload one and the directory where images get uploaded
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images') 
    bio = models.TextField() #text
    nickname = models.TextField(null=True)
    #convert an object into its string, so whenever we print out the profile of user, it will display his username
    def __str__(self):
        return self.user.username
    # resizing images:override the save() method which is a method that exists for all models and it is used to save an instance of the model.
    def save(self, *args, **kwargs):
        super().save() #to make sure that saving the object to the database still work

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
# class api(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)



