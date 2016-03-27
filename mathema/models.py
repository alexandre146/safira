# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm

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
    autor = models.CharField(max_length=200)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:suporte_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return SuporteEditForm(instance=self)


class SuporteEditForm(ModelForm):
    class Meta:
        model = Suporte
        fields = ['titulo', 'tipo', 'arquivo', 'link']
        

class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, through='AtividadeSuporte', null=True, blank=True)
    autor = models.CharField(max_length=200)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:atividade_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return AtividadeEditForm(instance=self)

    def get_suportes(self):
        atss = AtividadeSuporte.objects.filter(atividade_id = self.id).order_by('ordem')
        suportes = []
        for ats in atss:
            suportes. extend(list(Suporte.objects.filter(id=ats.suporte_id)))
        return suportes

    def add_meus_suportes(self):
        return Suporte.objects.filter(autor=self.autor)#.exclude(id__in=self.get_suportes())
    
    def add_outros_suportes(self):
        return Suporte.objects.all()#.exclude(id__in=self.add_meus_suportes()).exclude(id__in=self.get_suportes())


class AtividadeEditForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao']


class AtividadeSuporte(models.Model):
    atividade = models.ForeignKey(Atividade)
    suporte = models.ForeignKey(Suporte)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.atividade.titulo + " possui " + self.suporte.titulo + " (" + self.suporte.tipo + ") "


class Curriculum(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=500)
    dataCriacao = models.DateTimeField(null=True, blank=True)
    autor = models.CharField(max_length=200)
    
    def __unicode__(self):
        return (self.titulo)
    
    def get_absolute_url(self):
        return reverse(viewname='mathema:curriculum_edit', kwargs={'pk': self.pk})
    

class Objetivo(models.Model):
    curriculum = models.ForeignKey(Curriculum)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.IntegerField(null=True, blank=True)
    autor = models.CharField(max_length=200)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:objetivo_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return ObjetivoEditForm(instance=self)

    def get_topicos(self):
        topico_list = Topico.objects.filter(objetivo_id = self.id).order_by('ordem')
        return topico_list


class ObjetivoEditForm(ModelForm):
    class Meta:
        model = Objetivo
        fields = ['titulo', 'descricao', 'ordem']


class Topico(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    topicoPai = models.ForeignKey('self', null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.IntegerField(null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, through='TopicoSuporte', null=True, blank=True)
    atividades = models.ManyToManyField(Atividade, through='TopicoAtividade', null=True, blank=True)
    autor = models.CharField(max_length=200)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:topico_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return TopicoEditForm(instance=self)

    def get_atividades(self):
        tas = TopicoAtividade.objects.filter(topico_id = self.id).order_by('ordem')
        atividades = []
        for ta in tas:
            atividades.extend(list(Atividade.objects.filter(id=ta.atividade_id)))
        return atividades

    def add_minhas_atividades(self):
        return Atividade.objects.filter(autor=self.autor)#.exclude(id__in=self.get_atividades())
    
    def add_outros_atividades(self):
        return Atividade.objects.all()#.exclude(id__in=self.add_minhas_atividades()).exclude(id__in=self.get_atividades())

    def get_suportes(self):
        tss = TopicoSuporte.objects.filter(topico_id = self.id).order_by('ordem')
        suportes = []
        for ts in tss:
            suportes. extend(list(Suporte.objects.filter(id=ts.suporte_id)))
        return suportes

    def add_meus_suportes(self):
        return Suporte.objects.filter(autor=self.autor)#.exclude(id__in=self.get_suportes())
    
    def add_outros_suportes(self):
        return Suporte.objects.all()#.exclude(id__in=self.add_meus_suportes()).exclude(id__in=self.get_suportes())


class TopicoEditForm(ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'descricao', 'ordem', 'topicoPai']
        

class TopicoAtividade(models.Model):
    topico = models.ForeignKey(Topico)
    atividade = models.ForeignKey(Atividade)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.topico.titulo + " possui " + self.atividade.titulo


class TopicoSuporte(models.Model):
    topico = models.ForeignKey(Topico)
    suporte = models.ForeignKey(Suporte)
    ordem = models.IntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.topico.titulo + " possui " + self.suporte.titulo + " (" + self.suporte.tipo + ") "