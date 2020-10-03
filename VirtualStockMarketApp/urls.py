from django.urls import include, path
from . import views

urlpatterns = [
    path('Portfolio/',views.portfolio),
    path('home/',views.home)
]