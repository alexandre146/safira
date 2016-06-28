# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from mathema import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^sair/$', views.sair, name='sair'),
    url(r'^curriculum/list', views.curriculum_list, name='curriculum_list'),
    url(r'^curriculum/(?P<pk>\d+)/edit', views.curriculum_edit, name='curriculum_edit'),
    url(r'^curriculum/(?P<pk>\d+)/delete', views.curriculum_delete, name='curriculum_delete'),
    
    url(r'^curriculum/(?P<pk1>\d+)/objetivo/(?P<pk2>\d+)/delete$', views.curriculum_objetivo_delete, name='curriculum_objetivo_delete'),
    url(r'^curriculum/(?P<pk1>\d+)/topico/(?P<pk2>\d+)/delete$', views.curriculum_topico_delete, name='curriculum_topico_delete'),
    url(r'^curriculum/(?P<pk1>\d+)/topico/(?P<pk2>\d+)/atividade/(?P<pk3>\d+)/delete$', views.curriculum_atividade_delete, name='curriculum_atividade_delete'),
    url(r'^curriculum/(?P<pk1>\d+)/topico/(?P<pk2>\d+)/suporte/(?P<pk3>\d+)/delete$', views.curriculum_suporte_delete, name='curriculum_suporte_delete'),
    
    url(r'^curriculum/(?P<pk1>\d+)/atividade/(?P<pk2>\d+)/suporte/(?P<pk3>\d+)/delete$', views.curriculum_suporte_atividade_delete, name='curriculum_suporte_atividade_delete'),   
    
    url(r'^suporte/list$', views.suporte_list, name='suporte_list'),
    url(r'^suporte/(?P<pk>\d+)/edit$', views.suporte_edit, name='suporte_edit'),
    url(r'^suporte/(?P<pk>\d+)/delete$', views.suporte_delete, name='suporte_delete'),
)
