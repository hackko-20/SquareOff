from django.shortcuts import render
from hashlib import sha256
from . import models
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

"""
The register_view is called by default when the user visits the website or visits '/home'. The view 
generates Register.html, which either directs the user to Login.html page or accepts data for a new user.
Though called the register_view, it generates home page for all the logged out users!
"""
def register_view(request):

    # if user submits data (trying to register)
    if request.method == "POST":

        # create object
        user = models.User(
            first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"], 
            username = request.POST["username"],
            email = request.POST["email"],
            password = sha256(request.POST["password"].encode('utf-8')).hexdigest()
        )

        # if registration successful, return to Login page
        try: 
            user.save()
            return render(request, 'VirtualStockMarketApp/Login.html')

        # else
        except IntegrityError:

            # check email duplicacy
            query_set = models.User.objects.filter(email = request.POST["email"])
            if query_set:
                return render(request, 'VirtualStockMarketApp/Register.html', {
                    "message": "An account with the associated Email Address already exists."
                })

            # check username duplicacy
            query_set = models.User.objects.filter(username = request.POST["username"])
            if query_set:
                return render(request, 'VirtualStockMarketApp/Register.html', {
                    "message": "An account with the same username already exists."
                })

    # user gets to the page
    return render(request, 'VirtualStockMarketApp/Register.html')

"""
The login_view accepts data by the user for authentication. If the user submits the 
correct credentials, the Home.html page is rendered, displaying personal information.
Otherwise, the Login.html is re-generated displaying an error message.
"""
def login_view(request):
    
    # if user submits data
    if request.method == "POST":
        username = request.POST["username"]
        password = sha256(request.POST["password"].encode('utf-8')).hexdigest()
        user = models.User.objects.get(username=username)

        # if username or password is incorrect
        if user is None or user.password != password:
            return render(request, 'VirtualStockMaretApp/Login.html', {"message": "Invalid Credentials"})
        
        # if login successful, go home
        return render(request, 'VirtualStockMarketApp/Home.html')
    
    # if user visits page
    return render(request, 'VirtualStockMaretApp/Login.html')

def portfolio(request):
    return render(request, 'VirtualStockMarketApp/Portfolio.html', {})

