# Generated by Django 3.1.1 on 2020-10-06 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VirtualStockMarketApp', '0008_auto_20201006_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]