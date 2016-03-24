# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput

from programacao.models import Aluno, Professor, Curso, AlunoCurso,\
    ObjetivoProgramacao, TopicoProgramacao, AtividadeProgramacao,\
    ExercicioPratico, AlunoSubmissaoExercicioPratico, Curriculum, Interacao
from mathema.models import TopicoAtividade, Suporte

class RegistroForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(), label="Login")
    email = forms.EmailField(widget=forms.TextInput(), label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmação de senha")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Senhas não são iguais. Insira os dados novamente.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(), label="Login")
    email = forms.EmailField(widget=forms.TextInput(), label="Email")

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome']


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ['nome']
        

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo']


class CursoEditForm(ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo']


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ['titulo', 'descricao']


class CurriculumObjetivoForm(ModelForm):
    class Meta:
        model = ObjetivoProgramacao
        fields = ['titulo', 'descricao', 'ordem']


class CursoObjetivoForm(ModelForm):
    class Meta:
        model = ObjetivoProgramacao
        fields = ['curriculum', 'titulo', 'descricao', 'ordem']


class CursoTopicoForm(ModelForm):
    class Meta:
        model = TopicoProgramacao
        fields = ['objetivo', 'titulo', 'descricao', 'ordem', 'topicoPai']


class CursoAtividadeForm(ModelForm):
    class Meta:
        model = AtividadeProgramacao
        fields = ['titulo', 'descricao', 'deadline', 'suportes']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime'}),
        }


class CursoTopicoAtividadeForm(ModelForm):
    class Meta:
        model = TopicoAtividade
        fields = ['topico', 'atividade', 'ordem']


class CursoSuporteForm(ModelForm):
    class Meta:
        model = Suporte
        fields = ['titulo', 'tipo', 'arquivo', 'link']


class ExercicioForm(ModelForm):
    class Meta:
        model = ExercicioPratico
        fields = ['enunciado', 'arquivoTeste', 'arquivoSolucao']


class AlunoSubmissaoExercicioPraticoForm(ModelForm):
    class Meta:
        model = AlunoSubmissaoExercicioPratico
        fields = ['arquivo']
        

class InteracaoForm(ModelForm):
    class Meta:
        model = Interacao
        fields = ['titulo', 'ordem']

        
# class AlunoDisciplinaForm(ModelForm):
#     class Meta:
#         model = AlunoDisciplina
#         fields = ['aluno', 'disciplina']