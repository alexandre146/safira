# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlunoSubmissaoExercicioPratico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'submissao')),
                ('dataEnvio', models.DateTimeField()),
                ('autor', models.ForeignKey(to='programacao.Aluno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExercicioPratico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enunciado', models.CharField(max_length=200)),
                ('atividade', models.ForeignKey(to='programacao.AtividadeProgramacao')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alunosubmissaoexerciciopratico',
            name='exercicio',
            field=models.ForeignKey(to='programacao.ExercicioPratico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='atividadeprogramacao',
            name='autor',
            field=models.ForeignKey(default=1, to='programacao.Professor'),
            preserve_default=False,
        ),
    ]
