# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelForm
from django import forms

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
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:suporte_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return SuporteEditForm(instance=self)

    def get_topico_suporte_edit_form(self):
        ts = TopicoSuporte.objects.get(suporte=self)
        return TopicoSuporteEditForm(instance=ts)

    def get_atividade_suporte_edit_form(self):
        ats = AtividadeSuporte.objects.get(suporte=self)
        return AtividadeSuporteEditForm(instance=ats)

    def copy(self):
        suporte = Suporte.objects.create(titulo=self.titulo, tipo=self.tipo, arquivo=self.arquivo, link=self.link, visualizacoes=0, autor=self.autor)
        return suporte

class SuporteEditForm(ModelForm):
    class Meta:
        model = Suporte
        fields = ['titulo', 'tipo', 'arquivo', 'link']
        

class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, through='AtividadeSuporte', null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    deadline = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:atividade_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return AtividadeEditForm(instance=self)

    def get_topico_atividade_edit_form(self):
        ta = TopicoAtividade.objects.get(atividade=self)
        return TopicoAtividadeEditForm(instance=ta)

    def get_suportes(self):
        atss = AtividadeSuporte.objects.filter(atividade_id = self.id).order_by('ordem')
        suportes = []
        for ats in atss:
            suportes.extend(list(Suporte.objects.filter(id=ats.suporte_id)))
        return suportes

    def add_meus_suportes(self):
        return list(set(list(Suporte.objects.filter(autor=self.autor))) - set(self.get_suportes()))
    
    def add_outros_suportes(self):
        return list(set(list(Suporte.objects.exclude(autor=self.autor))) - set(self.get_suportes()))

    def get_exercicios(self):
        from programacao.models import ExercicioPratico
        return ExercicioPratico.objects.filter(atividade=self)

    def copy(self):
        atividade = Atividade.objects.create(titulo=self.titulo, descricao=self.descricao, autor=self.autor)
        # copia dos suportes
#         suportes_list = []
#         atividades_suportes = AtividadeSuporte.objects.filter(atividade=self)
#         for ats in atividades_suportes :
#             suportes_list.extend(list(Suporte.objects.filter(id=ats.suporte.id)))
        for suporte in self.get_suportes() :
            novo_suporte = suporte.copy()
            novo_suporte.atividade = atividade
            novo_suporte.save()

            AtividadeSuporte.objects.create(atividade=atividade, suporte=novo_suporte)
        return atividade

class AtividadeEditForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime'}, format='%d/%m/%Y'),
        }

class AtividadeSuporte(models.Model):
    atividade = models.ForeignKey(Atividade)
    suporte = models.ForeignKey(Suporte)
    ordem = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.atividade.titulo + " possui " + self.suporte.titulo + " (" + self.suporte.tipo.nome + ") "

class AtividadeSuporteEditForm(ModelForm):
    class Meta:
        model = AtividadeSuporte
        fields = ['ordem']

class Curriculum(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=500)
    dataCriacao = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    def __unicode__(self):
        return (self.titulo)
    
    def get_absolute_url(self):
        return reverse(viewname='mathema:curriculum_edit', kwargs={'pk': self.pk})
    
    def copy(self):
        curriculum = Curriculum.objects.create(titulo=self.titulo, descricao=self.descricao, dataCriacao= self.dataCriacao, autor=self.autor)
        objetivos_list = Objetivo.objects.filter(curriculum=self)
        for objetivo in objetivos_list :
            novo_objetivo = objetivo.copy()
            novo_objetivo.curriculum = curriculum
            novo_objetivo.save()
        return curriculum
    

class Objetivo(models.Model):
    curriculum = models.ForeignKey(Curriculum)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.PositiveIntegerField(null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:objetivo_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        return ObjetivoEditForm(instance=self)

    def get_topicos(self):
        topico_list = Topico.objects.filter(objetivo_id = self.id).order_by('ordem')
        return topico_list

    def copy(self):
        objetivo = Objetivo.objects.create(curriculum=self.curriculum, titulo=self.titulo, descricao=self.descricao, ordem=self.ordem, autor=self.autor)
        topicos_list = Topico.objects.filter(objetivo=self)
        for topico in topicos_list :
            novo_topico = topico.copy()
            novo_topico.objetivo = objetivo
            novo_topico.save()
        return objetivo


class ObjetivoEditForm(ModelForm):
    class Meta:
        model = Objetivo
        fields = ['titulo', 'descricao', 'ordem']


class Topico(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    topicoPai = models.ForeignKey('self', null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    ordem = models.PositiveIntegerField(null=True, blank=True)
    suportes = models.ManyToManyField(Suporte, through='TopicoSuporte', null=True, blank=True)
    atividades = models.ManyToManyField(Atividade, through='TopicoAtividade', null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.titulo

    def get_absolute_url(self):
        return reverse('mathema:topico_edit', kwargs={'pk': self.pk})

    def get_edit_form(self):
        curriculum = self.objetivo.curriculum
        objetivo_list = Objetivo.objects.filter(curriculum=curriculum)
        
        form = TopicoEditForm(instance=self)
        form.fields["topicoPai"].queryset = Topico.objects.filter(objetivo__in=objetivo_list).exclude(id=self.id)
        return form

    def get_atividades(self):
        tas = TopicoAtividade.objects.filter(topico_id = self.id).order_by('ordem')
        atividades = []
        for ta in tas:
            atividades.extend(list(Atividade.objects.filter(id=ta.atividade_id)))
        return atividades

    def add_minhas_atividades(self):
        return list(set(list(Atividade.objects.filter(autor=self.autor))) - set(self.get_atividades()))
    
    def add_outras_atividades(self):
        return list(set(list(Atividade.objects.exclude(autor=self.autor))) - set(self.get_atividades()))

    def get_suportes(self):
        tss = TopicoSuporte.objects.filter(topico_id = self.id).order_by('ordem')
        suportes = []
        for ts in tss:
            suportes. extend(list(Suporte.objects.filter(id=ts.suporte_id)))
        return suportes

    def add_meus_suportes(self):
        return list(set(list(Suporte.objects.filter(autor=self.autor))) - set(self.get_suportes()))
    
    def add_outros_suportes(self):
        return list(set(list(Suporte.objects.exclude(autor=self.autor))) - set(self.get_suportes()))

    def copy(self):
        topico = Topico.objects.create(objetivo=self.objetivo, topicoPai=self.topicoPai, titulo=self.titulo, descricao=self.descricao, ordem=self.ordem, autor=self.autor)
        # copia das atividades
        for atividade in self.get_atividades() :
            nova_atividade = atividade.copy()
            nova_atividade.topico = topico
            nova_atividade.save()
            
            TopicoAtividade.objects.create(topico=topico, atividade=nova_atividade)
        # copia dos suportes
        for suporte in self.get_suportes() :
            novo_suporte = suporte.copy()
            novo_suporte.topico = topico
            novo_suporte.save()
            
            TopicoSuporte.objects.create(topico=topico, suporte=novo_suporte)
        return topico

class TopicoEditForm(ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'descricao', 'ordem', 'topicoPai']
        

class TopicoAtividade(models.Model):
    topico = models.ForeignKey(Topico)
    atividade = models.ForeignKey(Atividade)
    ordem = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.topico.titulo + " possui " + self.atividade.titulo

class TopicoAtividadeEditForm(ModelForm):
    class Meta:
        model = TopicoAtividade
        fields = ['ordem']

class TopicoSuporte(models.Model):
    topico = models.ForeignKey(Topico)
    suporte = models.ForeignKey(Suporte)
    ordem = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.topico.titulo + " possui " + self.suporte.titulo + " (" + self.suporte.tipo.nome + ") "

class TopicoSuporteEditForm(ModelForm):
    class Meta:
        model = TopicoSuporte
        fields = ['ordem']
