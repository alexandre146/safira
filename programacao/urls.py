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
    url(r'^aluno/cursos/$', views.aluno_curso_list, name='aluno_curso_list'),
    url(r'^aluno/meus_cursos/$', views.aluno_meus_cursos, name='aluno_meus_cursos'),
    url(r'^aluno/curso/inscrever/(?P<pk>\d+)/$', views.aluno_curso_inscrever, name='aluno_curso_inscrever'),
    url(r'^aluno/curso/desinscrever/(?P<pk>\d+)/$', views.aluno_curso_desinscrever, name='aluno_curso_desinscrever'),
    url(r'^aluno/curso/(?P<pk>\d+)/$', views.aluno_curso, name='aluno_curso'),
    url(r'^aluno/atividade/(?P<pk>\d+)/$', views.aluno_atividade, name='aluno_atividade'),
    url(r'^aluno/atividade/exercicio/(?P<pk>\d+)/$', views.aluno_atividade_exercicio_submissao, name='aluno_atividade_exercicio_submissao'),

    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/edit/$', views.professor_edit, name='professor_edit'),
    url(r'^professor/meus_cursos/$', views.professor_meus_cursos, name='professor_meus_cursos'),
    url(r'^professor/minhas_atividades/$', views.professor_minhas_atividades, name='professor_minhas_atividades'),
    url(r'^professor/minhas_intervencoes/$', views.professor_minhas_intervencoes, name='professor_minhas_intervencoes'),
    url(r'^professor/professor_quadro_notas/$', views.professor_quadro_notas, name='professor_quadro_notas'),
    url(r'^professor/professor_comentarios/$', views.professor_comentarios, name='professor_comentarios'),
    url(r'^professor/curso/edit/(?P<pk>\d+)/$', views.professor_curso_edit, name='professor_curso_edit'),
    url(r'^professor/curso/delete/(?P<pk>\d+)/$', views.professor_curso_delete, name='professor_curso_delete'),
    url(r'^professor/curso/alunos$', views.professor_curso_alunos, name='professor_curso_alunos'),

    url(r'^professor/curso/(?P<pk>\d+)/curriculum/list', views.professor_curso_curriculum_list, name='professor_curso_curriculum_list'),
    url(r'^professor/curso/(?P<pk1>\d+)/curriculum/(?P<pk2>\d+)/view', views.professor_curso_curriculum_view, name='professor_curso_curriculum_view'),
    url(r'^professor/curso/(?P<pk1>\d+)/curriculum/(?P<pk2>\d+)/associar', views.professor_curso_associar_curriculum, name='professor_curso_associar_curriculum'),
#     url(r'^professor/curso/(?P<pk1>\d+)/curriculum/(?P<pk2>\d+)/edit', views.professor_curso_curriculum_edit, name='professor_curso_curriculum_edit'),
    url(r'^professor/curso/(?P<pk1>\d+)/curriculum/(?P<pk2>\d+)/delete', views.professor_curso_curriculum_delete, name='professor_curso_curriculum_delete'),

    url(r'^professor/atividade/exercicio/delete/(?P<pk>\d+)/$', views.professor_atividade_exercicio_delete, name='professor_atividade_exercicio_delete'),

    url(r'^professor/curso/(?P<pk1>\d+)/atividade/(?P<pk2>\d+)/exercicio/$', views.professor_curso_atividade_exercicio, name='professor_curso_atividade_exercicio'),
    url(r'^professor/curso/(?P<pk1>\d+)/atividade/exercicio/edit/(?P<pk2>\d+)/$', views.professor_curso_atividade_exercicio_edit, name='professor_curso_atividade_exercicio_edit'),
    url(r'^professor/curso/(?P<pk1>\d+)/atividade/exercicio/(?P<pk2>\d+)/view/$', views.professor_curso_atividade_exercicio_view, name='professor_curso_atividade_exercicio_view'),
    
    url(r'^professor/curso/curriculum/(?P<pk1>\d+)/atividade/exercicio/(?P<pk2>\d+)/avaliacoes/$', views.professor_curso_atividade_exercicio_avaliacoes, name='professor_curso_atividade_exercicio_avaliacoes'),

)
