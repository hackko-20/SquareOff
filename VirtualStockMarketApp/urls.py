from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('home/', views.home),
    path('portfolio/', views.portfolio),
]