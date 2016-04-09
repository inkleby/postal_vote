# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='cut_off_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
