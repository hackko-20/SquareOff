from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from . import models
import os
import requests
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q

if not os.getenv('IEX_TOKEN'):
    raise RuntimeError("API Key not set.")
api_key = os.getenv('IEX_TOKEN')

logger = get_task_logger(__name__)
@task(name='my_first_task')
def my_first_task():
    sleep(5)
    return('first_task_done')

@task(name='end_of_market_calculations')
def end_of_market():
    # square off every user's intraday trade
    try:
        users = models.User.objects.all()
        for user in users:
            try:
                user_intraday_stocks = models.IntradayStocksOwned.filter(userID = user.id)
                for user_stock in user_intraday_stocks:
                    if user_stock.quantity != 0:
                        # if he bought more
                        if user_stock.quantity > 0:
                            url = "https://cloud.iexapis.com/stable/stock/" + user_stock.stock_symbol + "/quote?token=" + api_key + "&filter=latestPrice"
                            current_price = requests.get(url).json()["latestPrice"]
                            share_amount = user_stock.quantity * current_price
                            user.balance =  float(user.balance) + float(share_amount) 
                            user.save()
                            new_txn = models.TransactionHistory(
                                userID = user,
                                bought = False,
                                stock_symbol = user_stock.stock_symbol,
                                quantity = user_stock.quantity,
                                share_price = current_price,
                                trait = 'SS'
                            )    
                            new_txn.save()
                            user_stock.delete()
                        # if he sold more
                        else:
                            url = "https://cloud.iexapis.com/stable/stock/" + user_stock.stock_symbol + "/quote?token=" + api_key + "&filter=latestPrice"
                            current_price = requests.get(url).json()["latestPrice"]
                            share_amount = user_stock.quantity * current_price
                            if share_amount > user.balance:
                                #reset
                                pass
                            else:
                                user.balance = float(user.balance) - float(share_amount)
                                user.save()
                                new_txn = models.TransactionHistory(
                                    userID = user,
                                    bought = True,
                                    stock_symbol = user_stock.stock_symbol,
                                    quantity = user_stock.quantity,
                                    share_price = current_price,
                                    trait = 'SB'
                                )    
                                new_txn.save()
                                user_stock.delete()

                # calculate day's profit/loss
                user_txns = models.TransactionHistory.objects.filter(userID = user.id)
                user_txns_bought = user_txns.filter(bought = True)
                profit = 0
                for txn in user_txns_bought:
                    profit = float(profit) - (float(txn.share_price) * float(txn.quantity))
                user_txns_sold = user_txns.filter(bought = False)
                for txn in user_txns_sold:
                    profit = float(profit) + (float(txn.share_price) * float(txn.quantity))
                user.balance = float(user.balance) + float(profit)
                user.save()
                new_data_point = models.MonthlyAnalysis(
                    userID = user,
                    timestamp = date.today(),
                    profit = profit
                )
                new_data_point.save()
                # save it to the month model

                # reset user's intraday balance
                user.intraday_balance = 3.0 * user.balance
                user.save()
                
            except:
                user.intraday_balance = 3.0 * user.balance
                user.save()
                continue            
    except:
        return('no users right now for end of market calculations')
    return('DONE MARKET CALCULATIONS')

@task(name='execute_delayed_orders')
def delayed_orders():
    try:
        users = models.User.objects.all()
        for user in users:
            try:
                user_orders = models.OrderHistory.objects.filter(userID = user.id)
                for order in user_orders:
                    if order.status_pending == True:
                        url = "https://cloud.iexapis.com/stable/stock/" + order.stock_symbol + "/quote?token=" + api_key + "&filter=latestPrice"
                        current_price = requests.get(url).json()["latestPrice"]
                        # check if limit order is pending
                        if order.limit_price == True:
                            if order.trait == 'IS' or order.trait == 'CS':
                                if current_price >= order.price:
                                    if order.trait == 'IS':
                                        user.intraday_balance = float(user.intraday_balance) + (float(order.quantity) * float(current_price))
                                        user.save()
                                        new_txn = models.TransactionHistory(
                                            userID = user,
                                            bought = False,
                                            stock_symbol = order.stock_symbol,
                                            quantity = order.quantity,
                                            share_price = current_price,
                                            trait = 'IS'
                                        )    
                                        new_txn.save()
                                        order.limit_price = False
                                        order.save()
                                        try:
                                            user_stock = models.IntradayStocksOwned.objects.filter(userID = user.id) 
                                            user_current_stock = user_stock.get(stock_symbol = order.stock_symbol)
                                            user_current_stock.quantity = user_current_stock.quantity - order.quantity
                                            user_current_stock.save()
                                        except:
                                            new_stock = models.IntradayStocksOwned(
                                                userID = user,
                                                stock_symbol = order.stock_symbol,
                                                quantity = -1 * order.quantity
                                            )
                                            new_stock.save()
                                    else:
                                        try:
                                            user_current_stock = models.StocksOwned.objects.get(userID = user.id, stock_symbol = order.stock_symbol)
                                            if user.current_stock.quantity >= order.quantity:
                                                user_current_stock.quantity = user_current_stock.quantity - order.quantity
                                                user_current_stock.save()
                                                user.balance = float(user.balance) + (float(order.quantity) * float(current_price))
                                                user.save()
                                                new_txn = models.TransactionHistory(
                                                    userID = user,
                                                    bought = False,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = order.quantity,
                                                    share_price = current_price,
                                                    trait = 'CS'
                                                )    
                                                new_txn.save()
                                                order.limit_price = False
                                                order.save()
                                        except:
                                            continue

                            elif order.trait == 'CB' or order.trait == 'IB':
                                if current_price <= order.price:
                                    share_amount = float(current_price) * float(order.quantity)
                                    if order.trait == 'CB':
                                        if share_amount <= user.balance:
                                            try:
                                                user_stock = models.StocksOwned.objects.filter(userID = user.id)
                                                user_current_stock = user_stock.get(stock_symbol = order.stock_symbol)
                                                user_current_stock.quantity = user_current_stock.quantity + order.quantity
                                                user_current_stock.save()           
                                            except:
                                                new_stock = models.StocksOwned(
                                                    userID = user,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = order.quantity
                                                )
                                                new_stock.save()
                                            user.balance = float(user.balance) - (float(order.quantity) * float(current_price))
                                            user.save()  
                                            new_txn = models.TransactionHistory(
                                                userID = user,
                                                bought = True,
                                                stock_symbol = order.stock_symbol,
                                                quantity = order.quantity,
                                                share_price = current_price,
                                                trait = 'CB'
                                            ) 
                                            new_txn.save() 
                                            order.limit_price = False
                                            order.save()
                                    else:
                                        if share_amount <= user.intraday_balance:
                                            try:
                                                user_stock = models.IntradayStocksOwned.objects.filter(userID = user.id)
                                                user_current_stock = user_stock.get(stock_symbol = order.stock_symbol)
                                                user_current_stock.quantity = user_current_stock.quantity + order.quantity
                                                user_current_stock.save()
                                                       
                                            except:
                                                new_stock = models.IntradayStocksOwned(
                                                    userID = user,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = order.quantity
                                                )
                                                new_stock.save()
                                            user.intraday_balance = float(user.intraday_balance) - (float(order.quantity) * float(current_price))
                                            user.save() 
                                            new_txn = models.TransactionHistory(
                                                userID = user,
                                                bought = True,
                                                stock_symbol = order.stock_symbol,
                                                quantity = order.quantity,
                                                share_price = current_price,
                                                trait = 'IB'
                                            ) 
                                            new_txn.save() 
                                            order.limit_price = False
                                            order.save()
                        if order.limit_price == False:
                            if order.stop_loss != 0:
                                if order.trait == 'IB' or order.trait == 'CB':
                                    if current_price >= order.stop_loss:
                                        if order.trait == 'IB':
                                            new_txn = models.TransactionHistory(
                                                userID = user,
                                                bought = False,
                                                stock_symbol = order.stock_symbol,
                                                quantity = order.quantity,
                                                share_price = current_price,
                                                trait = 'IS'
                                            )
                                            new_txn.save()
                                            try:
                                                user_current_stock = models.IntradayStocksOwned.objects.get(userID = user.id, stock_symbol = order.stock_symbol)
                                                user_current_stock.quantity = user_current_stock.quantity - order.quantity
                                                user_current_stock.save()
                                            except:
                                                new_stock = models.IntradayStocksOwned(
                                                    userID = user,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = -1 * order.quantity
                                                )
                                                new_stock.save()
                                            user.intraday_balance = float(user.intraday_balance) + (float(order.quantity) * float(current_price))
                                            user.save()
                                            order.stop_loss = 0
                                            order.save()
                                        else:
                                            try:
                                                user_current_stock = models.StocksOwned.objects.get(userID = user.id, stock_symbol = order.stock_symbol)
                                                if user.current_stock.quantity >= order.quantity:
                                                    user_current_stock.quantity = user_current_stock.quantity - order.quantity
                                                    user_current_stock.save()
                                                    user.balance = float(user.balance) + (float(order.quantity) * float(current_price))
                                                    user.save()
                                                    new_txn = models.TransactionHistory(
                                                        userID = user,
                                                        bought = False,
                                                        stock_symbol = order.stock_symbol,
                                                        quantity = order.quantity,
                                                        share_price = current_price,
                                                        trait = 'CS'
                                                    )    
                                                    new_txn.save()
                                                    order.stop_loss = 0
                                            except:
                                                continue
                                elif order.trait == 'CS' or order.trait == 'IS':
                                    if current_price <= order.stop_loss:
                                        share_amount = float(current_price) * float(order.quantity)
                                        if order.trait == 'CS':
                                            if share_amount <= user.balance:
                                                try:
                                                    user_current_stock = models.StocksOwned.objects.get(userID = user.id, stock_symbol = order.stock_symbol)
                                                    user_current_stock.quantity = user_current_stock.quantity + order.quantity
                                                    user_current_stock.save()         
                                                except:
                                                    new_stock = models.StocksOwned(
                                                        userID = user,
                                                        stock_symbol = order.stock_symbol,
                                                        quantity = order.quantity
                                                    )
                                                    new_stock.save()
                                                user.balance = float(user.balance) - (float(order.quantity) * float(current_price))
                                                user.save()  
                                                new_txn = models.TransactionHistory(
                                                    userID = user,
                                                    bought = True,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = order.quantity,
                                                    share_price = current_price,
                                                    trait = 'CB'
                                                ) 
                                                new_txn.save() 
                                                order.stop_loss = 0
                                                order.save()
                                        else:
                                            if share_amount <= user.intraday_balance:
                                                try:
                                                    user_current_stock = models.IntradayStocksOwned.objects.get(userID = user.id, stock_symbol = order.stock_symbol)
                                                    user_current_stock.quantity = user_current_stock.quantity + order.quantity
                                                    user_current_stock.save()
                                                        
                                                except:
                                                    new_stock = models.StocksOwned(
                                                        userID = user,
                                                        stock_symbol = order.stock_symbol,
                                                        quantity = order.quantity
                                                    )
                                                    new_stock.save()
                                                user.intraday_balance = float(user.intraday_balance) - (float(order.quantity) * float(current_price))
                                                user.save() 
                                                new_txn = models.TransactionHistory(
                                                    userID = user,
                                                    bought = True,
                                                    stock_symbol = order.stock_symbol,
                                                    quantity = order.quantity,
                                                    share_price = current_price,
                                                    trait = 'IB'
                                                ) 
                                                new_txn.save() 
                                                order.stop_loss = 0
                                                order.save()
                            if order.target_price != 0:
                                pass
                        if order.limit_price == False and order.stop_loss == 0 and order.target_price == 0:
                            order.status_pending = False
                            order.save()
            except:
                continue
    except:
        return('no users for delayed orders check right now')
    return('DONE CHECKING FOR DELAYED ORDERS')

@task(name='scraping_expired_orders')
def scrape_expired_orders():
    orders = models.OrderHistory.objects.filter(status_pending = True)
    for order in orders:
        if order.GTC == False:
            order.delete()
        elif order.GTC == True:
            expiry = order.timestamp.date() + timedelta(3)
            if date.today() >= expiry:
                order.delete()
    return('DONE SCRAPING EXPIRED ORDERS')