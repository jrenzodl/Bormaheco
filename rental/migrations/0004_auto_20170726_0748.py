# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-25 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0003_auto_20170722_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='comments',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='comments',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]