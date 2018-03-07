from django.db import models


class CoinPair(models.Model):
    firstCoinName = models.CharField(max_length=255)
    secondCoinName = models.CharField(max_length=255)
    exchange_code = models.CharField(max_length=255)
    active = models.BooleanField(default=True)


class CoingySettings(models.Model):
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    main = models.BooleanField(default=False)
    min_wall = models.FloatField(null=True)
    position_type = models.CharField(choices=(
        ('history', 'История'),
        ('asks', 'asks'),
        ('bids', 'bids'),
        ('orders', 'orders'),
        ('all', 'all'),

    ))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.main:
            try:
                main_setting = self.__class__.objects.get(main=True)
                main_setting.main = False
                main_setting.save()
            except self.DoesNotExist:
                pass

        super(self, self.__class__).save(force_insert, force_update, using,
                                         update_fields)


class MarketPosition(models.Model):
    coin_pair = models.ForeignKey(CoinPair, on_delete=models.CASCADE)
    settings = models.ForeignKey(CoingySettings, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField()
    position_type = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
