#!/usr/bin/env bash

su -m crypto_trading_user -c "celery -A ${CELERY_CONFIG} worker -B -n default@%h --loglevel=INFO"
