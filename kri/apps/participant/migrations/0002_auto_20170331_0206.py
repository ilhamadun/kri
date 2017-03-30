# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import kri.apps.participant.models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(blank=True, upload_to=kri.apps.participant.models.person_image_directory),
        ),
    ]
