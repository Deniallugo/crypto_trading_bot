FROM python:3.6.4-onbuild

ENV DJANGO_SETTINGS_MODULE=crypto_trading.settings
ENV CELERY_CONFIG=crypto_trading.celery

ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos ‘’ crypto_trading_user
RUN chown -R crypto_trading_user:crypto_trading_user ./
RUN chmod +x ./run_celery.bash
