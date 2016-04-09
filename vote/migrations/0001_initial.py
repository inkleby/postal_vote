# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import vote.tools.django_tools


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('website', models.CharField(default=b'', max_length=255, blank=True)),
                ('postcode', models.CharField(default=b'', max_length=9, blank=True)),
                ('lad13cd', models.CharField(default=b'', max_length=13, blank=True)),
                ('address', models.TextField(default=0)),
                ('email', models.CharField(default=b'', max_length=255, blank=True)),
                ('phone', models.CharField(default=b'', max_length=255, blank=True)),
                ('forms_completed', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, vote.tools.django_tools.StockModelHelpers),
        ),
        migrations.CreateModel(
            name='Postcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('postcode', models.CharField(max_length=7, blank=True)),
                ('council', models.ForeignKey(related_name='postcode_refs', blank=True, to='vote.Council', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, vote.tools.django_tools.StockModelHelpers),
        ),
    ]
