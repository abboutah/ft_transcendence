from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#Signals are used to perform some action on modification/creation of a particular entry in database.
# instance: The instance of a User, whether this was created or updated.
# Sender: is usually a model that notifies the receiver when an event occurs.
# Receiver: The receiver is usually a function that works on the data once it is notified of some action that has taken place for instance when a user instance is just about to be saved inside the database.
# The connection between the senders and the receivers is done through “signal dispatchers”.
# kwargs: A dictionary of keyword arguments .
# https://docs.djangoproject.com/en/3.2/ref/signals/#post-save
#post_save is the signal that is sent at the end of the save method to the receiver function
@receiver(post_save, sender=User)
#run every time a user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_logged_in)
def update_user_online_status(sender, user, request, **kwargs):
        profile = user.profile
        profile.is_online = True
        profile.save()


@receiver(user_logged_out)
def update_user_offline_status(sender, user, request, **kwargs):
        profile = user.profile
        profile.is_online = False
        profile.save()
