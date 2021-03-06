# Generated by Django 2.0 on 2018-03-07 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoingySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=255)),
                ('secret_key', models.CharField(max_length=255)),
                ('main', models.BooleanField(default=False)),
                ('min_wall', models.FloatField(null=True)),
                ('position_type', models.CharField(choices=[('history', 'История'), ('asks', 'asks'), ('bids', 'bids'), ('orders', 'orders'), ('all', 'all')], max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='CoinPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstCoinName', models.CharField(max_length=255)),
                ('secondCoinName', models.CharField(max_length=255)),
                ('exchange_code', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarketPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('total', models.FloatField()),
                ('position_type', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coin_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto_bot.CoinPair')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto_bot.CoingySettings')),
            ],
        ),
    ]
