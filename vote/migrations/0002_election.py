# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
