from django.shortcuts import render

# Create your views here.

def Portfolio(request):
    return render(request,'VirtualStockMarketApp/Portfolio.html',{})
