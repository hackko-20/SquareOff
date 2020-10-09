from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.register_view),          
    path('register', views.register_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('explore', views.explore),
    path('place_order', views.place_order),
    path('portfolio', views.portfolio),
    path('home', views.home)
]