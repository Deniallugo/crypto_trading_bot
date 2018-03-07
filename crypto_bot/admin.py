from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CoinPair)
admin.site.register(CoingySettings)
admin.site.register(MarketPosition)
