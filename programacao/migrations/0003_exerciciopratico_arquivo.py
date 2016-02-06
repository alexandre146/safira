# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programacao', '0002_auto_20160118_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciciopratico',
            name='arquivo',
            field=models.FileField(null=True, upload_to=b'teste', blank=True),
            preserve_default=True,
        ),
    ]
