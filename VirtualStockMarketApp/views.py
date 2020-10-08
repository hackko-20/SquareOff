from django.shortcuts import render
from hashlib import sha256
from . import models
from django.db import IntegrityError
from django.urls import reverse
import pandas as pd
from iexfinance.stocks import get_historical_data
import requests
from django.http import HttpResponseRedirect, request
import os
import json

# api key 
if not os.getenv('IEX_TOKEN'):
    raise RuntimeError("API Key not set.")
api_key = os.getenv('IEX_TOKEN')

# Create your views here.

def home_logged_out(request):
    return render(request, 'VirtualStockMarketApp/HomeLoggedOut.html')

def register_view(request):
    """
    The register_view is called by default when the user visits the website or visits '/home'. The view 
    generates Register.html, which either directs the user to Login.html page or accepts data for a new user.
    Though called the register_view, it generates home page for all the logged out users!
    """
    if request.method == "POST":

        # input form data
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]

        # check empty fields
        if first_name == '' or last_name == '' or username == '' or password == '':
            return render(request, 'VirtualStockMarketApp/Register.html', {
                "message": "All fields are required."
            })
            
        # create object
        user = models.User(
            first_name = first_name, 
            last_name = last_name, 
            username = username,
            password = sha256(password.encode('utf-8')).hexdigest()
        )

        # if registration successful, return to Login page
        try: 
            user.save()
            return HttpResponseRedirect(reverse(login_view))

        # else if registration fails
        except IntegrityError:

            # check username duplicacy
            query_set = models.User.objects.filter(username = request.POST["username"])
            if query_set:
                return render(request, 'VirtualStockMarketApp/Register.html', {
                    "message": "An account with the same username already exists."
                })

    # if request method is GET
    return render(request, 'VirtualStockMarketApp/Register.html')


def login_view(request):
    """
    The login_view accepts data by the user for authentication. If the user submits the 
    correct credentials, the Home.html page is rendered, displaying personal information.
    Otherwise, the Login.html is re-generated displaying an error message.
    """
    if request.method == "POST":

        # input form data
        username = request.POST["username"]
        password = request.POST["password"]

        # check empty fields
        if username == '' or password == '':
            return render(request, 'VirtualStockMarketApp/Login.html', {
                "message": "All fields are required."
            })
        
        # if username or password is incorrect
        password = sha256(password.encode('utf-8')).hexdigest()
        user = models.User.objects.filter(username=username).first()

        if user is None or user.password != password:
            return render(request, 'VirtualStockMarketApp/Login.html', {"message": "Invalid Credentials"})
        
        # else if login is successful
        request.session['user_id'] = user.id
        return HttpResponseRedirect(reverse(home))
    
    # if request method is GET
    return render(request, 'VirtualStockMarketApp/Login.html')

def portfolio(request):

    if not request.session.get('user_id'):
        return HttpResponseRedirect(reverse(login_view))

    user = models.User.objects.get(id = request.session.get('user_id'))
    user_favourites = models.Favourites.objects.filter(id = request.session.get('user_id'))
    user_txn_history = models.TransactionHistory.objects.filter(id = request.session.get('user_id'))
    user_stocks_owned = models.StocksOwned.objects.filter(id = request.session.get('user_id'))

    #  calculation of net worth of the user
    # url = "https://cloud.iexapis.com/" + "stable/stock/" + "MSFT" + "/quote?token=" + api_key + "&filter=iexRealtimePrice"
    # response = requests.get(url)
    # NW= response.json() 
    # net_worth = NW["iexRealtimePrice"]
    net_worth = 0
    for txn in user_stocks_owned:
        quantity = 0
        stock_list = user_txn_history.objects.filter(stock_symbol = txn.stock_symbol)
        for stock in stock_list:
            if stock.bought == True:
                quantity += stock.quantity
            else:
                quantity -= stock.quantity
        if(quantity > 0):
            url = "https://cloud.iexapis.com/" + "stable/stock/" + txn.stock_symbol + "/quote?token=" + api_key + "&filter=iexRealtimePrice"
            response = requests.get(url)
            present_price = response.json()
            net_worth += (quantity * present_price["iexRealtimePrice"])

    #  calculation of profit/loss
    total_profit = 0
    for txn in user_stocks_owned:
        profit = 0
        stock_list = user_txn_history.objects.filter(stock_symbol = txn.stock_symbol)
        for stock in stock_list:
            if stock.bought == True:
                profit -= (stock.quantity * stock.share_price)
            else:
                profit += (stock.quantity * stock.share_price)
        total_profit += profit  
    
    return render(request, 'VirtualStockMarketApp/Portfolio.html', {"user_favourites": user_favourites, "user_transactHistory": user_txn_history, "net_worth": net_worth, "profit": total_profit, "user": user})

def home(request):
    if not request.session.get('user_id'):
        return HttpResponseRedirect(reverse(login_view))

    user_favourites = models.Favourites.objects.filter(id = request.user.id)
    return render(request,'VirtualStockMarketApp/Home.html', {"user_favourites": user_favourites})
