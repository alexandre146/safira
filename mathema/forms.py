# -*- coding: utf-8 -*-
from django.forms import ModelForm

from mathema.models import Suporte, Atividade, Topico, Objetivo, TopicoAtividade,\
    TopicoSuporte

class SuporteForm(ModelForm):
    class Meta:
        model = Suporte
        fields = ['titulo', 'tipo', 'arquivo', 'link']
        

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'suportes']


class TopicoForm(ModelForm):
    class Meta:
        model = Topico
        fields = ['objetivo', 'titulo', 'descricao', 'ordem', 'topicoPai', 'suportes']
        
        
class TopicoAtividadeForm(ModelForm):
    class Meta:
        model = TopicoAtividade
        fields = ['topico', 'atividade', 'ordem']


class ObjetivoForm(ModelForm):
    class Meta:
        model = Objetivo
        fields = ['titulo', 'descricao', 'ordem']
        
        
class TopicoSuporteForm(ModelForm):
    class Meta:
        model = TopicoSuporte
        fields = ['topico', 'suporte', 'ordem']

