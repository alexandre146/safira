# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AtividadeSuporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordem', models.IntegerField(null=True, blank=True)),
                ('atividade', models.ForeignKey(to='mathema.Atividade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=500)),
                ('dataCriacao', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=300, null=True, blank=True)),
                ('ordem', models.IntegerField(null=True, blank=True)),
                ('curriculum', models.ForeignKey(to='mathema.Curriculum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('arquivo', models.FileField(null=True, upload_to=b'suporte', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('visualizacoes', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoSuporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=300, null=True, blank=True)),
                ('ordem', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicoAtividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordem', models.IntegerField(null=True, blank=True)),
                ('atividade', models.ForeignKey(to='mathema.Atividade')),
                ('topico', models.ForeignKey(to='mathema.Topico')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicoSuporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordem', models.IntegerField(null=True, blank=True)),
                ('suporte', models.ForeignKey(to='mathema.Suporte')),
                ('topico', models.ForeignKey(to='mathema.Topico')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='topico',
            name='atividades',
            field=models.ManyToManyField(to='mathema.Atividade', null=True, through='mathema.TopicoAtividade', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topico',
            name='objetivo',
            field=models.ForeignKey(to='mathema.Objetivo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topico',
            name='suportes',
            field=models.ManyToManyField(to='mathema.Suporte', null=True, through='mathema.TopicoSuporte', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topico',
            name='topicoPai',
            field=models.ForeignKey(blank=True, to='mathema.Topico', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suporte',
            name='tipo',
            field=models.ForeignKey(to='mathema.TipoSuporte'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atividadesuporte',
            name='suporte',
            field=models.ForeignKey(to='mathema.Suporte'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atividade',
            name='suportes',
            field=models.ManyToManyField(to='mathema.Suporte', null=True, through='mathema.AtividadeSuporte', blank=True),
            preserve_default=True,
        ),
    ]
