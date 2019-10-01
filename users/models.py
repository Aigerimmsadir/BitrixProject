from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from .managers import CustomUserManager
from .utils.choices import STATUS_CHOICES

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user     = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    position = models.IntegerField(choices=STATUS_CHOICES)
    department = models.CharField(max_length=255)
    avatar   = models.ImageField(upload_to = 'images/')
    date_of_birth = models.DateField()
