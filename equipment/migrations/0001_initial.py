# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 05:21
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
                ('status', models.CharField(choices=[('IE', 'In Engagement'), ('AV', 'Available'), ('UM', 'Under Maintenance')], max_length=2)),
                ('hourly_service_rate', models.DecimalField(decimal_places=2, max_digits=12)),
                ('equipment_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentEngagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.Equipment')),
            ],
        ),
    ]
