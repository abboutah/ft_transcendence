from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django import forms
from PIL import Image
 
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the image was uploaded

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
    is_online = models.BooleanField(default=False)
    matches = models.IntegerField(blank=True, default=0)
    wins = models.IntegerField(blank=True, default=0)
    losses = models.IntegerField(blank=True, default=0)
    # date_played = models.DateField()
    # winner = models.ForeignKey(User, related_name='won_matches', on_delete=models.CASCADE)
    # loser = models.ForeignKey(User, related_name='lost_matches', on_delete=models.CASCADE)
    #match1 = Match.objects.create(date_played='2024-02-25', winner=user1, loser=user2)
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
        return self.friends.all().exclude(id=self.user.id)
    
    def get_number_of_friends(self):
        return self.get_friends().count()
    def get_wstats(self):
        if self.matches == 0:
            return 0
        return (self.wins/self.matches) * 100
    def get_lstats(self):
        if self.matches == 0:
            return 0
        return (self.losses/self.matches) * 100

    def get_games(self):
        return Game.objects.filter(models.Q(player1=self.user) | models.Q(player2=self.user))

    def calculate_wins_losses(self):
        games = self.get_games()
        self.wins = games.filter(winner=self.user).count()
        self.losses = games.exclude(winner=self.user).count()
        self.matches = games.count()
        self.save()
    
    # def play_match(request, match_id):
    #     # Assuming you have a view that handles playing matches
    #     match = get_object_or_404(Match, pk=match_id)

    #     # Perform the logic for the match

    #     # Update the date_played field to the current date
    #     match.date_played = date.today()
    #     match.save()
    

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

class Game(models.Model):
    # ForeignKey is used to define a many-to-one relationship between two models.
    #  When you define a ForeignKey field in a model,
    #  it creates a column in the database table for that model,
    #  which stores the primary key of the associated record in another table.
    player1 = models.ForeignKey(User, related_name= 'player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name= 'player2', on_delete=models.CASCADE)
    date = models.DateTimeField()
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.CASCADE)
