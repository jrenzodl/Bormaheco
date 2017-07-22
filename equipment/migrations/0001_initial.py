# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('acquisition_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('acquisition_date', models.DateField()),
                ('details', models.CharField(max_length=2000)),
                ('type', models.CharField(choices=[('AC', 'Air Compressor'), ('BL', 'Backhoe Loader'), ('BR', 'Breaker'), ('BD', 'Bulldozer'), ('CR', 'Crane'), ('DT', 'Dump Truck'), ('EX', 'Excavator'), ('FT', 'Flatbed Truck'), ('FL', 'Forklifts'), ('GS', 'Genarating Set'), ('LB', 'Low Bed Trailer'), ('MT', 'Manlift Truck'), ('MC', 'Motorcycle'), ('PL', 'Payloader'), ('PM', 'Prime Mover'), ('RG', 'Road Grader'), ('RR', 'Road Roller'), ('SL', 'Skidsteer Loader'), ('OT', 'Other')], max_length=2)),
                ('status', models.CharField(choices=[('IE', 'In Engagement'), ('AV', 'Available'), ('UM', 'Under Maintenance')], max_length=2)),
                ('hourly_service_rate', models.DecimalField(decimal_places=2, max_digits=12)),
                ('image', models.ImageField(default='../media/equipmentimages/defaultequipment.png', upload_to='equipmentimages')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.Equipment')),
            ],
        ),
    ]
