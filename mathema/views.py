# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404

from mathema.models import Suporte, Atividade, Topico, Objetivo, TopicoAtividade
from mathema.forms import SuporteForm, AtividadeForm, TopicoForm, ObjetivoForm, TopicoAtividadeForm

## Suporte
def suporte_list(request, template_name='mathema/suporte_list.html'):
    suportes = Suporte.objects.all().order_by('titulo')
    data = {}
    data['object_list'] = suportes
    return render(request, template_name, data)


def suporte_create(request, template_name='mathema/suporte_form.html'):
    form = SuporteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mathema:suporte_list')
    return render(request, template_name, {'form':form})


def suporte_update(request, pk,
    template_name='mathema/suporte_form.html'):
    server = get_object_or_404(Suporte, pk=pk)
    form = SuporteForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('mathema:suporte_list')
    return render(request, template_name, {'form':form})


def suporte_delete(request, pk,
    template_name='mathema/suporte_confirm_delete.html'):
    suporte = get_object_or_404(Suporte, pk=pk)
    if request.method=='POST':
        suporte.delete()
        return redirect('mathema:suporte_list')
    return render(request, template_name, {'object':suporte})


## Atividade
def atividade_list(request, template_name='mathema/atividade_list.html'):
    atividades = Atividade.objects.all().order_by('titulo')
    data = {}
    data['object_list'] = atividades
    return render(request, template_name, data)


def atividade_create(request, template_name='mathema/atividade_form.html'):
    form = AtividadeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mathema:atividade_list')
    return render(request, template_name, {'form':form})


def atividade_update(request, pk,
    template_name='mathema/atividade_form.html'):
    server = get_object_or_404(Atividade, pk=pk)
    form = AtividadeForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('mathema:atividade_list')
    return render(request, template_name, {'form':form})


def atividade_delete(request, pk,
    template_name='mathema/atividade_confirm_delete.html'):
    atividade = get_object_or_404(Atividade, pk=pk)
    if request.method=='POST':
        atividade.delete()
        return redirect('mathema:atividade_list')
    return render(request, template_name, {'object':atividade})


## Topico
def topico_list(request, template_name='mathema/topico_list.html'):
    topicos = Topico.objects.all().order_by('ordem', 'titulo')
    data = {}
    data['object_list'] = topicos
    return render(request, template_name, data)


def topico_create(request, template_name='mathema/topico_form.html'):
    form = TopicoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mathema:topico_list')
    return render(request, template_name, {'form':form})


def topico_update(request, pk,
    template_name='mathema/topico_form.html'):
    server = get_object_or_404(Topico, pk=pk)
    form = TopicoForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('mathema:topico_list')
    return render(request, template_name, {'form':form})


def topico_delete(request, pk,
    template_name='mathema/topico_confirm_delete.html'):
    topico = get_object_or_404(Topico, pk=pk)
    if request.method=='POST':
        topico.delete()
        return redirect('mathema:topico_list')
    return render(request, template_name, {'object':topico})

## Topico Atividade
def topico_atividade_list(request, template_name='mathema/topico_atividade_list.html'):
    topicos_atividades = TopicoAtividade.objects.all()
    data = {}
    data['object_list'] = topicos_atividades
    return render(request, template_name, data)


def topico_atividade_create(request, template_name='mathema/topico_atividade_form.html'):
    form = TopicoAtividadeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mathema:topico_atividade_list')
    return render(request, template_name, {'form':form})


def topico_atividade_update(request, pk,
    template_name='mathema/topico_atividade_form.html'):
    server = get_object_or_404(TopicoAtividade, pk=pk)
    form = TopicoAtividadeForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('mathema:topico_atividade_list')
    return render(request, template_name, {'form':form})


def topico_atividade_delete(request, pk,
    template_name='mathema/topico_atividade_confirm_delete.html'):
    topicoAtividade = get_object_or_404(Topico, pk=pk)
    if request.method=='POST':
        topicoAtividade.delete()
        return redirect('mathema:topico_atividade_list')
    return render(request, template_name, {'object':topicoAtividade})


## Objetivo
def objetivo_list(request, template_name='mathema/objetivo_list.html'):
    objetivos = Objetivo.objects.all().order_by('titulo')
    data = {}
    data['object_list'] = objetivos
    return render(request, template_name, data)


def objetivo_create(request, template_name='mathema/objetivo_form.html'):
    form = ObjetivoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mathema:objetivo_list')
    return render(request, template_name, {'form':form})


def objetivo_update(request, pk,
    template_name='mathema/objetivo_form.html'):
    server = get_object_or_404(Objetivo, pk=pk)
    form = ObjetivoForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('mathema:objetivo_list')
    return render(request, template_name, {'form':form})


def objetivo_delete(request, pk,
    template_name='mathema/objetivo_confirm_delete.html'):
    objetivo = get_object_or_404(Objetivo, pk=pk)
    if request.method=='POST':
        objetivo.delete()
        return redirect('mathema:objetivo_list')
    return render(request, template_name, {'object':objetivo})
