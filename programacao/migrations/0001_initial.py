# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import programacao.models
import django.db.models.deletion
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
            name='AlunoCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(to='programacao.Aluno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlunoSubmissaoExercicioPratico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=programacao.models.user_submissao_directory_path, null=True, verbose_name=b'Codigo fonte', blank=True)),
                ('dataEnvio', models.DateTimeField()),
                ('avaliacao', models.FloatField(null=True, blank=True)),
                ('autor', models.ForeignKey(to='programacao.Aluno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('alunos', models.ManyToManyField(to='programacao.Aluno', null=True, through='programacao.AlunoCurso', blank=True)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='mathema.Curriculum', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExercicioPratico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('enunciado', models.CharField(max_length=200)),
                ('arquivoTeste', models.FileField(upload_to=programacao.models.user_teste_directory_path, null=True, verbose_name=b'Arquivo de testes unitarios', blank=True)),
                ('arquivoSolucao', models.FileField(upload_to=programacao.models.user_teste_directory_path, null=True, verbose_name=b'Arquivo da solucao de referencia', blank=True)),
                ('atividade', models.ForeignKey(to='mathema.Atividade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_professor', 'view_professor'), ('view_autor', 'view_autor')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='curso',
            name='professor',
            field=models.ForeignKey(to='programacao.Professor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alunosubmissaoexerciciopratico',
            name='exercicio',
            field=models.ForeignKey(to='programacao.ExercicioPratico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alunocurso',
            name='curso',
            field=models.ForeignKey(to='programacao.Curso'),
            preserve_default=True,
        ),
    ]
