# Generated by Django 3.2.5 on 2021-07-29 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cef', '0002_auto_20210729_1302'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CEF',
            new_name='Ticker',
        ),
    ]