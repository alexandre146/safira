# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
import os
import subprocess

from mathema.forms import TopicoSuporteForm
from mathema.models import TopicoAtividade, Suporte
from programacao.forms import AlunoForm, ProfessorForm, CursoForm, RegistroForm, \
    UserEditForm, CursoEditForm, CursoObjetivoForm, \
    CursoTopicoForm, CursoAtividadeForm, CursoTopicoAtividadeForm, \
    CursoSuporteForm, ExercicioForm, AlunoSubmissaoExercicioPraticoForm, \
    CurriculumForm, CurriculumObjetivoForm, InteracaoForm
from programacao.models import Aluno, Professor, Curso, AlunoCurso, ObjetivoProgramacao, TopicoProgramacao, \
    AtividadeProgramacao, ExercicioPratico, AlunoSubmissaoExercicioPratico, \
    Curriculum, Interacao


def index(request, template_name='programacao/index.html'):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            u = form.get_user()
            login(request, u)
            if u.has_perm('programacao.view_professor'):
                return redirect(reverse(viewname='programacao:professor_index'))
            elif u.has_perm('programacao.view_aluno'):
                return redirect(reverse(viewname='programacao:aluno_index'))
        else: 
            messages.add_message(request, messages.ERROR, 'Usuário não cadastrado ou sem permissão de acesso!')

    form = AuthenticationForm()

    data = {}
    data['form'] = form
    return render(request, template_name, data)

def registro(request, template_name='programacao/registro.html'):
    if request.method == 'POST':
        aluno_form = AlunoForm(request.POST or None)
        user_form = RegistroForm(request.POST or None)
        if aluno_form.is_valid() and user_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.is_active = True
                user.save()
 
                aluno = aluno_form.save(commit=False)
                aluno.user = user
                aluno.save()

                permission = Permission.objects.get(name='view_aluno')
                user.user_permissions.add(permission)

                messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso!')
                return redirect('programacao:index')
        else:
            messages.add_message(request, messages.ERROR, 'Erro ao tentar cadastrar!') 

    aluno_form = AlunoForm()
    user_form = RegistroForm()

    data = {}
    data['aluno_form'] = aluno_form
    data['user_form'] = user_form
    return render(request, template_name, data)


def sair(request):
    logout(request)
    return redirect('programacao:index')


## Aluno
#@login_required() #@view_aluno()
def aluno_index(request, template_name='programacao/aluno_index.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    aluno_curso = AlunoCurso.objects.filter(aluno_id=aluno.id)
    
    curriculum = []
    for ad in aluno_curso :
        disc = Curso.objects.get(id=ad.curso_id)
        curriculum.extend(list(Curriculum.objects.get(id=disc.curriculum.id)))
    
    objetivos = []
    for c in curriculum :
        objetivos.extend(list(ObjetivoProgramacao.objects.filter(curriculum_id=c.id)))

    topicos = []
    for obj in objetivos :
        topicos.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))

    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
    
    data = {}
    data['atividades_list'] = atividades
    return render(request, template_name, data)


#@login_required() #@view_aluno()
def aluno_edit(request, template_name='programacao/aluno_edit.html'):
    user = request.user
    aluno = Aluno.objects.get(user_id=user.id)

    user_form = UserEditForm(request.POST or None, instance=user)
    aluno_form = AlunoForm(request.POST or None, instance=aluno)

    if aluno_form.is_valid() and user_form.is_valid():
        user_form.save()
        aluno_form.save()
        return redirect('programacao:aluno_edit')
    
    data = {}
    data['user_form'] = user_form
    data['aluno_form'] = aluno_form
    return render(request, template_name, data)


def aluno_curso_list(request, template_name='programacao/aluno_curso_list.html'):
    todos_cursos = Curso.objects.all()
    
    aluno = Aluno.objects.get(user_id=request.user.id)
    aluno_curso = AlunoCurso.objects.filter(aluno_id=aluno.id)
    meus_cursos = []
    for ad in aluno_curso :
        meus_cursos.extend(list(Curso.objects.filter(id=ad.curso_id)))

    cursos = set(todos_cursos).difference(set(meus_cursos))
    
    data = {}
    data['obj_list'] = cursos
    return render(request, template_name, data)

# @login_required()
def aluno_meus_cursos(request, template_name='programacao/aluno_meus_cursos.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    aluno_curso = AlunoCurso.objects.filter(aluno_id=aluno.id)
    meus_cursos = []
    for ad in aluno_curso :
        meus_cursos.extend(list(Curso.objects.filter(id=ad.curso_id)))

    meus_cursos = sorted(meus_cursos, key=lambda curso: curso.titulo)

    data = {}
    data['cursos_list'] = meus_cursos
    return render(request, template_name, data)


def aluno_curso_inscrever(request, pk, template_name='programacao/aluno_curso_list.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    curso = get_object_or_404(Curso, pk=pk)
    
    inscricao = AlunoCurso.objects.create(aluno=aluno, curso=curso)
    inscricao.save()
    
    return redirect('programacao:aluno_minhas_cursos')


def aluno_curso_desinscrever(request, pk, template_name='programacao/aluno_minhas_cursos.html'):
#     aluno = Aluno.objects.get(user_id=request.user.id)
    curso = get_object_or_404(Curso, pk=pk)
    
    inscricao = AlunoCurso.objects.get(curso=curso)
    inscricao.delete()

    return redirect('programacao:aluno_minhas_cursos')


def aluno_curso(request, pk, template_name='programacao/aluno_curso.html'):
    curso = get_object_or_404(Curso, pk=pk)

    objetivos = ObjetivoProgramacao.objects.filter(curriculum_id=curso.curriculum.id)

    topicos = []
    for obj in objetivos :
        topicos.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))

    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
    
    data = {}
    data['curso'] = curso
    data['atividades_list'] = atividades
    return render(request, template_name, data)


def aluno_atividade(request, pk, template_name='programacao/aluno_atividade.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk)
    exercicios = ExercicioPratico.objects.filter(atividade_id=atividade.id)
    aluno = Aluno.objects.get(user_id=request.user.id)
    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(autor=aluno)
    
    data = {}
    data['atividade'] = atividade
    data['exercicios_list'] = exercicios
    data['submissoes_list'] = submissoes
    return render(request, template_name, data)


def aluno_atividade_exercicio_submissao(request, pk, template_name='programacao/aluno_atividade_exercicio_submissao.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk)
    aluno= Aluno.objects.get(user_id=request.user.id)

    try:
        submissao = AlunoSubmissaoExercicioPratico.objects.get(autor=aluno, exercicio=exercicio)
        form = AlunoSubmissaoExercicioPraticoForm(request.POST or None, request.FILES or None, instance=submissao)
        if request.method == 'POST':
            if form.is_valid():
                submissao = form.save(commit=False)
                submissao.exercicio = exercicio
                submissao.autor = aluno
                submissao.dataEnvio = datetime.datetime.now()
                submissao.save()
                return redirect('programacao:aluno_atividade_exercicio_submissao', pk=pk)

        data = {}
        data['form'] = form
        data['exercicio'] = exercicio
        data['submissao'] = submissao
        return render(request, template_name, data)
    except:
        form = AlunoSubmissaoExercicioPraticoForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                submissao = form.save(commit=False)
                submissao.exercicio = exercicio
                submissao.autor = aluno
                submissao.dataEnvio = datetime.datetime.now()
                submissao.save()
                return redirect('programacao:aluno_atividade_exercicio_submissao', pk=pk)

        data = {}
        data['form'] = form
        data['exercicio'] = exercicio
        return render(request, template_name, data)



## Professor
# @login_required()
def professor_index(request, template_name='programacao/professor_index.html'):
    professor = Professor.objects.get(user_id=request.user.id)
    cursos = Curso.objects.filter(professor_id=professor.id)

    curriculum = []
    for d in cursos:
        curriculum.extend(list(Curriculum.objects.filter(id=d.curriculum_id)))
    
    objetivos = []
    for c in curriculum :
        objetivos.extend(list(ObjetivoProgramacao.objects.filter(curriculum_id=c.id)))

    topicos = []
    for obj in objetivos :
        topicos.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))

    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
    
    data = {}
    data['atividades_list'] = atividades
    return render(request, template_name, data)

# @login_required()
def professor_edit(request, template_name='programacao/professor_edit.html'):
    user = request.user
    professor = Professor.objects.get(user_id=user.id)

    user_form = UserEditForm(request.POST or None, instance=user)
    professor_form = ProfessorForm(request.POST or None, instance=professor)

    if professor_form.is_valid() and user_form.is_valid():
        user_form.save()
        professor_form.save()
        return redirect('programacao:professor_edit')
    
    data = {}
    data['user_form'] = user_form
    data['professor_form'] = professor_form
    return render(request, template_name, data)


# @login_required()
def professor_meus_cursos(request, template_name='programacao/professor_meus_cursos.html'):
    professor = Professor.objects.get(user_id=request.user.id)
    meus_cursos = Curso.objects.filter(professor_id=professor.id).order_by('titulo')
    
    if request.method=='POST':
        form = CursoForm(request.POST or None)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = professor
            curso.save()
    else :
        form = CursoForm()

    data = {}
    data['obj_list'] = meus_cursos
    data['form'] = form
    return render(request, template_name, data)

def professor_curso_alunos(request, template_name='programacao/professor_curso_alunos.html'):
    professor = Professor.objects.get(user_id=request.user.id)
    minhas_cursos = Curso.objects.filter(professor_id=professor.id).order_by('titulo')

    if request.method=='POST':
        id_curso = request.POST.get('curso')
        curso = Curso.objects.get(id=id_curso)
        aluno_curso = AlunoCurso.objects.filter(curso_id=id_curso)
        alunos = []
        for ad in aluno_curso :
            alunos.extend(list(Aluno.objects.filter(id=ad.aluno_id)))

        data = {}
        data['curso_list'] = minhas_cursos
        data['alunos_list'] = alunos
        data['curso'] = curso
        return render(request, template_name, data)

    data = {}
    data['curso_list'] = minhas_cursos
    return render(request, template_name, data)

# @login_required()
def professor_minhas_atividades(request, template_name='programacao/professor_minhas_cursos.html'):
    data = {}
    return render(request, template_name, data)


def professor_atividade(request, pk, template_name='programacao/professor_atividade.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk)
    
    data = {}
    data['atividade'] = atividade
    return render(request, template_name, data)


# @login_required()
def professor_minhas_intervencoes(request, template_name='programacao/professor_minhas_cursos.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_quadro_notas(request, template_name='programacao/professor_minhas_cursos.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_comentarios(request, template_name='programacao/professor_minhas_cursos.html'):
    data = {}
    return render(request, template_name, data)


## Curso
# @login_required()
def professor_curso_edit(request, pk, template_name='programacao/professor_curso_edit.html'):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoEditForm(request.POST or None, instance=curso)
    
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_edit', pk=pk)
        else :
            form = CursoEditForm()

    interacao_list = Interacao.objects.filter(curso_id=curso.id)
    
    try:
        curriculum = Curriculum.objects.get(id=curso.curriculum_id)

        objetivos = ObjetivoProgramacao.objects.filter(curriculum_id=curriculum.id).order_by('ordem')
        topicos = []
        atividades = []
        suportes = []
        
        for obj in objetivos :
            topicos.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))
    
        for obj in topicos :
            suportes.extend(list(obj.suportes.all()))
            tas = TopicoAtividade.objects.filter(topico_id=obj.id)
            for ta in tas :
                atividades.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
        
        for obj in atividades :
            suportes.extend(list(obj.suportes.all()))
    
        data = {}
        data['form'] = form
        data['curso'] = curso
        data['curriculum'] = curriculum
        data['interacao_list'] = interacao_list
        data['objetivos_list'] = objetivos
        data['topicos_list'] = topicos
        data['atividades_list'] = atividades
        data['suportes_list'] = suportes
        return render(request, template_name, data)
    except:
        pass
        #add mensagem

    data = {}
    data['form'] = form
    data['curso'] = curso
    data['interacao_list'] = interacao_list
    return render(request, template_name, data)


# @login_required()
def professor_curso_delete(request, pk, template_name='programacao/professor_curso_confirm_delete.html'):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method=='POST':
        curso.delete()
        return redirect('programacao:professor_minhas_cursos')
    
    data = {}
    data['curso'] = curso
    
    return render(request, template_name, data)


def professor_curriculum(request, template_name='programacao/professor_curriculum_edit.html'):
    form = CurriculumForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
#             professor = Professor.objects.get(user_id=request.user.id) AUTOR
            form.save()
            return redirect('programacao:professor_curriculum')
        else : 
            form = CurriculumForm()

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curriculum_add(request, pk1, template_name='programacao/professor_curriculum_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    
    form = CurriculumForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
#             professor = Professor.objects.get(user_id=request.user.id) AUTOR
            curriculum = form.save() 
            
            curso.curriculum_id = curriculum.id
            curso.curriculum = curriculum
            curso.save()

            return redirect('programacao:professor_curso_edit', pk=pk1)
        else : 
            form = CurriculumForm()

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curriculum_edit(request, pk, template_name='programacao/professor_curriculum_edit.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    
    form = CurriculumForm(request.POST or None, instance=curriculum)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curriculum_edit', pk=pk)
        else : 
            form = CurriculumForm()

    data = {}
    data['form'] = form
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def professor_curso_curriculum(request, pk, template_name='programacao/professor_curso_curriculum.html'):   
    curso = get_object_or_404(Curso, pk=pk)
    curriculum_list = Curriculum.objects.all()

    if request.method=='POST':
        id_curriculum = request.POST.get('curriculum')
        curriculum = Curriculum.objects.get(id=id_curriculum)

        objetivos_list = ObjetivoProgramacao.objects.filter(curriculum_id=curriculum.id).order_by('ordem')
        topicos_list = []
        atividades_list = []
        suportes_list = []
        
        for obj in objetivos_list :
            topicos_list.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))
    
        for obj in topicos_list :
            suportes_list.extend(list(obj.suportes.all()))
            tas = TopicoAtividade.objects.filter(topico_id=obj.id)
            for ta in tas :
                atividades_list.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
        
        for obj in atividades_list :
            suportes_list.extend(list(obj.suportes.all()))

        data = {}
        data['curso'] = curso
        data['curriculum_list'] = curriculum_list
        data['curriculum'] = curriculum
        data['objetivos_list'] = objetivos_list
        data['topicos_list'] = topicos_list
        data['atividades_list'] = atividades_list
        data['suportes_list'] = suportes_list
        return render(request, template_name, data)

    data = {}
    data['curso'] = curso
    data['curriculum_list'] = curriculum_list
    return render(request, template_name, data)


def professor_curso_associar_curriculum(request, pk1, pk2, template_name='programacao/professor_curso_curriculum_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)
    
    curso.curriculum_id = curriculum.id
    curso.curriculum = curriculum
    curso.save()

    return redirect('programacao:professor_curso_edit', pk=pk1)


def professor_curso_curriculum_edit(request, pk1, pk2, template_name='programacao/professor_curso_curriculum_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)
   
    form = CurriculumForm(request.POST or None, instance=curriculum)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CurriculumForm()
   
    objetivos_list = ObjetivoProgramacao.objects.filter(curriculum_id=curriculum.id).order_by('ordem')
    topicos_list = []
    atividades_list = []
    suportes_list = []
    
    for obj in objetivos_list :
        topicos_list.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))

    for obj in topicos_list :
        suportes_list.extend(list(obj.suportes.all()))
        tas = TopicoAtividade.objects.filter(topico_id=obj.id)
        for ta in tas :
            atividades_list.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
    
    for obj in atividades_list :
        suportes_list.extend(list(obj.suportes.all()))

    data = {}
    data['curso'] = curso
    data['curriculum'] = curriculum
    data['form'] = form
    data['objetivos_list'] = objetivos_list
    data['topicos_list'] = topicos_list
    data['atividades_list'] = atividades_list
    data['suportes_list'] = suportes_list
    return render(request, template_name, data)


def professor_curriculum_delete(request, pk1, pk2, template_name='programacao/professor_curso_curriculum_confirm_delete.html'):
    curso = get_object_or_404(Curriculum, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)
    if request.method=='POST':
        curriculum.delete()
        curso.curriculum = None
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['curso'] = curso
    data['curriculum'] = curriculum
    return render(request, template_name, data)


def professor_curso_objetivo(request, template_name='programacao/professor_curso_objetivo_edit.html'):
    objetivo_list = ObjetivoProgramacao.objects.all()   
    if request.method=='POST':
        form = CursoObjetivoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_objetivo')
        else : 
            form = CursoObjetivoForm()

    form = CursoObjetivoForm(request.POST or None)

    data = {}
    data['form'] = form
    data['objetivo_list'] = objetivo_list
    return render(request, template_name, data)


def professor_curso_objetivo_add(request, pk1, pk2, template_name='programacao/professor_curso_objetivo_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)

    if request.method=='POST':
        form = CurriculumObjetivoForm(request.POST or None)
        if form.is_valid():
            objetivo = form.save(commit=False)
            objetivo.curriculum = curriculum
            objetivo.save()
            
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CurriculumObjetivoForm()

    form = CurriculumObjetivoForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_objetivo_edit(request, pk1, pk2, template_name='programacao/professor_curso_objetivo_edit.html'):
    objetivo_list = ObjetivoProgramacao.objects.all()
    objetivo = get_object_or_404(ObjetivoProgramacao, pk=pk2)
    form = CursoObjetivoForm(request.POST or None, instance=objetivo)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_objetivo_edit', pk=pk1)
        else : 
            form = CursoObjetivoForm()

    data = {}
    data['objetivo'] = objetivo
    data['curso_id'] = pk1
    data['form'] = form
    data['objetivo_list'] = objetivo_list
    return render(request, template_name, data)


# @login_required()
def professor_curso_objetivo_delete(request, pk1, pk2, template_name='programacao/professor_curso_objetivo_confirm_delete.html'):
    objetivo = get_object_or_404(ObjetivoProgramacao, pk=pk2)
    if request.method=='POST':
        objetivo.delete()
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['objetivo'] = objetivo
    return render(request, template_name, data)


def professor_curso_topico(request, template_name='programacao/professor_curso_topico_edit.html'):
    if request.method=='POST':
        form = CursoTopicoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_topico')
        else : 
            form = CursoTopicoForm()

    form = CursoTopicoForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_topico_add(request, pk1, pk2, template_name='programacao/professor_curso_topico_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)

    if request.method=='POST':
        form = CursoTopicoForm(request.POST or None)
        form.fields["objetivo"].queryset = ObjetivoProgramacao.objects.filter(curriculum_id=curriculum.id)
        if form.is_valid():
            form.save()
            
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CursoTopicoForm()

    form = CursoTopicoForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_topico_edit(request, pk1, pk2, template_name='programacao/professor_curso_topico_edit.html'):
    topico = get_object_or_404(TopicoProgramacao, pk=pk2)
    form = CursoTopicoForm(request.POST or None, instance=topico)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_topico_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CursoTopicoForm()

    data = {}
    data['topico'] = topico
    data['curso_id'] = pk1
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_topico_delete(request, pk1, pk2, template_name='programacao/professor_curso_topico_confirm_delete.html'):
    topico = get_object_or_404(TopicoProgramacao, pk=pk2)
    if request.method=='POST':
        topico.delete()
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['topico'] = topico
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_atividade(request, template_name='programacao/professor_curso_atividade_edit.html'):
    if request.method=='POST':
        form = CursoAtividadeForm(request.POST or None)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.autor = Professor.objects.get(user_id=request.user.id)
            atividade.save()

            return redirect('programacao:professor_curso_atividade')
        else : 
            form = CursoAtividadeForm()

    form = CursoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_atividade_add(request, pk1, pk2, template_name='programacao/professor_curso_atividade_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)

    if request.method=='POST':
        form = CursoAtividadeForm(request.POST or None)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.autor = Professor.objects.get(user_id=request.user.id)
            atividade.save()
            
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CursoAtividadeForm()

    form = CursoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_atividade_edit(request, pk1, pk2, template_name='programacao/professor_curso_atividade_edit.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk2)
    form = CursoAtividadeForm(request.POST or None, instance=atividade)
    exercicios = ExercicioPratico.objects.filter(atividade_id=atividade.id)

    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_atividade_edit', pk1=pk1, pk2=pk2)
        else :
            form = CursoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    data['atividade'] = atividade
    data['curso_id'] = pk1
    data['exercicios_list'] = exercicios
    return render(request, template_name, data)


def professor_curso_atividade_delete(request, pk1, pk2, template_name='programacao/professor_curso_atividade_confirm_delete.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk2)
    topico_atividade = TopicoAtividade.objects.get(atividade_id=pk2)

    if request.method=='POST':
        topico_atividade.delete()
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['atividade'] = atividade
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_topico_atividade(request, template_name='programacao/professor_curso_topico_atividade.html'):
    if request.method=='POST':
        form = CursoTopicoAtividadeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_topico_atividade')
        else : 
            form = CursoTopicoAtividadeForm()

    form = CursoTopicoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_topico_atividade_add(request, pk1, pk2, template_name='programacao/professor_curso_topico_atividade.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)    
    
    if request.method=='POST':
        form = CursoTopicoAtividadeForm(request.POST or None)
#         form.fields["atividade"].queryset = AtividadeProgramacao.objects.filter(autor_id = request.user.id)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CursoTopicoAtividadeForm()

    form = CursoTopicoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_suporte(request, template_name='programacao/professor_curso_suporte_edit.html'):
    form = CursoSuporteForm(request.POST or None, request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_suporte')
        else : 
            form = CursoSuporteForm()

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_suporte_add(request, pk1, pk2, template_name='programacao/professor_curso_suporte_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)

    if request.method=='POST':
        form = CursoSuporteForm(request.POST or None)
        if form.is_valid():
            form.save()
            
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = CursoSuporteForm()

    form = CursoSuporteForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_suporte_edit(request, pk1, pk2, template_name='programacao/professor_curso_suporte_edit.html'):
    suporte = get_object_or_404(Suporte, pk=pk2)
    form = CursoSuporteForm(request.POST or None, request.FILES or None, instance=suporte)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_suporte_edit', pk=pk2)
        else : 
            form = CursoSuporteForm()

    data = {}
    data['form'] = form
    data['suporte'] = suporte
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_suporte_delete(request, pk1, pk2, template_name='programacao/professor_curso_suporte_confirm_delete.html'):
    suporte = get_object_or_404(Suporte, pk=pk2)
    if request.method=='POST':
        topicos = TopicoProgramacao.objects.filter(suportes=suporte) 
        for t in topicos :
            t.suportes.remove(suporte)
        atividades = AtividadeProgramacao.objects.filter(suportes=suporte) 
        for a in atividades :
            a.suportes.remove(suporte)
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['suporte'] = suporte
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_topico_suporte(request, template_name='programacao/professor_curso_topico_suporte.html'):
    if request.method=='POST':
        form = TopicoSuporteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_topico_suporte')
        else : 
            form = TopicoSuporteForm()

    form = TopicoSuporteForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_curso_topico_suporte_add(request, pk1, pk2, template_name='programacao/professor_curso_topico_suporte.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)    
    
    if request.method=='POST':
        form = TopicoSuporteForm(request.POST or None)
#         form.fields["atividade"].queryset = AtividadeProgramacao.objects.filter(autor_id = request.user.id)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_curriculum_edit', pk1=pk1, pk2=pk2)
        else : 
            form = TopicoSuporteForm()

    form = TopicoSuporteForm(request.POST or None)

    data = {}
    data['form'] = form
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_atividade_exercicio(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_edit.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk2)
    form = ExercicioForm(request.POST or None, request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            exercicio = form.save(commit=False)
            exercicio.atividade = atividade
            exercicio.save()
            return redirect('programacao:professor_curso_atividade_edit', pk1=pk1, pk2=pk2)
    
    data = {}
    data['form'] = form
    data['atividade'] = atividade
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_atividade_exercicio_edit(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_edit.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)
    form = ExercicioForm(request.POST or None, request.FILES or None, instance=exercicio)

    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_atividade_edit', pk1=pk1, pk2=pk2)
   
    data = {}
    data['form'] = form
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['curso_id'] = pk1
    return render(request, template_name, data)


def professor_curso_atividade_exercicio_delete(request, pk, template_name='programacao/professor_curso_atividade_exercicio_confirm_delete.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)
    if request.method=='POST':
        exercicio.delete()
        return redirect('programacao:professor_curso_atividade_edit', pk1=exercicio.id, pk2=atividade.id)
    
    data = {}
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    return render(request, template_name, data)

def professor_curso_atividade_exercicio_testes(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_testes.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)

    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(exercicio_id=exercicio.id)
    
    professor = Professor.objects.get(user_id=request.user.id)
    testFile = str(exercicio.arquivoTeste)
    for submissao in submissoes:
        submissaoFile = str(submissao.arquivo)
       
        p = subprocess.Popen('python ' + settings.MEDIA_ROOT + '/' + testFile + ' ' + settings.MEDIA_ROOT + ' ' + submissaoFile + ' ' + professor.user.username, shell=True)
        p.wait()

        with open(settings.MEDIA_ROOT + '/teste/' + professor.user.username + '/result.txt', 'r') as f:
            resultFile = File(f)
            errors = int(resultFile.readline().rstrip())
            failures = int(resultFile.readline().rstrip())
            tests = int(resultFile.readline().rstrip())
            resultFile.close()

        result = ((float(tests) - (float(errors) + float(failures))) / tests) * 100
        submissao.avaliacao = result
        submissao.save()

    data = {}
    data['curso_id'] = pk1
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['submissoes_list'] = submissoes
   
    return render(request, template_name, data)


def professor_curso_atividade_exercicio_view(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_testes.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)

    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(exercicio_id=exercicio.id)

    data = {}
    data['curso_id'] = pk1
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['submissoes_list'] = submissoes
   
    return render(request, template_name, data)


def professor_curso_interacao(request, pk1, template_name='programacao/professor_curso_interacao_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)

    form = InteracaoForm(request.POST or None)    
    if request.method=='POST':
        if form.is_valid():
            interacao = form.save(commit = False)
            interacao.curso = curso
            interacao.save()
            return redirect('programacao:professor_curso_edit', pk=pk1)
   
    data = {}
    data['form'] = form
    data['curso'] = curso
    return render(request, template_name, data)


def professor_curso_interacao_edit(request, pk1, pk2, template_name='programacao/professor_curso_interacao_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    interacao = get_object_or_404(Interacao, pk=pk2)

    form = InteracaoForm(request.POST or None, instance=interacao)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_curso_edit', pk=pk1)
        else:
            form = InteracaoForm(request.POST or None) 
   
    data = {}
    data['form'] = form
    data['curso'] = curso
    return render(request, template_name, data)


def professor_curso_interacao_delete(request, pk1, pk2, template_name='programacao/professor_curso_confirm_delete.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    interacao = get_object_or_404(Interacao, pk=pk2)
    
    if request.method=='POST':
        interacao.delete()
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['curso'] = curso
    return render(request, template_name, data)
