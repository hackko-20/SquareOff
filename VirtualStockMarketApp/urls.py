from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.register_view),          
    path('home/', views.register_view),
    path('login/', views.login_view),
    path('portfolio/', views.portfolio),
    path('user/',views.homeLoggedIn)
]