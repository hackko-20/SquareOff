# Generated by Django 3.1 on 2020-10-24 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VirtualStockMarketApp', '0008_user_intraday_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntradayStocksOwned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_symbol', models.CharField(max_length=64)),
                ('quantity', models.IntegerField(default=0)),
                ('userID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VirtualStockMarketApp.user')),
            ],
        ),
    ]