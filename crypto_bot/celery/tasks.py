from miningPlatform.celery import app
import datetime
from django.utils import timezone
from backend.models import ContractTransaction, Cluster, MainContract, \
    CoinsTransaction
from django.conf import settings
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from backend.Email import BaseEmail
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from django.db.models import Sum
from backend.helpers.ethermine_helper import EthermineHelper

logger = get_task_logger(__name__)


@app.task(name='backend.distribute_new_coins')
def find_new_market_positions():
    from crypto_bot.models import CoingySettings, CoinPair
    main_url = 'https://api.coinigy.com/api/v1/data'
    settings = CoingySettings.objects.get(main=True)
    coin_pairs = CoinPair.objects.filter(active=True)
    for coin_pair in coin_pairs:
        pass


app.add_periodic_task(crontab(seconds='*/1'), find_new_market_positions)
#
# def distribute_new_coins(final_date=datetime.datetime.now()):
#     final_date = timezone.make_aware(final_date,
#                                      timezone.get_current_timezone())
#     start_date = final_date - datetime.timedelta(
#         hours=settings.HOURS_TO_DISTRIBUTE)
#     for cluster in Cluster.objects.all():
#         cluster.update_payouts()
#         all_mining_coins_today = cluster.get_count_on_payouts_amount(
#             final_date=final_date,
#             start_date=start_date
#         )
#
#         print(all_mining_coins_today)
#         withdraw_coins_today = 0
#
#         for contract in cluster.contracts.filter(
#                 main_contract__status=MainContract.ACTIVE):
#             coins_for_contract = all_mining_coins_today * contract.part_power
#             if coins_for_contract:
#                 withdraw_coins_today += coins_for_contract
#                 if withdraw_coins_today > all_mining_coins_today:
#                     raise Exception
#                 with atomic():
#                     ContractTransaction.generate_transaction(
#                         contract=contract,
#                         amount=coins_for_contract
#                     )
#                     usd_rate = EthermineHelper.get_usd_rate()
#                     electricity_paid = -(contract.power /
#                                          contract.main_contract.rate.count *
#                                          contract.main_contract.rate.electricity_price / usd_rate)
#                     # print(electricity_paid)
#                     CoinsTransaction.objects.create(
#                         amount=electricity_paid,
#                         user=contract.main_contract.user
#                     )
#     send_email_coin_transaction()
#
#
# def send_email_coin_transaction():
#     for contract in MainContract.objects.filter(status=MainContract.ACTIVE):
#         full_sum = ContractTransaction.objects.filter(
#             contract__main_contract=contract,
#             created_at__gte=timezone.now() - datetime.timedelta(
#                 hours=settings.HOURS_TO_DISTRIBUTE + 1)
#         ).aggregate(
#             full_sum=Sum('amount')
#         )['full_sum']
#         if full_sum:
#             async_email_send.delay(email_type='new_coins_email',
#                                    users=contract.user,
#                                    contract=contract, full_sum=full_sum)
#
#
# @app.task(name='backend.send_email')
# def async_email_send(email_type: str, users=None, **kwargs):
#     try:
#
#         kwargs['email_type'] = email_type
#         BaseEmail.factory(kwargs).build_email(users)
#     except ObjectDoesNotExist as e:
#         pass
#
#
# app.add_periodic_task(
#     crontab(hour=0, minute=0),
#     distribute_new_coins)
#
#
# @app.task(name='backend.deactivate_contract')
# def deactivate_contract(contract_id, status):
#     from backend.models import MainContract
#     contract = MainContract.objects.get(pk=contract_id)
#     contract.deactivate_contract(status)
#
#
# @app.task(name='backend.activate_contract')
# def activate_contract(contract_id):
#     from backend.models import MainContract
#     contract = MainContract.objects.get(pk=contract_id)
#     contract.activate_contract()
#
#
# @app.task(name='backend.withdraw')
# def withdraw_ethereum(withdraw_trans_id):
#     from backend.models import WithdrawTransaction
#     from backend.helpers.ethereum_withdraw import EthereumWithdraw
#     ethereum_withdraw = EthereumWithdraw()
#     withdraw_trans = WithdrawTransaction.objects.get(pk=withdraw_trans_id)
#
#     try:
#         trans_number = ethereum_withdraw.withdraw(
#             withdraw_trans.withdraw_wallet.wallet_number, withdraw_trans.gas)
#         withdraw_trans.status = withdraw_trans.SUCCESS
#         withdraw_trans.save()
#         async_email_send.delay(email_type='success_transaction_ether',
#                                trans_number=trans_number,
#                                users=withdraw_trans.user)
#     except Exception as e:
#         async_email_send.delay(email_type='error_transaction',
#                                error=str(e))
#     return withdraw_trans
#
#
# def revoke_task(task_id):
#     app.control.revoke(task_id)
