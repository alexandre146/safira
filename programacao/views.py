# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
import os

from mathema.forms import TopicoSuporteForm
from mathema.models import TopicoAtividade, Suporte, Curriculum, Objetivo, \
    Atividade, Topico
from programacao.forms import AlunoForm, ProfessorForm, CursoForm, RegistroForm, \
    UserEditForm, CursoEditForm, ExercicioForm, AlunoSubmissaoExercicioPraticoForm
from programacao.models import Aluno, Professor, Curso, AlunoCurso, ExercicioPratico, AlunoSubmissaoExercicioPratico, \
    Avaliador


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
    for ac in aluno_curso :
        curso = Curso.objects.get(id=ac.curso_id)
        curriculum.extend(list(Curriculum.objects.filter(id=curso.curriculum.id)))
     
    objetivos = []
    for c in curriculum :
        objetivos.extend(list(Objetivo.objects.filter(curriculum_id=c.id)))
 
    topicos = []
    for obj in objetivos :
        topicos.extend(list(Topico.objects.filter(objetivo_id=obj.id)))
 
    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(Atividade.objects.filter(id=ta.atividade.id)))
    
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
    
    return redirect('programacao:aluno_meus_cursos')


def aluno_curso_desinscrever(request, pk, template_name='programacao/aluno_meus_cursos.html'):
#     aluno = Aluno.objects.get(user_id=request.user.id)
    curso = get_object_or_404(Curso, pk=pk)
    
    inscricao = AlunoCurso.objects.get(curso=curso)
    inscricao.delete()

    return redirect('programacao:aluno_meus_cursos')


def aluno_curso(request, pk, template_name='programacao/aluno_curso.html'):
    curso = get_object_or_404(Curso, pk=pk)
    
    try :
        objetivos = Objetivo.objects.filter(curriculum_id=curso.curriculum.id)
     
        topicos = []
        for obj in objetivos :
            topicos.extend(list(Topico.objects.filter(objetivo_id=obj.id)))
     
        atividades = []
        for t in topicos :
            tas = TopicoAtividade.objects.filter(topico_id=t.id)
            for ta in tas :
                atividades.extend(list(Atividade.objects.filter(id=ta.atividade.id)))
        
    except:
        data = {}
        data['curso'] = curso
        return render(request, template_name, data)        

    data = {}
    data['curso'] = curso
    data['atividades_list'] = atividades
    return render(request, template_name, data)


def aluno_atividade(request, pk, template_name='programacao/aluno_atividade.html'):
    atividade = get_object_or_404(Atividade, pk=pk)
    exercicios = atividade.get_exercicios()
    
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
        objetivos.extend(list(Objetivo.objects.filter(curriculum_id=c.id)))
 
    topicos = []
    for obj in objetivos :
        topicos.extend(list(Topico.objects.filter(objetivo_id=obj.id)))
 
    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(Atividade.objects.filter(id=ta.atividade.id)))
    
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
def professor_minhas_atividades(request, template_name='programacao/professor_meus_cursos.html'):
    data = {}
    return render(request, template_name, data)


def professor_atividade(request, pk, template_name='programacao/professor_atividade.html'):
    atividade = get_object_or_404(Atividade, pk=pk)
    
    data = {}
    data['atividade'] = atividade
    return render(request, template_name, data)


# @login_required()
def professor_minhas_intervencoes(request, template_name='programacao/professor_meus_cursos.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_quadro_notas(request, template_name='programacao/professor_meus_cursos.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_comentarios(request, template_name='programacao/professor_meus_cursos.html'):
    data = {}
    return render(request, template_name, data)


## Curso
# @login_required()
def professor_curso_edit(request, pk, template_name='programacao/professor_curso_edit.html'):
    curso = get_object_or_404(Curso, pk=pk)
    curso_form = CursoEditForm(request.POST or None, instance=curso)

    if request.method=='POST' and 'salvar' in request.POST:
        print("salvar")
        if curso_form.is_valid():
            curso_form.save()
            return redirect('programacao:professor_curso_edit', pk=pk)

    try :
        curriculum = curso.curriculum
        objetivo_list = Objetivo.objects.filter(curriculum_id = curriculum.id).order_by('ordem')
        
        topicos_list = []
        for objetivo in objetivo_list :
            topicos_list.extend(list(objetivo.get_topicos()))
        
        atividade_list = []
        for topico in topicos_list :
            atividade_list.extend(list(topico.get_atividades()))

        data = {}
        data['curso'] = curso
        data['curso_form'] = curso_form
        data['curriculum'] = curriculum
        data['atividade_list'] = atividade_list
    except:
        data = {}
        data['curso'] = curso
        data['curso_form'] = curso_form

    return render(request, template_name, data)


# @login_required()
def professor_curso_delete(request, pk, template_name='programacao/professor_curso_confirm_delete.html'):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method=='POST':
        curso.delete()
        return redirect('programacao:professor_meus_cursos')
    
    data = {}
    data['curso'] = curso
    
    return render(request, template_name, data)


def professor_curso_curriculum_list(request, pk, template_name='programacao/professor_curso_curriculum_list.html'):
    curso = get_object_or_404(Curso, pk=pk)
    curriculum_list = Curriculum.objects.filter(autor=request.user)

    data = {}
    data['curso'] = curso
    data['curriculum_list'] = curriculum_list
    
    return render(request, template_name, data)


def professor_curso_curriculum_view(request, pk1, pk2, template_name='programacao/professor_curso_curriculum_view.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)
    objetivo_list = Objetivo.objects.filter(curriculum_id = curriculum.id).order_by('ordem')

    data = {}
    data['curso'] = curso
    data['curriculum'] = curriculum
    data['objetivo_list'] = objetivo_list

    return render(request, template_name, data)   


def professor_curso_associar_curriculum(request, pk1, pk2, template_name='programacao/professor_curso_edit.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)
    
    # copia de curriculum
    novo_curriculum = curriculum.copy()

    curso.curriculum = novo_curriculum
    curso.save()
    return redirect('programacao:professor_curso_edit', pk=pk1)


def professor_curso_curriculum_delete(request, pk1, pk2, template_name='programacao/professor_curso_curriculum_confirm_delete.html'):
    curso = get_object_or_404(Curso, pk=pk1)
    curriculum = get_object_or_404(Curriculum, pk=pk2)

    if request.method=='POST':
        curso.curriculum = None
        curso.save()
        
        #curriculum.delete()
        
        return redirect('programacao:professor_curso_edit', pk=pk1)
    
    data = {}
    data['curso'] = curso
    data['curriculum'] = curriculum
    
    return render(request, template_name, data)


def professor_curso_atividade_exercicio(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_edit.html'):
    atividade = get_object_or_404(Atividade, pk=pk2)
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
    atividade = Atividade.objects.get(id=exercicio.atividade_id)
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


def professor_atividade_exercicio_delete(request, pk, template_name='programacao/professor_atividade_exercicio_confirm_delete.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk)

    if request.method=='POST':
        exercicio.delete()
        return redirect('programacao:curriculum_list')
    # redirect para o curriculum     
    
    data = {}
    data['exercicio'] = exercicio
    return render(request, template_name, data)


def professor_curso_atividade_exercicio_avaliacoes(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_avaliacoes.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk1)
    curso = Curso.objects.get(curriculum=curriculum)
    
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(exercicio_id=exercicio.id)
    
    professor = Professor.objects.get(user_id=request.user.id)
    
    avaliador = Avaliador() 
    avaliador.avaliar(exercicio, submissoes, professor)

    data = {}
    data['curso'] = curso
    data['curriculum'] = curriculum
#     data['atividade'] = atividade
    data['exercicio'] = exercicio
    data['submissoes_list'] = submissoes
   
    return render(request, template_name, data)


def professor_curso_atividade_exercicio_view(request, pk1, pk2, template_name='programacao/professor_curso_atividade_exercicio_testes.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = Atividade.objects.get(id=exercicio.atividade_id)

    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(exercicio_id=exercicio.id)

    data = {}
    data['curso_id'] = pk1
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['submissoes_list'] = submissoes
   
    return render(request, template_name, data)

