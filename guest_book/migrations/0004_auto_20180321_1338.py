# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-21 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest_book', '0003_auto_20180221_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
    ]
