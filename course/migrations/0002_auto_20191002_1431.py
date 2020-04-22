# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-02 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='create_token_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='account',
            name='pwd',
            field=models.CharField(default='123', max_length=128, verbose_name='密码'),
        ),
        migrations.AddField(
            model_name='account',
            name='token',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户姓名'),
        ),
    ]