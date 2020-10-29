from django.shortcuts import render
from hashlib import sha256
from . import models
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, request, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import os
import requests
from . import tasks
import json
from datetime import date,time


# api key  
if not os.getenv('IEX_TOKEN'):
    raise RuntimeError("API Key not set.")
api_key = os.getenv('IEX_TOKEN')

# Create your views here.

# just a test
def test_celery(request):
    tasks.my_first_task.delay(100)
    return HttpResponse("good to go!")

class chartData(APIView):
    def get(self, request, format=None):
        if not request.session.get('user_id'):
            return HttpResponseRedirect(reverse(login_view))

        user_monthly_analysis = models.MonthlyAnalysis.objects.filter(userID = request.session.get('user_id'))
        labels = []
        values = []
        for row in user_monthly_analysis:
            labels.append(row.timestamp)
            values.append(row.profit)
        context = {
            'labels': labels,
            'values': values
        }
        return Response(context)

def register_view(request):
    """
    The register_view is called by default when the user visits the website or visits '/register'. The view 
    generates Register.html, which either directs the user to Login.html page or accepts data for a new user.
    Though called the register_view, it generates home page for all the logged out users!
    """
    if request.method == "POST":

        # input form data
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["cpassword"]

        # check empty fields
        if first_name == '' or last_name == '' or username == '' or password == '':
            return render(request, 'VirtualStockMarketApp/Register.html', {
                "message": "All fields are required."
            })

        if password != confirm_password:
            return render(request, 'VirtualStockMarketApp/Register.html', {
                "message": "Please confirm your password again."
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

def logout_view(request):
    """
    Logs user out, if signed in, by deleting the user_id from session.
    """
    if request.session.get('user_id'):
        del request.session['user_id']
    return HttpResponseRedirect(reverse(register_view))

def portfolio(request):
    """
    This view renders the portfolio, the page where all the information about the user is shown.
    API Reference:
        # url = "https://cloud.iexapis.com/" + "stable/stock/" + "MSFT" + "/quote?token=" + api_key + "&filter=iexRealtimePrice"
        # response = requests.get(url)
        # NW= response.json() 
        # net_worth = NW["iexRealtimePrice"]
    """
    # if the user has not logged in
    if not request.session.get('user_id'):
        return HttpResponseRedirect(reverse(login_view))

    user = models.User.objects.get(id = request.session.get('user_id'))
    user_favourites = models.Favourites.objects.filter(userID = request.session.get('user_id'))
    user_txn_history = models.TransactionHistory.objects.filter(userID = request.session.get('user_id'))
    user_stocks_owned = models.StocksOwned.objects.filter(userID = request.session.get('user_id'))
    user_monthly_analysis = models.MonthlyAnalysis.objects.filter(userID = user.id)

    # calculation of net worth of the user
    net_worth = user.balance
    num_stocks_owned = 0.
    for row in user_stocks_owned:
        quantity = user_stocks_owned.get(stock_symbol = row.stock_symbol)
        url = "https://cloud.iexapis.com/stable/stock/" + row.stock_symbol + "/quote?token=" + api_key + "&filter=latestPrice"
        if requests.get(url).status_code == 200:
            present_price = requests.get(url).json()
        else:
            presentPrice = {"latestPrice": 0}
        net_worth = float(net_worth) + (float(quantity.quantity) * float(present_price["latestPrice"]))

    #  calculation of profit/loss
    total_profit = 0
    stock_list = user_txn_history
    for stock in stock_list:
        if stock.bought == True:
            total_profit -= (stock.quantity * stock.share_price)
        else:
            total_profit += (stock.quantity * stock.share_price)
    try:
        prev_profit = user_monthly_analysis.get(timestamp = date.today()).profit
        day_profit = total_profit - prev_profit
    except:
        day_profit = total_profit
    
    return render(request, 'VirtualStockMarketApp/Portfolio.html', {
        "user_favourites": user_favourites, 
        "user_transact_history": user_txn_history, 
        "net_worth": net_worth, 
        "profit": total_profit, 
        "user": user,
        "user_stocks_owned": user_stocks_owned,
        "user_monthly_analysis": user_monthly_analysis,
        "day_profit": day_profit
    })

def place_order(request):
    """
    The page displays in-depth data about a particular stock. 
    The page also accepts data to process an order, if placed by a user.
    """
    # if the user has not logged in
    if not request.session.get("user_id"):
        return HttpResponseRedirect(reverse(login_view))

    if request.method == "GET":
        stock_symbol = "NOT FOUND"
        if request.GET.get("ss") is not None:
            stock = request.GET["ss"]
            url = "https://cloud.iexapis.com/" + "stable/stock/" + stock + "/quote?token=" + api_key
            response = requests.get(url)
            stock_details = response.json()
            return render(request, 'VirtualStockMarketApp/BuySell.html', {"stock": stock_details})
        return HttpResponseRedirect(reverse(home))   
    
    # if the user submits data to place an order
    trait = request.POST["TRAIT"]
    stock_symbol = request.POST["stock_symbol"]
    if request.POST["LimitCheck"] == 'limit':
        limit_price = True
    else:
        limit_price = False
    price = float(request.POST["price"])
    quantity = int(request.POST["quantity"])
    if limit_price is False:
        GTC = True
    elif request.POST["OrderType"] == "GTC":
        GTC = True
    else: 
        GTC = False
    stop_loss = float(request.POST["StopLoss"])
    target_price = float(request.POST["TargetPrice"])

    # creating object
    new_order = models.OrderHistory (
        userID = models.User.objects.get(id = request.session['user_id']), 
        stock_symbol = stock_symbol,
        trait = trait,
        quantity = quantity,
        GTC = GTC,
        limit_price = limit_price,
        price = price,
        timestamp = timezone.now(),
        stop_loss = stop_loss,
        target_price = target_price
    )
    
    # getting the user's current data
    user = models.User.objects.get(id=request.session["user_id"])
    current_balance = user.balance
    # check if the user already owns some stocks
    try:
        user_stocks_owned = models.StocksOwned.objects.filter(userID=request.session["user_id"])
    except:
        user_stocks_owned = models.StockOwned(
            userID = user,
            stock_symbol = stock_symbol,
            quantity = 0
        )
        user_stocks_owned.save()
    # if user opts for Cash Buy
    if trait == 'CB':

        # if user opts for Current Price
        if not limit_price:
            
            # if user can afford the purchase
            if current_balance >= (quantity * price):

                # modify user's balance
                user.balance = float(user.balance) - (float(quantity) * float(price))
                user.save()

                # modify user's stocks owned
                if user_stocks_owned.filter(stock_symbol=stock_symbol):
                    models.StocksOwned.objects.filter(stock_symbol=stock_symbol, userID=user).update(
                        quantity = user_stocks_owned.get(stock_symbol=stock_symbol).quantity + quantity
                    )
                else:
                    new_stock_owned = models.StocksOwned (
                        userID = user,
                        stock_symbol = stock_symbol,
                        quantity = quantity
                    )
                    new_stock_owned.save()

                # add transaction to history
                new_txn = models.TransactionHistory(
                    userID = user,
                    stock_symbol = stock_symbol,
                    bought = True,
                    quantity = quantity,
                    share_price = price,
                    trait = trait
                )
                new_txn.save()
                new_order.GTC = False
                if stop_loss != 0 or target_price != 0:
                    new_order.status_pending = True
                    new_order.save()
                
                else:
                    new_order.status_pending = False
                    new_order.save()

                return HttpResponseRedirect(reverse(portfolio))

            # if user cannot afford the purchase
            url = "https://cloud.iexapis.com/" + "stable/stock/" + stock_symbol + "/quote?token=" + api_key
            response = requests.get(url)
            stock_details = response.json()
            return render(request, 'VirtualStockMarketApp/BuySell.html', {
                "stock": stock_details,
                "message": "Your account balance is too low for the purchase."
            })
        
        # if user opts for Limit Price
        elif limit_price:
            new_order.status_pending = True
            new_order.save()
            return HttpResponseRedirect(reverse(portfolio))

    # if user opts for Cash Sell
    elif trait == 'CS':

        # if user opts for Current Price
        if not limit_price:
            
            # number of shares user owns for the stock
            if not user_stocks_owned.get(stock_symbol=stock_symbol):
                share_quantity = 0
            else:
                share_quantity = user_stocks_owned.get(stock_symbol=stock_symbol).quantity

            # if user has enough shares to sell
            if share_quantity >= quantity:

                # modify user's balance
                user.balance = float(user.balance) + (float(quantity) * float(price))
                user.save()

                # modify user's stocks owned
                models.StocksOwned.objects.filter(userID=user, stock_symbol=stock_symbol).update(
                    quantity = share_quantity - quantity
                )
                
                # add transaction to history
                new_txn = models.TransactionHistory(
                    userID = user,
                    stock_symbol = stock_symbol,
                    bought = False,
                    quantity = quantity,
                    share_price = price,
                    trait = trait
                )
                new_txn.save()
                new_order.GTC = False
                if stop_loss != 0 or target_price != 0:
                    new_order.status_pending = True
                    new_order.save()
                
                else:
                    new_order.status_pending = False
                    new_order.save()

                return HttpResponseRedirect(reverse(portfolio))

            # if user does not have enough shares to sell
            url = "https://cloud.iexapis.com/" + "stable/stock/" + stock_symbol + "/quote?token=" + api_key
            response = requests.get(url)
            stock_details = response.json()
            return render(request, "VirtualStockMarketApp/BuySell.html", {
                "stock": stock_details,
                "message": "You do not hold enough shares to sell."
            })

        # if user opts for Limit Price
        elif limit_price:
            new_order.status_pending = True
            new_order.save()
            return HttpResponseRedirect(reverse(portfolio))

    elif trait == 'IB':
        if not limit_price:
            pay_amount = quantity * price
            if pay_amount > user.intraday_balance:
                return render(request, "VirtualStockMarketApp/BuySell.html", {
                    "stock_symbol": stock_symbol,
                    "message": "You have exceeded your intraday transaction limit."
                })
            user.intraday_balance = float(user.intraday_balance) - float(pay_amount)
            user.save()
            new_txn = models.TransactionHistory(
                    userID = user,
                    stock_symbol = stock_symbol,
                    bought = True,
                    quantity = quantity,
                    share_price = price,
                    trait = trait
                )
            new_txn.save()
            try:
                user_intraday_stocks = models.IntradayStocksOwned.objects.filter(userID = user.id)
                if user_intraday_stocks:
                    try:
                        user_stock = user_intraday_stocks.get(stock_symbol=stock_symbol)
                        if user_stock:
                            temp = user_stock.quantity
                            models.IntradayStocksOwned.objects.filter(userID = user.id, stock_symbol = stock_symbol).update(
                                quantity = temp + quantity
                            )
                        else:
                            new_intra_order = models.IntradayStocksOwned(
                                userID = user,
                                stock_symbol = stock_symbol,
                                quantity = quantity
                            )
                            new_intra_order.save()
                    except:
                        new_intra_order = models.IntradayStocksOwned(
                                userID = user,
                                stock_symbol = stock_symbol,
                                quantity = quantity
                            )
                        new_intra_order.save()
                else:
                    new_intra_order = models.IntradayStocksOwned(
                            userID = user,
                            stock_symbol = stock_symbol,
                            quantity = quantity
                        )
                    new_intra_order.save()
            except:
                new_intra_order = models.IntradayStocksOwned(
                            userID = user,
                            stock_symbol = stock_symbol,
                            quantity = quantity
                        )
                new_intra_order.save()
            new_order.GTC = False
            if stop_loss != 0 or target_price != 0:
                new_order.status_pending = True
                new_order.save()
            else:
                new_order.status_pending = False
                new_order.save()
            return HttpResponseRedirect(reverse(portfolio))
        else:
            new_order.status_pending = True
            new_order.save()
            return HttpResponseRedirect(reverse(portfolio))

    elif trait == 'IS':
        if not limit_price:
            share_quantity = 0
            user_stock = None
            try:
                user_intraday_stocks = models.IntradayStocksOwned.objects.filter(userID = user.id)
                try:
                    user_stock = user_intraday_stocks.get(stock_symbol=stock_symbol)
                    share_quantity = user_stock.quantity
                except:
                    if user_stock is None:
                        share_quantity = 0
            except:
                share_quantity = 0
            if quantity >= share_quantity:
                share_amount = (quantity - share_quantity) * price
                if share_amount > user.intraday_balance:
                    return render(request, "VirtualStockMarketApp/BuySell.html", {
                        "stock_symbol": stock_symbol,
                        "message": "You have exceeded your intraday transaction limit."
                    })
                if user_stock:
                    user_stock.quantity = share_quantity - quantity
                    user_stock.save()
                else:
                    new_intra_order = models.IntradayStocksOwned(
                        userID = user,
                        stock_symbol = stock_symbol,
                        quantity = share_quantity - quantity
                    )
                    new_intra_order.save()
                user.intraday_balance = float(user.intraday_balance) - float(share_amount)
                user.save()
                new_order.GTC = False
                new_order.save()
                new_txn = models.TransactionHistory(
                    userID = user,
                    stock_symbol = stock_symbol,
                    bought = False,
                    quantity = quantity,
                    share_price = price,
                    trait = trait
                )
                new_txn.save()

            elif quantity < share_quantity:
                share_amount = quantity * price
                if user_stock:
                    user_stock.quantity = user_stock.quantity - quantity
                    user_stock.save()
                else:
                    user_stock = models.IntradayStocksOwned(
                        userID = user,
                        stock_symbol = stock_symbol,
                        quantity = -1 * quantity
                    )
                    user_stock.save()
                user.intraday_balance = float(user.intraday_balance) + float(share_amount)
                user.save()
                new_txn = models.TransactionHistory(
                    userID = user,
                    stock_symbol = stock_symbol,
                    bought = False,
                    quantity = quantity,
                    share_price = price,
                    trait = trait
                )
                new_txn.save()
                new_order.GTC = False
                new_order.save()

            if stop_loss != 0 or target_price != 0:
                new_order.status_pending = True
                new_order.save()

            else:
                new_order.status_pending = False
                new_order.save()
            return HttpResponseRedirect(reverse(portfolio))

        else:
            new_order.status_pending = True
            new_order.save()
            return HttpResponseRedirect(reverse(portfolio))

    else:
        return render(request, "VirtualStockMarketApp/BuySell.html", {
                "stock_symbol": stock_symbol,
                "message": "The order could not be placed. Please try again."
            })

def explore(request):
    # if user is not logged in
    if not request.user.get('user_id'):
        return HttpResponseRedirect(reverse(login_view))
    
    return render(request, 'VirtualStockMarketApp/Home.html')

def home(request):
    if not request.session.get('user_id'):
        return HttpResponseRedirect(reverse(login_view))

    user_favourites = models.Favourites.objects.filter(id = request.session.get('user_id'))
    return render(request,'VirtualStockMarketApp/Home.html', {"user_favourites": user_favourites}) 

