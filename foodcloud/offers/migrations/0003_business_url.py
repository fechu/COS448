# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='url',
            field=models.URLField(default='http://www.google.ch'),
            preserve_default=False,
        ),
    ]
