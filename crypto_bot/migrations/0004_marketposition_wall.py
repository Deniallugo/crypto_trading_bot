# Generated by Django 2.0 on 2018-03-07 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_bot', '0003_marketposition_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketposition',
            name='wall',
            field=models.BooleanField(default=False),
        ),
    ]