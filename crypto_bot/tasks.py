from crypto_trading.celery import app

import json
from celery.utils.log import get_task_logger
import requests

logger = get_task_logger(__name__)


@app.task(name='find_new_market_positions')
def find_new_market_positions():
    from crypto_bot.models import CoingySettings, CoinPair, MarketPosition
    main_url = 'https://api.coinigy.com/api/v1/data'
    try:

        coingy_settings = CoingySettings.objects.get(main=True)
    except CoingySettings.DoesNotExist:
        return

    coin_pairs = CoinPair.objects.filter(active=True)
    headers = {
        'X-API-KEY': coingy_settings.api_key,
        'X-API-SECRET': coingy_settings.secret_key,
        'Content-Type': 'application/json'
    }

    for coin_pair in coin_pairs:
        payload = {
            "exchange_code": coin_pair.exchange_code,
            "exchange_market":
                f"{coin_pair.firstCoinName}/{coin_pair.secondCoinName}",
            "type": coin_pair.position_type,

        }
        try:
            data = requests.post(main_url, data=json.dumps(payload),
                                 headers=headers).json()
            data = data['data']
        except KeyError:
            raise Exception('failed post')

        if coin_pair.position_type == 'all':
            pass
        else:
            try:
                data = data[coin_pair.position_type]
            except KeyError:
                pass
            for market_position in data:

                market_position_obj, _ = MarketPosition.objects.update_or_create(
                    coin_pair=coin_pair,
                    settings=coingy_settings,
                    position_type=coin_pair.position_type,
                    price=market_position['price'],
                    quantity=market_position['quantity'],
                    total=market_position['total'],
                )
                if market_position_obj.wall:
                    from .utility_information import send_data
                    send_data(data=
                              f'pair {market_position_obj.coin_pair} '
                              f' биржа {market_position_obj.coin_pair.exchange_code}'
                              f' position_type '
                              f' {market_position_obj.coin_pair.position_type} '
                              f' price {market_position_obj.price} '
                              f' quantity {market_position_obj.quantity}'
                              f' time {market_position_obj.updated_at}'
                              )


app.add_periodic_task(5.0, find_new_market_positions)
