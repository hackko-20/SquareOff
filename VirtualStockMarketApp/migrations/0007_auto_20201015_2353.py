# Generated by Django 3.1 on 2020-10-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VirtualStockMarketApp', '0006_auto_20201015_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1000000.0, max_digits=50, null=True),
        ),
    ]
