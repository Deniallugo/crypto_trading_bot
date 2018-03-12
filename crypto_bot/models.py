from django.db import models
import datetime
from django.utils import timezone
from crypto_bot.decorators import cache_for


class CoinPair(models.Model):
    firstCoinName = models.CharField(max_length=255)
    secondCoinName = models.CharField(max_length=255)
    exchange_code = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    position_type = models.CharField(choices=(
        ('history', 'История'),
        ('asks', 'asks'),
        ('bids', 'bids'),
        ('orders', 'orders'),
        ('all', 'all'),

    ), max_length=6)

    def __str__(self):
        return f'{self.firstCoinName}/{self.secondCoinName}'


class CoingySettings(models.Model):
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    main = models.BooleanField(default=False)
    min_wall = models.FloatField(null=True)

    @classmethod
    @cache_for(60 * 5)
    def main_setting(cls):
        return cls.objects.filter(main=True)[0]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.main:
            try:
                main_setting = self.__class__.objects.get(main=True)
                main_setting.main = False
                main_setting.save()
            except self.DoesNotExist:
                pass

        super(self.__class__, self).save(force_insert, force_update, using,
                                         update_fields)

    def __str__(self):
        return self.api_key


class MarketPosition(models.Model):
    coin_pair = models.ForeignKey(CoinPair, on_delete=models.CASCADE)
    settings = models.ForeignKey(CoingySettings, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField()
    position_type = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    @cache_for(60 * 60 * 24)
    def avg_quantity_day(cls):
        return cls.objects.filter(updated_at__gte=timezone.now() -
                                                  datetime.timedelta(
                                                      days=1)).aggregate(
            avg_day=models.Avg('quantity'))['avg_day']

    @property
    @cache_for(60 * 60)
    def wall(self):
        return float(self.quantity) > min(self.avg_quantity_day() * 100,
                                          CoingySettings.main_setting().min_wall)

    def __str__(self):
        return str(self.price)
