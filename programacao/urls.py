# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from programacao import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^sair/$', views.sair, name='sair'),
    url(r'^aluno/$', views.aluno_index, name='aluno_index'),
    url(r'^aluno/edit/$', views.aluno_edit, name='aluno_edit'),
    url(r'^aluno/disciplinas/$', views.aluno_disciplina_list, name='aluno_disciplina_list'),
    url(r'^aluno/minhas_disciplinas/$', views.aluno_minhas_disciplinas, name='aluno_minhas_disciplinas'),
    url(r'^aluno/disciplina/inscrever/(?P<pk>\d+)/$', views.aluno_disciplina_inscrever, name='aluno_disciplina_inscrever'),
    url(r'^aluno/disciplina/desinscrever/(?P<pk>\d+)/$', views.aluno_disciplina_desinscrever, name='aluno_disciplina_desinscrever'),
    url(r'^aluno/disciplina/(?P<pk>\d+)/$', views.aluno_disciplina, name='aluno_disciplina'),
    url(r'^aluno/atividade/(?P<pk>\d+)/$', views.aluno_atividade, name='aluno_atividade'),
    url(r'^aluno/atividade/exercicio/(?P<pk>\d+)/$', views.aluno_atividade_exercicio_submissao, name='aluno_atividade_exercicio_submissao'),
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/edit/$', views.professor_edit, name='professor_edit'),
    url(r'^professor/minhas_disciplinas/$', views.professor_minhas_disciplinas, name='professor_minhas_disciplinas'),
    url(r'^professor/minhas_atividades/$', views.professor_minhas_atividades, name='professor_minhas_atividades'),
    url(r'^professor/minhas_intervencoes/$', views.professor_minhas_intervencoes, name='professor_minhas_intervencoes'),
    url(r'^professor/professor_quadro_notas/$', views.professor_quadro_notas, name='professor_quadro_notas'),
    url(r'^professor/professor_comentarios/$', views.professor_comentarios, name='professor_comentarios'),
    url(r'^professor/disciplina/edit/(?P<pk>\d+)/$', views.professor_disciplina_edit, name='professor_disciplina_edit'),
    url(r'^professor/disciplina/delete/(?P<pk>\d+)/$', views.professor_disciplina_delete, name='professor_disciplina_delete'),
    url(r'^professor/disciplina/alunos$', views.professor_disciplina_alunos, name='professor_disciplina_alunos'),
    url(r'^professor/disciplina/objetivo/$', views.professor_disciplina_objetivo, name='professor_disciplina_objetivo'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/objetivo/edit/(?P<pk2>\d+)/$', views.professor_disciplina_objetivo_edit, name='professor_disciplina_objetivo_edit'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/objetivo/delete/(?P<pk2>\d+)/$', views.professor_disciplina_objetivo_delete, name='professor_disciplina_objetivo_delete'),
    url(r'^professor/disciplina/topico/$', views.professor_disciplina_topico, name='professor_disciplina_topico'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/topico/edit/(?P<pk2>\d+)/$', views.professor_disciplina_topico_edit, name='professor_disciplina_topico_edit'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/topico/delete/(?P<pk2>\d+)/$', views.professor_disciplina_topico_delete, name='professor_disciplina_topico_delete'),
    url(r'^professor/disciplina/atividade/$', views.professor_disciplina_atividade, name='professor_disciplina_atividade'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/edit/(?P<pk2>\d+)/$', views.professor_disciplina_atividade_edit, name='professor_disciplina_atividade_edit'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/delete/(?P<pk2>\d+)/$', views.professor_disciplina_atividade_delete, name='professor_disciplina_atividade_delete'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/(?P<pk>\d+)/exercicio/$', views.professor_disciplina_atividade_exercicio, name='professor_disciplina_atividade_exercicio'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/exercicio/edit/(?P<pk2>\d+)/$', views.professor_disciplina_atividade_exercicio_edit, name='professor_disciplina_atividade_exercicio_edit'),    
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/exercicio/delete/(?P<pk2>\d+)/$', views.professor_disciplina_atividade_exercicio_delete, name='professor_disciplina_atividade_exercicio_delete'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/atividade/exercicio/(?P<pk2>\d+)/testes/$', views.professor_disciplina_atividade_exercicio_testes, name='professor_disciplina_atividade_exercicio_testes'),
    url(r'^professor/disciplina/suporte/$', views.professor_disciplina_suporte, name='professor_disciplina_suporte'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/suporte/edit/(?P<pk2>\d+)/$', views.professor_disciplina_suporte_edit, name='professor_disciplina_suporte_edit'),
    url(r'^professor/disciplina/(?P<pk1>\d+)/suporte/delete/(?P<pk2>\d+)/$', views.professor_disciplina_suporte_delete, name='professor_disciplina_suporte_delete'),
    url(r'^professor/disciplina/topico_atividade/$', views.professor_disciplina_topico_atividade, name='professor_disciplina_topico_atividade'),
)