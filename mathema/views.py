# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

import copy

from mathema.forms import SuporteForm, AtividadeForm, TopicoForm, ObjetivoForm, TopicoAtividadeForm, \
    CurriculumForm, TopicoSuporteForm, AtividadeSuporteForm
from mathema.models import Suporte, Atividade, Topico, Objetivo, TopicoAtividade, \
    Curriculum, TopicoSuporte, SuporteEditForm, AtividadeSuporte


def curriculum_edit(request, pk, template_name='mathema/curriculum_edit.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    curriculum_form = CurriculumForm(request.POST or None, instance=curriculum)
    
    objetivo_novo_form = ObjetivoForm(request.POST or None)
    objetivo_list = Objetivo.objects.filter(curriculum_id = curriculum.id).order_by('ordem')

    topico_novo_form = TopicoForm(request.POST or None)
    atividade_nova_form = AtividadeForm(request.POST or None)
    suporte_novo_form = SuporteForm(request.POST or None)

    topico_atividade_form = TopicoAtividadeForm(request.POST or None)
    topico_suporte_form = TopicoSuporteForm(request.POST or None)
    atividade_suporte_form = AtividadeSuporteForm(request.POST or None)

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
        if atividade_nova_form.is_valid() and topico_atividade_form.is_valid():
            atividade = atividade_nova_form.save(commit=False)
            atividade.save()
            
            topico = Topico.objects.get(pk=request.POST["id_topico"])

            topico_atividade = TopicoAtividade.objects.create(topico=topico, atividade=atividade)
            data = topico_atividade_form.cleaned_data
            topico_atividade.ordem = data['ordem']            
            topico_atividade.save()

            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_atividade' in request.POST and topico_atividade_form.is_valid:
        print("salvar_atividade")
        atividade = Atividade.objects.get(pk=request.POST["id"])
        atividade.titulo = request.POST["titulo"]
        atividade.descricao = request.POST["descricao"]
        atividade.save()
        
        topico = Topico.objects.get(pk=request.POST["id_topico"])

        topico_atividade = TopicoAtividade.objects.get(topico=topico, atividade=atividade)
        topico_atividade.ordem = request.POST["ordem"]
        topico_atividade.save()
        
        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'salvar_novo_suporte' in request.POST:
        print("salvar_novo_suporte")
        if suporte_novo_form.is_valid() and topico_suporte_form.is_valid():
            suporte = suporte_novo_form.save(commit=False)
            if 'arquivo' in request.FILES :
                suporte.arquivo = request.FILES['arquivo']
            suporte.save()
            
            topico = Topico.objects.get(pk=request.POST["id_topico"])

            topico_suporte = TopicoSuporte.objects.get(topico=topico, suporte=suporte)
            topico_suporte.ordem = request.POST["ordem"]
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
        if suporte_novo_form.is_valid() and atividade_suporte_form.is_valid():
            suporte = suporte_novo_form.save(commit=False)
            if 'arquivo' in request.FILES :
                suporte.arquivo = request.FILES['arquivo']
            suporte.save()
            
            atividade = Atividade.objects.get(pk=request.POST["id_atividade"])

            atividade_suporte = AtividadeSuporte.objects.create(atividade=atividade, suporte=suporte)
            data = atividade_suporte_form.cleaned_data
            atividade_suporte.ordem = data['ordem']
            atividade_suporte.save()

            return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'adicionar_suporte_atividade' in request.POST:
        print("adicionar_suporte_atividade")
        atividade = Atividade.objects.get(pk=request.POST["id_atividade"])

        if "id_meu_suporte_atividade" in request.POST :
            meu_suporte = Suporte.objects.get(pk=request.POST["id_meu_suporte_atividade"])
            novo_suporte = Suporte.objects.create(titulo=meu_suporte.titulo, tipo=meu_suporte.tipo, arquivo=meu_suporte.arquivo, link=meu_suporte.link, visualizacoes=0, autor=meu_suporte.autor)
            novo_suporte.save()
            
            atividade_suporte = AtividadeSuporte.objects.create(atividade=atividade, suporte=novo_suporte)
            atividade_suporte.save()

        if "id_outro_suporte_atividade" in request.POST :
            outro_suporte = Suporte.objects.get(pk=request.POST["id_outro_suporte_atividade"])
            novo_suporte = Suporte.objects.create(titulo=outro_suporte.titulo, tipo=outro_suporte.tipo, arquivo=outro_suporte.arquivo, link=outro_suporte.link, visualizacoes=0, autor=outro_suporte.autor)
            novo_suporte.save()

            atividade_suporte = AtividadeSuporte.objects.create(atividade=atividade, suporte=novo_suporte)
            atividade_suporte.save()

        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'adicionar_atividade' in request.POST:
        print("adicionar_atividade")
        topico = Topico.objects.get(pk=request.POST["id_topico"])

        if "id_minha_atividade" in request.POST :
            minha_atividade = Atividade.objects.get(pk=request.POST["id_minha_atividade"])
            nova_atividade = Atividade.objects.create(titulo=minha_atividade.titulo, descricao=minha_atividade.descricao, autor=minha_atividade.autor)
            
            for suporte in minha_atividade.get_suportes() :
                novo_suporte = Suporte.objects.create(titulo=suporte.titulo, tipo=suporte.tipo, arquivo=suporte.arquivo, link=suporte.link, visualizacoes=0, autor=suporte.autor)
                novo_suporte.save()
                
                atividade_suporte = AtividadeSuporte.objects.create(atividade=nova_atividade, suporte=novo_suporte)
                atividade_suporte.save()
                
            nova_atividade.save()

            topico_atividade = TopicoAtividade.objects.create(topico=topico, atividade=nova_atividade)
            topico_atividade.save()

        if "id_outra_atividade" in request.POST :
            outra_atividade = Atividade.objects.get(pk=request.POST["id_outra_atividade"])
            nova_atividade = Atividade.objects.create(titulo=outra_atividade.titulo, descricao=outra_atividade.descricao, autor=outra_atividade.autor)

            for suporte in outra_atividade.get_suportes() :
                novo_suporte = Suporte.objects.create(titulo=suporte.titulo, tipo=suporte.tipo, arquivo=suporte.arquivo, link=suporte.link, visualizacoes=0, autor=suporte.autor)
                novo_suporte.save()
                
                atividade_suporte = AtividadeSuporte.objects.create(atividade=nova_atividade, suporte=novo_suporte)
                atividade_suporte.save()

            nova_atividade.save()

            topico_atividade = TopicoAtividade.objects.create(topico=topico, atividade=nova_atividade)
            topico_atividade.save()

        return redirect('mathema:curriculum_edit', pk=pk)
    elif request.method=='POST' and 'adicionar_suporte' in request.POST:
        print("adicionar_suporte")
        topico = Topico.objects.get(pk=request.POST["id_topico"])

        if "id_meu_suporte" in request.POST :
            meu_suporte = Suporte.objects.get(pk=request.POST["id_meu_suporte"])
            novo_suporte = Suporte.objects.create(titulo=meu_suporte.titulo, tipo=meu_suporte.tipo, arquivo=meu_suporte.arquivo, link=meu_suporte.link, visualizacoes=0, autor=meu_suporte.autor)
            novo_suporte.save()
            
            topico_suporte = TopicoSuporte.objects.create(topico=topico, suporte=novo_suporte)
            topico_suporte.save()

        if "id_outro_suporte" in request.POST :
            outro_suporte = Suporte.objects.get(pk=request.POST["id_outro_suporte"])
            novo_suporte = Suporte.objects.create(titulo=outro_suporte.titulo, tipo=outro_suporte.tipo, arquivo=outro_suporte.arquivo, link=outro_suporte.link, visualizacoes=0, autor=outro_suporte.autor)
            novo_suporte.save()

            topico_suporte = TopicoSuporte.objects.create(topico=topico, suporte=novo_suporte)
            topico_suporte.save()

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
    
    data['topico_atividade_form'] = topico_atividade_form
    data['topico_suporte_form'] = topico_suporte_form
    data['atividade_suporte_form'] = atividade_suporte_form

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


def curriculum_objetivo_delete(request, pk1, pk2, template_name='mathema/curriculum_objetivo_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    objetivo = get_object_or_404(Objetivo, pk=pk2)

    if request.method=='POST':
        objetivo.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    data['objetivo'] = objetivo
    return render(request, template_name, data)


def curriculum_topico_delete(request, pk1, pk2, template_name='mathema/curriculum_topico_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    topico = get_object_or_404(Topico, pk=pk2)

    if request.method=='POST':
        topico.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    data['topico'] = topico
    return render(request, template_name, data)


def curriculum_atividade_delete(request, pk1, pk2, pk3, template_name='mathema/curriculum_atividade_confirm_delete.html'):
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
    data['atividade'] = atividade
    return render(request, template_name, data) 


def curriculum_suporte_delete(request, pk1, pk2, pk3, template_name='mathema/curriculum_suporte_confirm_delete.html'):
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
    data['suporte'] = suporte
    return render(request, template_name, data)


def curriculum_suporte_atividade_delete(request, pk1, pk2, pk3, template_name='mathema/curriculum_suporte_confirm_delete.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    atividade = get_object_or_404(Atividade, pk=pk2)
    suporte = get_object_or_404(Suporte, pk=pk3)
    
    atividade_suporte = AtividadeSuporte.objects.get(atividade=atividade, suporte=suporte)

    if request.method=='POST':
        atividade_suporte.delete()
        suporte.delete()
        return redirect('mathema:curriculum_edit', pk=pk1)

    data = {}
    data['curriculum'] = curriculum
    data['suporte'] = suporte
    return render(request, template_name, data)


def suporte_list(request, template_name='mathema/suporte_list.html'):
    suportes_list = Suporte.objects.all().order_by('titulo')
    suporte_form = SuporteForm(request.POST or None, request.FILES or None)
    
    if suporte_form.is_valid():
        suporte_form.save()
        return redirect('mathema:suporte_list')
    
    data = {}
    data['suporte_form'] = suporte_form
    data['suportes_list'] = suportes_list
    return render(request, template_name, data)


def suporte_edit(request, pk, template_name='mathema/suporte_edit.html'):
    suporte = get_object_or_404(Suporte, pk=pk)
    suporte_form = SuporteForm(request.POST or None, request.FILES or None, instance=suporte)

    if suporte_form.is_valid():
        suporte_form.save()
        return redirect('mathema:suporte_list')

    data = {}
    data['suporte_form'] = suporte_form
    data['suporte'] = suporte
    return render(request, template_name, data)


def suporte_delete(request, pk, template_name='mathema/suporte_confirm_delete.html'):
    suporte = get_object_or_404(Suporte, pk=pk)

    if request.method=='POST':
        suporte.delete()
        return redirect('mathema:suporte_list')

    data = {}
    data['suporte'] = suporte
    return render(request, template_name, data)

