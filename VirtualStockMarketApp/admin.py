from django.contrib import admin
from .models import User, Favourites, TransactionHistory, StocksOwned

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "password")

admin.site.register(User, UserAdmin)
admin.site.register(Favourites)
admin.site.register(TransactionHistory)
admin.site.register(StocksOwned)
