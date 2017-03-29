# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 05:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kri.apps.participant.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('core_member', 'Tim Inti'), ('mechanics', 'Mekanik'), ('adviser', 'Dosen Pembimbing'), ('supporter', 'Supporter')], max_length=11)),
                ('instance_id', models.CharField(max_length=30)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('shirt_size', models.CharField(choices=[('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL'), ('xxxl', 'XXXL')], max_length=4)),
                ('photo', models.ImageField(upload_to=kri.apps.participant.models.person_image_directory)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('division', models.CharField(choices=[('krai', 'KRAI'), ('krsbi_beroda', 'KRSBI Beroda'), ('krsti', 'KRSTI'), ('krpai', 'KRPAI')], max_length=12)),
                ('arrival_time', models.DateTimeField(null=True)),
                ('transport', models.CharField(max_length=100, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=kri.apps.participant.models.team_image_directory)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbreviation', models.CharField(max_length=10, null=True)),
                ('krai', models.BooleanField(default=False)),
                ('krsbi_beroda', models.BooleanField(default=False)),
                ('krsti', models.BooleanField(default=False)),
                ('krpai', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='participant.University'),
        ),
        migrations.AddField(
            model_name='person',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='participant.Team'),
        ),
    ]
