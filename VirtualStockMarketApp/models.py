from django.db import models
from django.contrib import admin



# Create your models here.

# User model stores records for every registered user.
class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

class Favourites(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)

class TransactionHistory(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)
    bought = models.BooleanField(null=False)
    quantity = models.IntegerField(default=0)
    share_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)

class StocksOwned(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)

# Registered models
admin.site.register(Favourites)
admin.site.register(TransactionHistory)
admin.site.register(StocksOwned)