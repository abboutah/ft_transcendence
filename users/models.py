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
    otp = models.CharField(max_length=6, blank=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]
    def __str__(self):
        return self.username
