# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import programacao.models


class Migration(migrations.Migration):

    dependencies = [
        ('mathema', '0001_initial'),
        ('programacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('ordem', models.IntegerField(null=True, blank=True)),
                ('disciplina', models.ForeignKey(to='programacao.Disciplina')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuporteProgramacao',
            fields=[
                ('suporte_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mathema.Suporte')),
                ('interacao', models.ForeignKey(blank=True, to='programacao.Interacao', null=True)),
            ],
            options={
            },
            bases=('mathema.suporte',),
        ),
        migrations.AddField(
            model_name='atividadeprogramacao',
            name='interacao',
            field=models.ForeignKey(blank=True, to='programacao.Interacao', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='objetivoprogramacao',
            name='interacao',
            field=models.ForeignKey(blank=True, to='programacao.Interacao', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topicoprogramacao',
            name='interacao',
            field=models.ForeignKey(blank=True, to='programacao.Interacao', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exerciciopratico',
            name='arquivoSolucao',
            field=models.FileField(upload_to=programacao.models.user_teste_directory_path, null=True, verbose_name=b'Arquivo da solucao de referencia', blank=True),
            preserve_default=True,
        ),
    ]
