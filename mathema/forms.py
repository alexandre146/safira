# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from mathema.models import Suporte, Atividade, Topico, Objetivo, TopicoAtividade,\
    TopicoSuporte, Curriculum, AtividadeSuporte

class SuporteForm(ModelForm):
    class Meta:
        model = Suporte
        fields = ['titulo', 'tipo', 'arquivo', 'link']
        

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao']


class AtividadeSuporteForm(ModelForm):
    class Meta:
        model = AtividadeSuporte
        fields = ['ordem']

class TopicoForm(ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'descricao', 'ordem', 'topicoPai']
        
        
class TopicoAtividadeForm(ModelForm):
    class Meta:
        model = TopicoAtividade
        fields = ['ordem']


class ObjetivoForm(ModelForm):
    class Meta:
        model = Objetivo
        fields = ['titulo', 'descricao', 'ordem']
        
        
class TopicoSuporteForm(ModelForm):
    class Meta:
        model = TopicoSuporte
        fields = ['ordem']


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ['titulo', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
