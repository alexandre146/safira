# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm
import os
import subprocess
from django.core.files import File

from mathema.models import Atividade, Curriculum

class Professor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('programacao:professor_edit', kwargs={'pk': self.pk})
    
#     def save(self, *args, **kwargs):
#         super(Professor, self).save(*args, **kwargs)
#         if not self.pk:
#             try:
#                 os.mkdir(settings.MEDIA_ROOT + "/teste/" + self.user.username)
#             except Exception, e:
#                 #print repr(e)
#                 pass
    
    class Meta:
        permissions=(('view_professor', 'view_professor'),('view_autor', 'view_autor'))


class Aluno(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nome = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(Aluno, self).save(*args, **kwargs)
#         if not self.pk:
        try:
            os.mkdir(settings.MEDIA_ROOT + "/submissao/" + self.user.username)
        except Exception, e:
            #print repr(e)
            pass

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('programacao:aluno_edit', kwargs={'pk': self.pk})

    class Meta:
        permissions=(('view_aluno', 'view_aluno'),)


class Curso(models.Model):
#     slug=models.SlugField(blank=True,max_length=100,unique=True,db_index=True)
    titulo = models.CharField(max_length=200)
    professor = models.ForeignKey(Professor)
    alunos = models.ManyToManyField(Aluno, through='AlunoCurso', blank=True)
    curriculum = models.ForeignKey(Curriculum, null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return "%s (%s)" % (self.titulo, self.professor)

    def get_absolute_url(self):
        return reverse('programacao:suporte_edit', kwargs={'pk': self.pk})


class AlunoCurso(models.Model):
    curso = models.ForeignKey(Curso)
    aluno = models.ForeignKey(Aluno)

    def __unicode__(self):
        return ("%s no curso %s" % (self.aluno, self.curso))

    def get_absolute_url(self):
        return reverse(viewname='programacao:aluno_curso_edit', kwargs={'pk': self.pk})

    
# file will be uploaded to MEDIA_ROOT/submissao/<username>/<filename>
def user_teste_directory_path(instance, filename):
    return 'teste/{0}/{1}'.format(instance.atividade.autor.username, filename)   


class ExercicioPratico(models.Model):
    atividade = models.ForeignKey(Atividade)
    titulo = models.CharField(max_length=200)
    enunciado = models.CharField(max_length=200)
    arquivoTeste = models.FileField(upload_to=user_teste_directory_path, verbose_name='Arquivo de testes unitarios' , null=True, blank=True)
    arquivoSolucao = models.FileField(upload_to=user_teste_directory_path, verbose_name='Arquivo da solucao de referencia' , null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_curso_atividade_exercicio_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return ExercicioPraticoEditForm(instance=self)


class ExercicioPraticoEditForm(ModelForm):
    class Meta:
        model = ExercicioPratico
        fields = ['titulo', 'enunciado', 'arquivoTeste', 'arquivoSolucao']

    
# file will be uploaded to MEDIA_ROOT/submissao/<username>/<filename>
def user_submissao_directory_path(instance, filename):
    return 'submissao/{0}/{1}'.format(instance.autor.user.username, filename)

    
class AlunoSubmissaoExercicioPratico(models.Model):
    exercicio = models.ForeignKey(ExercicioPratico)
    autor = models.ForeignKey(Aluno)
    arquivo = models.FileField(upload_to=user_submissao_directory_path, verbose_name='Codigo fonte', null=True, blank=True)
    dataEnvio = models.DateTimeField()
    avaliacao = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return ('Submissao de ' + self.autor.nome + ' em ' + self.exercicio.enunciado)

    def get_absolute_url(self):
        return reverse(viewname='programacao:aluno_atividade_exercicio_submissao_edit', kwargs={'pk': self.pk})


class Avaliador(models.Model):
    tipo = models.CharField(max_length=200)
    
    def __unicode__(self):
        return ('Avaliador ' + self.tipo)
    
    def avaliar(self, exercicio, submissoes, professor):
        testFile = str(exercicio.arquivoTeste)
        for submissao in submissoes:
            submissaoFile = str(submissao.arquivo)
            
            subprocess.call('python ' + settings.MEDIA_ROOT + '/' + testFile + ' ' + settings.MEDIA_ROOT + ' ' + submissaoFile + ' ' + professor.user.username +' ' + str(submissao.id), shell=True)
