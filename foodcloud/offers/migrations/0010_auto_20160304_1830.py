# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0009_offer_devices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='devices',
            field=models.ManyToManyField(blank=True, null=True, related_name='offers', to='offers.Device'),
        ),
    ]
