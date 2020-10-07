from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.register_view),          
    path('register', views.register_view),
    path('login', views.login_view),
    path('portfolio/', views.portfolio),
    path('home', views.home)
]