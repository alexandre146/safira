# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mathema', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_aluno', 'view_aluno'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlunoDisciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(to='programacao.Aluno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AtividadeProgramacao',
            fields=[
                ('atividade_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mathema.Atividade')),
                ('deadline', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=('mathema.atividade',),
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('alunos', models.ManyToManyField(to='programacao.Aluno', null=True, through='programacao.AlunoDisciplina', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObjetivoProgramacao',
            fields=[
                ('objetivo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mathema.Objetivo')),
                ('disciplina', models.ForeignKey(to='programacao.Disciplina')),
            ],
            options={
            },
            bases=('mathema.objetivo',),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_professor', 'view_professor'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicoProgramacao',
            fields=[
                ('topico_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mathema.Topico')),
            ],
            options={
            },
            bases=('mathema.topico',),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='professor',
            field=models.ForeignKey(to='programacao.Professor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atividadeprogramacao',
            name='autor',
            field=models.ForeignKey(blank=True, to='programacao.Professor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alunodisciplina',
            name='disciplina',
            field=models.ForeignKey(to='programacao.Disciplina'),
            preserve_default=True,
        ),
    ]
