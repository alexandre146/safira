# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import programacao.models


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
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=500)),
                ('dataCriacao', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('alunos', models.ManyToManyField(to='programacao.Aluno', null=True, through='programacao.AlunoDisciplina', blank=True)),
                ('curriculum', models.ForeignKey(blank=True, to='programacao.Curriculum', null=True)),
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
                ('arquivoTeste', models.FileField(upload_to=programacao.models.user_teste_directory_path, null=True, verbose_name=b'Arquivo de testes unitarios', blank=True)),
                ('arquivoSolucao', models.FileField(upload_to=programacao.models.user_teste_directory_path, null=True, verbose_name=b'Arquivo da solucao de referncia', blank=True)),
                ('atividade', models.ForeignKey(to='programacao.AtividadeProgramacao')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObjetivoProgramacao',
            fields=[
                ('objetivo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mathema.Objetivo')),
                ('curriculum', models.ForeignKey(to='programacao.Curriculum')),
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
                'permissions': (('view_professor', 'view_professor'), ('view_autor', 'view_autor')),
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
            model_name='alunodisciplina',
            name='disciplina',
            field=models.ForeignKey(to='programacao.Disciplina'),
            preserve_default=True,
        ),
    ]
