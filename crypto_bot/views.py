from django.shortcuts import render

# Create your views here.
from django.core import serializers
from crypto_bot.models import MarketPosition
from django.http import JsonResponse
import datetime
from django.core.serializers.json import DjangoJSONEncoder


def get_data(request):
    start_date = int(request.GET.get('start_date', 0))
    wall = request.GET.get('wall', False)
    start_date = datetime.datetime.utcfromtimestamp(start_date)
    market_position = MarketPosition.objects.filter(
        updated_at__gte=start_date, wall=wall)
    data = serializers.serialize('json', market_position,
                                 cls=DjangoJSONEncoder)
    return JsonResponse(data, safe=False)

