# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from mathema import views

urlpatterns = patterns('',
    url(r'^suporte/$', views.suporte_list, name='suporte_list'),
    url(r'^suporte/new$', views.suporte_create, name='suporte_new'),
    url(r'^suporte/edit/(?P<pk>\d+)$', views.suporte_update, name='suporte_edit'),
    url(r'^suporte/delete/(?P<pk>\d+)$', views.suporte_delete, name='suporte_delete'),
    url(r'^atividade/$', views.atividade_list, name='atividade_list'),
    url(r'^atividade/new$', views.atividade_create, name='atividade_new'),
    url(r'^atividade/edit/(?P<pk>\d+)$', views.atividade_update, name='atividade_edit'),
    url(r'^atividade/delete/(?P<pk>\d+)$', views.atividade_delete, name='atividade_delete'),
    url(r'^topico/$', views.topico_list, name='topico_list'),
    url(r'^topico/new$', views.topico_create, name='topico_new'),
    url(r'^topico/edit/(?P<pk>\d+)$', views.topico_update, name='topico_edit'),
    url(r'^topico/delete/(?P<pk>\d+)$', views.topico_delete, name='topico_delete'),
    url(r'^topicoatividade/$', views.topico_atividade_list, name='topico_atividade_list'),
    url(r'^topicoatividade/new$', views.topico_atividade_create, name='topico_atividade_new'),
    url(r'^topicoatividade/edit/(?P<pk>\d+)$', views.topico_atividade_update, name='topico_atividade_edit'),
    url(r'^topicoatividade/delete/(?P<pk>\d+)$', views.topico_atividade_delete, name='topico_atividade_delete'),
    url(r'^objetivo/$', views.objetivo_list, name='objetivo_list'),
    url(r'^objetivo/new$', views.objetivo_create, name='objetivo_new'),
    url(r'^objetivo/edit/(?P<pk>\d+)$', views.objetivo_update, name='objetivo_edit'),
    url(r'^objetivo/delete/(?P<pk>\d+)$', views.objetivo_delete, name='objetivo_delete'),
)
