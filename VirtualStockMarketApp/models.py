from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=320, unique=True)
    password = models.CharField(max_length=30)
