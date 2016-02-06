# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programacao', '0003_exerciciopratico_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='alunosubmissaoexerciciopratico',
            name='avaliacao',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
