# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('idrssd', models.PositiveIntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=16)),
                ('zipcode', models.PositiveIntegerField()),
                ('assets', models.PositiveIntegerField()),
                ('deposits', models.PositiveIntegerField()),
                ('liabilities', models.PositiveIntegerField()),
                ('bank', models.ForeignKey(related_name=b'reports', to='reports.Bank')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
