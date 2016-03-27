# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
import os

from mathema.models import Objetivo, Topico, Atividade, Suporte, Curriculum


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
    titulo = models.CharField(max_length=200)
    professor = models.ForeignKey(Professor)
    alunos = models.ManyToManyField(Aluno, through='AlunoCurso', null=True, blank=True)
    curriculum = models.ForeignKey(Curriculum, null=True, blank=True)
    
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


class Interacao(models.Model):
    titulo = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:curso_interacao_edit', kwargs={'pk': self.pk})
    

class ObjetivoProgramacao(Objetivo):
    curriculum_temp = models.ForeignKey(Curriculum)
    interacao = models.ForeignKey(Interacao, null=True, blank=True)
    
    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:curso_objetivo_edit', kwargs={'pk': self.pk})


class TopicoProgramacao(Topico):
    interacao = models.ForeignKey(Interacao, null=True, blank=True)
   
    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_curso_topico_edit', kwargs={'pk': self.pk})
    

class AtividadeProgramacao(Atividade):
    deadline = models.DateTimeField(null=True, blank=True)
    interacao = models.ForeignKey(Interacao, null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_curso_atividade_edit', kwargs={'pk': self.pk})
 
    
# file will be uploaded to MEDIA_ROOT/submissao/<username>/<filename>
def user_teste_directory_path(instance, filename):
    return 'teste/{0}/{1}'.format(instance.atividade.autor.user.username, filename)   


class ExercicioPratico(models.Model):
    atividade = models.ForeignKey(AtividadeProgramacao)
    enunciado = models.CharField(max_length=200)
    arquivoTeste = models.FileField(upload_to=user_teste_directory_path, verbose_name='Arquivo de testes unitarios' , null=True, blank=True)
    arquivoSolucao = models.FileField(upload_to=user_teste_directory_path, verbose_name='Arquivo da solucao de referencia' , null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_curso_atividade_exercicio_edit', kwargs={'pk': self.pk})

    
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
    

class SuporteProgramacao(Suporte):
    interacao = models.ForeignKey(Interacao, null=True, blank=True)
    
    def __unicode__(self):
        return (self.titulo + "(" + self.tipo + ")")

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_curso_suporte', kwargs={'pk': self.pk})

