from django.db import models
from django import forms

class AccessToken(models.Model):
    token = models.CharField(max_length = 250)
# Create your models here.
