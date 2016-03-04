# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_auto_20160304_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='userdevices',
            name='user',
        ),
        migrations.RemoveField(
            model_name='device',
            name='user_devices',
        ),
        migrations.DeleteModel(
            name='UserDevices',
        ),
        migrations.AddField(
            model_name='device',
            name='app_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='offers.AppUser'),
            preserve_default=False,
        ),
    ]
