from django.db import models
from django.contrib import admin
from django.utils import timezone


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=50, decimal_places=2, null=True, default=1.e6)
    intraday_balance = models.DecimalField(max_digits=50, decimal_places=2, null=True, default=3.e6)

class MonthlyAnalysis(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateField(null=False)
    profit = models.DecimalField(max_digits=50, decimal_places=2, null=True, default=0)
    
class Favourites(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)

class TransactionHistory(models.Model):

    TRAITS = (
        ('CB', "cash_buy"),
        ('CS', 'cash_sell'),
        ('IS', 'intraday_sell'),
        ('IB', "intraday_buy"),
        ('SS', "short_sell"),
        ('SB', "short buy")
    )

    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)
    bought = models.BooleanField(null=False)
    quantity = models.IntegerField(default=0)
    share_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    trait = models.CharField(max_length=32, choices = TRAITS)

class StocksOwned(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

class IntradayStocksOwned(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stock_symbol = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

class OrderHistory(models.Model):

    TRAITS = (
        ('CB', "cash_buy"),
        ('CS', 'cash_sell'),
        ('IS', 'intraday_sell'),
        ('IB', "intraday_buy")
    )

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=64)
    trait = models.CharField(max_length=32, choices = TRAITS)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=False)
    status_pending = models.BooleanField(null=False, default=True)
    limit_price = models.BooleanField(null=False, default=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    stop_loss = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    target_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    GTC = models.BooleanField(null=True)

