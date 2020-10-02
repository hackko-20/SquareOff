from django.urls import include, path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio)
]