# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_election_cut_off_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcode',
            name='postcode',
            field=models.CharField(db_index=True, max_length=7, blank=True),
        ),
    ]
