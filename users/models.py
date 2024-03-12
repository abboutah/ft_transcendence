from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import IntegrityError

class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **others):
        if not email:
            raise ValueError('Users must have an email address')
        try:
            user = self.model(
                email=self.normalize_email(email),
            )
            user.username = others['username']
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                raise ValueError('Email already exists')
            else:
                raise e

    def create_superuser(self, email, password=None, **others):
        user = self.create_user(
            email,
            password=password,
            **others,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def create_intrauser(self, email, password=None, **others):
        user = self.create_user(
            email,
            password=password,
            **others,
        )
        user.is_student = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, blank=True)
    tournement_username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True, unique=True)
    # is_authenticated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    objects = ProfileManager()
    is_student = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]
    def __str__(self):
        return self.username

# class IntraProfileManager(BaseUserManager):

#     def create_superuser(self,username, email, phone_number,password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)
      
#         if other_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must be assigned to is_staff=True')
       
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must be assigned to is_superuser=True')
#         user =  self.create_user(username,email, phone_number, password, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_user(self, username, email, phone_number,password,**other_fields):
#         if not email:
#             raise ValueError('Email address is required!')
#         email = self.normalize_email(email)
#         if password is not None:
#             user = self.model(username=username,email=email, phone_number=phone_number,password=password, **other_fields)
#             user.save()
#         else:
#             user = self.model(username=username,email=email, phone_number=phone_number, password=password,**other_fields)
#             user.set_unusable_password()
#             user.save()

#         return user

# class IntraProfile(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=50, blank=True)
#     tournement_username = models.CharField(max_length=50, blank=True)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     email = models.EmailField(max_length=100, blank=True, unique=True)

#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_online = models.BooleanField(default=True)

#     objects = IntraProfileManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username", "first_name", "last_name"]
#     def __str__(self):
#         return self.username`