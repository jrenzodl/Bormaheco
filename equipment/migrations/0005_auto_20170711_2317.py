# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_remove_equipment_equipment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.ImageField(default='../media/equipmentimages/defaultequipment.png', upload_to='equipmentimages'),
        ),
    ]
