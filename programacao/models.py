# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from mathema.models import Objetivo, Topico, Atividade, TopicoAtividade, Suporte

class Professor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('programacao:professor_edit', kwargs={'pk': self.pk})
    
    class Meta:
        permissions=(('view_professor', 'view_professor'),)


class Aluno(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nome = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('programacao:aluno_edit', kwargs={'pk': self.pk})

    class Meta:
        permissions=(('view_aluno', 'view_aluno'),)


class Disciplina(models.Model):
    titulo = models.CharField(max_length=200)
    professor = models.ForeignKey(Professor)
    alunos = models.ManyToManyField(Aluno, through='AlunoDisciplina', null=True, blank=True)
    
    def __unicode__(self):
        return "%s (%s)" % (self.titulo, self.professor)

    def get_absolute_url(self):
        return reverse('programacao:suporte_edit', kwargs={'pk': self.pk})


class AlunoDisciplina(models.Model):
    disciplina = models.ForeignKey(Disciplina)
    aluno = models.ForeignKey(Aluno)

    def __unicode__(self):
        return ("%s na disciplina %s" % (self.aluno, self.disciplina))

    def get_absolute_url(self):
        return reverse(viewname='programacao:aluno_disciplina_edit', kwargs={'pk': self.pk})


class ObjetivoProgramacao(Objetivo):
    disciplina = models.ForeignKey(Disciplina)
    
    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:disciplina_objetivo_edit', kwargs={'pk': self.pk})


class TopicoProgramacao(Topico):
   
    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:disciplina_topico_edit', kwargs={'pk': self.pk})
    

class AtividadeProgramacao(Atividade):
    autor = models.ForeignKey(Professor)
    deadline = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:disciplina_atividade_edit', kwargs={'pk': self.pk})
    
   

class ExercicioPratico(models.Model):
    atividade = models.ForeignKey(AtividadeProgramacao)
    enunciado = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to='teste', null=True, blank=True)

    def __unicode__(self):
        return (self.titulo)

    def get_absolute_url(self):
        return reverse(viewname='programacao:professor_disciplina_atividade_exercicio_edit', kwargs={'pk': self.pk})
    
    
class AlunoSubmissaoExercicioPratico(models.Model):
    exercicio = models.ForeignKey(ExercicioPratico)
    autor = models.ForeignKey(Aluno)
    arquivo = models.FileField(upload_to='submissao', null=True, blank=True)
    dataEnvio = models.DateTimeField()
    avaliacao = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return ('Submissao de ' + self.autor.nome + ' em ' + self.exercicio.enunciado)

    def get_absolute_url(self):
        return reverse(viewname='programacao:aluno_atividade_exercicio_submissao_edit', kwargs={'pk': self.pk})
    
    