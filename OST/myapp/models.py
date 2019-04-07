from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse("home")

USER_CHOICES= [
    ('driver', 'Driver'),
    ('user', 'User'),

    ]

class Profile(models.Model):
    Name=models.CharField(max_length=264)
    ContactNo=PhoneNumberField(null=False, blank=False, unique=True)
    Address=models.CharField(max_length=264)
    Age=models.IntegerField()
    Type = models.CharField(max_length=6, choices=USER_CHOICES, default='user')
    RefName1=models.CharField(max_length=264)
    RefContactNo1=PhoneNumberField(null=False, blank=False, unique=True)
    RefName2=models.CharField(max_length=264)
    RefContactNo2=PhoneNumberField(null=False, blank=False, unique=True)
    RefName3=models.CharField(max_length=264)
    RefContactNo3=PhoneNumberField(null=False, blank=False, unique=True)
    RefName4=models.CharField(max_length=264)
    RefContactNo4=PhoneNumberField(null=False, blank=False, unique=True)
    RefName5=models.CharField(max_length=264)
    RefContactNo5=PhoneNumberField(null=False, blank=False, unique=True)
    Accuracy=models.IntegerField(default=0)
