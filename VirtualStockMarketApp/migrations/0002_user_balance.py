# Generated by Django 3.1.1 on 2020-10-11 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VirtualStockMarketApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=5, max_digits=50, null=True),
        ),
    ]