from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CoingySettings)


@admin.register(MarketPosition)
class MarketPositionAdmin(admin.ModelAdmin):
    list_display = ['price', 'quantity', 'coin_pair',
                    'created_at', 'updated_at']
    # list_filter = ['wall']
    # list_editable = ['wall']


@admin.register(CoinPair)
class CoinPairAdmin(admin.ModelAdmin):
    list_display = ['firstCoinName', 'secondCoinName', 'exchange_code']
    list_filter = ['firstCoinName', 'secondCoinName', 'exchange_code']
