# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='bank',
        ),
        migrations.DeleteModel(
            name='Bank',
        ),
        migrations.AddField(
            model_name='report',
            name='idrssd',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
