from django.shortcuts import render
from hashlib import sha256
from . import models
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):

    # if user is not authenticated
    if not request.user.is_authenticated:

        # if user submits data
        if request.method == "POST":

            # create object
            user = models.User(
                first_name = request.POST["first_name"], 
                last_name = request.POST["last_name"], 
                username = request.POST["username"],
                email = request.POST["email"],
                password = sha256(request.POST["password"])
            )

            # if registration successful, return to Login page
            try: 
                user.save()
                return HttpResponseRedirect(reverse(login_view))

            # else
            except IntegrityError:

                # check email duplicacy
                query_set = models.User.objects.filter(email = request.POST["email"])
                if query_set:
                    return render(request, 'VirtualStockMarketApp/HomeLoggedOut.html', {
                        "message": "An account with the associated Email Address already exists."
                    })

                # check username duplicacy
                query_set = models.User.objects.filter(username = request.POST["username"])
                if query_set:
                    return render(request, 'VirtualStockMarketApp/HomeLoggedOut.html', {
                        "message": "An account with the same username already exists."
                    })

        # user gets to the page
        return render(request, 'VirtualStockMarketApp/HomeLoggedOut.html')

    # if user is authenticated
    return render(request, 'VirtualStockMarketApp/Home.html')

def login_view(request):
    
    # if user submits data
    if request.method == "POST":
        username = request.POST["username"]
        password = sha256(request.POST["password"])
        user = models.User.objects.get(username=username)

        # if username or password is incorrect
        if user is None or user.password != password:
            return render(request, 'VirtualStockMaretApp/Login.html', {"message": "Invalid Credentials"})
        
        # if login successful, go home
        return HttpResponseRedirect(reverse(home))
    
    # if user visits page
    return render(request, 'VirtualStockMaretApp/Login.html')

def portfolio(request):
    return render(request, 'VirtualStockMarketApp/Portfolio.html', {})

