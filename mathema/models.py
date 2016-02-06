# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

class TipoSuporte(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('mathema:tipo_suporte_edit', kwargs={'pk': self.pk})


class Suporte(models.Model):
    titulo = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoSuporte)
    arquivo = models.FileField(upload_to='suporte', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    visualizacoes = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:suporte_edit', kwargs={'pk': self.pk})
    
class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, null=True, blank=True)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:atividade_edit', kwargs={'pk': self.pk})


class Objetivo(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:objetivo_edit', kwargs={'pk': self.pk})


class Topico(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.IntegerField(null=True, blank=True)
    objetivo = models.ForeignKey(Objetivo, null=True, blank=True)
    topicoPai = models.ForeignKey('self', null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, null=True, blank=True)
    atividades = models.ManyToManyField(Atividade, through='TopicoAtividade', null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:topico_edit', kwargs={'pk': self.pk})


class TopicoAtividade(models.Model):
    topico = models.ForeignKey(Topico)
    atividade = models.ForeignKey(Atividade)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.topico.titulo + " possui " + self.atividade.titulo
