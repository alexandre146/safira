# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404

from mathema.models import Suporte, Atividade, Topico, Objetivo, TopicoAtividade,\
    Curriculum, TopicoSuporte, TipoSuporte, SuporteEditForm, AtividadeSuporte
from mathema.forms import SuporteForm, AtividadeForm, TopicoForm, ObjetivoForm, TopicoAtividadeForm,\
    CurriculumForm

def curriculum_edit(request, pk, template_name='mathema/curriculum_edit.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    curriculum_form = CurriculumForm(request.POST or None, instance=curriculum)
    
    objetivo_novo_form = ObjetivoForm(request.POST or None)
    objetivo_list = Objetivo.objects.filter(curriculum_id = curriculum.id)

    topico_novo_form = TopicoForm(request.POST or None)
    atividade_nova_form = AtividadeForm(request.POST or None)
    suporte_novo_form = SuporteForm(request.POST or None)

    if request.method=='POST' and 'salvar_curriculum' in request.POST:
        print("salvar_curriculum")
        if curriculum_form.is_valid():
            curriculum_form.save()
            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_novo_objetivo' in request.POST:
        print("salvar_novo_objetivo")
        if objetivo_novo_form.is_valid():
            objetivo = objetivo_novo_form.save(commit=False)
            objetivo.curriculum = curriculum
            objetivo.save()
            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_objetivo' in request.POST:
        print("salvar_objetivo")
        objetivo = Objetivo.objects.get(pk=request.POST["id"])
        objetivo.titulo = request.POST["titulo"]
        objetivo.descricao = request.POST["descricao"]
        objetivo.ordem = request.POST["ordem"]
        objetivo.curriculum = curriculum
        objetivo.save()
        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_novo_topico' in request.POST:
        print("salvar_novo_topico")
        if topico_novo_form.is_valid():
            topico = topico_novo_form.save(commit=False)
            topico.objetivo = Objetivo.objects.get(pk=request.POST["id_objetivo"])
            topico.save()
            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_topico' in request.POST:
        print("salvar_topico")
        topico = Topico.objects.get(pk=request.POST["id"])
        topico.titulo = request.POST["titulo"]
        topico.descricao = request.POST["descricao"]
        topico.ordem = request.POST["ordem"]
        if request.POST.get("topico_pai") :
            topico.topico_pai = request.POST.get("topico_pai")
        topico.save()
        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_nova_atividade' in request.POST:
        print("salvar_nova_atividade")
        if atividade_nova_form.is_valid():
            atividade = atividade_nova_form.save(commit=False)
            atividade.save()
            
            topico = Topico.objects.get(pk=request.POST["id_topico"])

            topico_atividade = TopicoAtividade.objects.create(topico=topico, atividade=atividade)
            topico_atividade.save()

            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_atividade' in request.POST:
        print("salvar_atividade")
        atividade = Atividade.objects.get(pk=request.POST["id"])
        atividade.titulo = request.POST["titulo"]
        atividade.descricao = request.POST["descricao"]
        if request.POST.get("suportes") :
            atividade.suportes = request.POST.get("suportes")
        atividade.save()
        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_novo_suporte' in request.POST:
        print("salvar_novo_suporte")
        if suporte_novo_form.is_valid():
            suporte = suporte_novo_form.save(commit=False)
            suporte.save()
            
            topico = Topico.objects.get(pk=request.POST["id_topico"])

            topico_suporte = TopicoSuporte.objects.create(topico=topico, suporte=suporte)
            topico_suporte.save()

            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_suporte' in request.POST:
        print("salvar_suporte")
        suporte = Suporte.objects.get(pk=request.POST["id"]) #get_object_or_404(Location, pk=pk)
        suporte_form = SuporteEditForm(request.POST or None, request.FILES or None, instance=suporte)

        if suporte_form.is_valid():
            suporte_form.save()
            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_novo_suporte_atividade' in request.POST:
        print("salvar_novo_suporte_atividade")
        if suporte_novo_form.is_valid():
            suporte = suporte_novo_form.save(commit=False)
            suporte.save()
            
            atividade = Atividade.objects.get(pk=request.POST["id_atividade"])

            atividade_suporte = AtividadeSuporte.objects.create(atividade=atividade, suporte=suporte)
            atividade_suporte.save()

            return redirect('mathema:curriculum_edit', pk=pk)
    else:
        print('do nothing!')

    data = {}
    data['curriculum'] = curriculum
    data['curriculum_form'] = curriculum_form

    data['objetivo_novo_form'] = objetivo_novo_form
    data['objetivo_list'] = objetivo_list

    data['topico_novo_form'] = topico_novo_form
    data['atividade_nova_form'] = atividade_nova_form
    data['suporte_novo_form'] = suporte_novo_form

    return render(request, template_name, data)


def curriculum_list(request, template_name='mathema/curriculum_list.html'):
    curriculum_list = Curriculum.objects.all()
    curriculum_form = CurriculumForm(request.POST or None)
    
    if request.method=='POST':
        if curriculum_form.is_valid():
            curriculum = curriculum_form.save(commit=False)
            curriculum.dataCriacao = datetime.now()
            curriculum.save()
            return redirect('mathema:curriculum_list')
        else:
            curriculum_form = CurriculumForm()

    data = {}
    data['curriculum_form'] = curriculum_form
    data['curriculum_list'] = curriculum_list
    return render(request, template_name, data)


def curriculum_delete(request, pk, template_name='mathema/curriculum_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk)

    if request.method=='POST':
        curriculum.delete()
        return redirect('mathema:curriculum_list')

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def objetivo_delete(request, pk1, pk2, template_name='mathema/objetivo_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    objetivo = get_object_or_404(Objetivo, pk=pk2)

    if request.method=='POST':
        objetivo.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def topico_delete(request, pk1, pk2, template_name='mathema/topico_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    topico = get_object_or_404(Topico, pk=pk2)

    if request.method=='POST':
        topico.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def atividade_delete(request, pk1, pk2, pk3, template_name='mathema/atividade_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    topico = get_object_or_404(Topico, pk=pk2)
    atividade = get_object_or_404(Atividade, pk=pk3)
    
    topico_atividade = TopicoAtividade.objects.get(topico=topico, atividade=atividade)

    if request.method=='POST':
        topico_atividade.delete()
        atividade.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data) 


def suporte_delete(request, pk1, pk2, pk3, template_name='mathema/suporte_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    topico = get_object_or_404(Topico, pk=pk2)
    suporte = get_object_or_404(Suporte, pk=pk3)
    
    topico_suporte = TopicoSuporte.objects.get(topico=topico, suporte=suporte)

    if request.method=='POST':
        topico_suporte.delete()
        suporte.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def suporte_atividade_delete(request, pk1, pk2, pk3, template_name='mathema/suporte_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    atividade = get_object_or_404(Atividade, pk=pk2)
    suporte = get_object_or_404(Suporte, pk=pk3)
    
#     atividade_suporte = AtividadeSuporte.objects.get(atividade=atividade, suporte=suporte)

    if request.method=='POST':
#         atividade_suporte.delete()
        suporte.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def suporte_list(request, template_name='mathema/suporte_list.html'):
    suportes = Suporte.objects.all().order_by('titulo')
    data = {}
    data['object_list'] = suportes
    return render(request, template_name, data)