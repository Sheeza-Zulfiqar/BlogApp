# Generated by Django 3.2.6 on 2021-08-22 18:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0007_auto_20210822_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 22, 18, 50, 41, 91051, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 22, 18, 50, 41, 90425, tzinfo=utc)),
        ),
    ]