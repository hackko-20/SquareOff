from django.shortcuts import render

# Create your views here.

def portfolio(request):
    return render(request, 'VirtualStockMarketApp/Portfolio.html', {})

def home(request):
    return render(request, 'VirtualStockMarketApp/Home.html')
