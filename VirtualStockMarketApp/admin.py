from django.contrib import admin
from .models import User, Favourites, TransactionHistory, StocksOwned, OrderHistory, IntradayStocksOwned, MonthlyAnalysis

#Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "password", "balance", "intraday_balance")

class FavouritesAdmin(admin.ModelAdmin):
    list_display = ("userID", "stock_symbol")

class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ("userID", "stock_symbol","bought", "quantity", "share_price")

class StocksOwnedAdmin(admin.ModelAdmin):
    list_display = ("userID", "stock_symbol", "quantity")

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("userID", "stock_symbol", "trait", "quantity","timestamp", "status_pending", "limit_price", "stop_loss", "target_price", "price", "GTC")

admin.site.register(User, UserAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
admin.site.register(StocksOwned, StocksOwnedAdmin)
admin.site.register(IntradayStocksOwned)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(MonthlyAnalysis)

