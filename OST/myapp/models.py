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
    Name=models.CharField('Name',max_length=264)
    ContactNo=PhoneNumberField('Contact Number',null=False, blank=False, unique=True)
    Address=models.CharField(max_length=264)
    Age=models.IntegerField()
    Type = models.CharField(max_length=6, choices=USER_CHOICES, default='user')
    RefName1=models.CharField('Emergency Contact Name-1',max_length=264)
    RefContactNo1=PhoneNumberField('Emergency Contact Number-1',null=False, blank=False, unique=True)
    RefName2=models.CharField('Emergency Contact Name-2',max_length=264)
    RefContactNo2=PhoneNumberField('Emergency Contact Number-2',null=False, blank=False, unique=True)
    RefName3=models.CharField('Emergency Contact Name-3',max_length=264)
    RefContactNo3=PhoneNumberField('Emergency Contact Number-3',null=False, blank=False, unique=True)
    RefName4=models.CharField('Emergency Contact Name-4',max_length=264)
    RefContactNo4=PhoneNumberField('Emergency Contact Number-4',null=False, blank=False, unique=True)
    RefName5=models.CharField('Emergency Contact Name-5',max_length=264)
    RefContactNo5=PhoneNumberField('Emergency Contact Number-5',null=False, blank=False, unique=True)
    Accuracy=models.IntegerField(default=0)
    no_of_trips=models.IntegerField(default=0)
    no_of_sleeps=models.IntegerField(default=0)
