from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(unique=True)
    name        = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=False)  #this will be false until we verify the email
    is_staff    = models.BooleanField(default=False) #this will never change to make sure no one can log in to admin panel
    created_at  = models.DateTimeField(auto_now_add=True) 

    # Awakening results
    char_class      = models.CharField(max_length=20, blank=True, null=True)
    archetype       = models.CharField(max_length=20, blank=True, null=True) 
    awakening_done  = models.BooleanField(default=False)

    # Six stats — stored as FloatField for trophy fractions later
    stat_str = models.FloatField(default=0)
    stat_end = models.FloatField(default=0)
    stat_agi = models.FloatField(default=0)
    stat_int = models.FloatField(default=0)
    stat_cha = models.FloatField(default=0)
    stat_wil = models.FloatField(default=0)

    #level and rank
    level = models.IntegerField(default=1)
    rank  = models.CharField(max_length=1, default='E')  #E, D, C, B, A, S
    exp = models.IntegerField(default=0)
    aura = models.IntegerField(default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return self.email

class OTP(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    code       = models.CharField(max_length=6)
    purpose    = models.CharField(max_length=20)  # 'verify' or 'reset'
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)