from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django import forms
from PIL import Image
 

# Create your models here.
class Profile(models.Model):
    #one to one relationship, one record in a table is associated with one and only one record in another table using foreign key
    #related to user, if the user deleted then delete his profile
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    #the default image to use for a user if they don't upload one and the directory where images get uploaded
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    #blank indicate that a field can be left blank in forms
    #null allow field to have NULL in the database
    bio = models.TextField(blank=True, null=True) #text
    nickname = models.TextField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    #each record of the first model is related to many records of the second model and also 
    #each record of the second model is related to many records of the first model. 
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    #related_name is an attribute that can be used to specify the name of the reverse relation in Django models
    #https://djangocentral.com/understanding-related-name-in-django-models/
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

    def get_friends(self):
        return self.friends.all()
    
    def get_number_of_friends(self):
        return self.friends.all().count()

    # STATUS_CHOICES = (
    #     ('send', 'send'),
    #     ('accepted', 'accepted'),
    # )

# class api(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)

# class relationship(models.Model):
#     sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
#     status = models.CharField(max_length=8, choices=STATUS_CHOICES)

