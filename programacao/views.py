# -*- coding: utf-8 -*-
import datetime
import subprocess
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File

from mathema.models import TopicoAtividade, Suporte
from programacao.forms import AlunoForm, ProfessorForm, DisciplinaForm, RegistroForm, \
    UserEditForm, DisciplinaEditForm, DisciplinaObjetivoForm, \
    DisciplinaTopicoForm, DisciplinaAtividadeForm, DisciplinaTopicoAtividadeForm, \
    DisciplinaSuporteForm, ExercicioForm, AlunoSubmissaoExercicioPraticoForm
from programacao.models import Aluno, Professor, Disciplina, AlunoDisciplina, ObjetivoProgramacao, TopicoProgramacao, \
    AtividadeProgramacao, ExercicioPratico, AlunoSubmissaoExercicioPratico


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

                messages.add_message(request, messages.INFO, 'Cadastrado realizado com sucesso!')
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
    aluno_disciplina = AlunoDisciplina.objects.filter(aluno_id=aluno.id)
    objetivos = []
    for ad in aluno_disciplina :
        objetivos.extend(list(ObjetivoProgramacao.objects.filter(disciplina_id=ad.disciplina_id)))

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


def aluno_disciplina_list(request, template_name='programacao/aluno_disciplina_list.html'):
    todas_disciplinas = Disciplina.objects.all()
    
    aluno = Aluno.objects.get(user_id=request.user.id)
    aluno_disciplina = AlunoDisciplina.objects.filter(aluno_id=aluno.id)
    minhas_disciplinas = []
    for ad in aluno_disciplina :
        minhas_disciplinas.extend(list(Disciplina.objects.filter(id=ad.disciplina_id)))

    disciplinas = set(todas_disciplinas).difference(set(minhas_disciplinas))
    
    data = {}
    data['obj_list'] = disciplinas
    return render(request, template_name, data)

# @login_required()
def aluno_minhas_disciplinas(request, template_name='programacao/aluno_minhas_disciplinas.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    aluno_disciplina = AlunoDisciplina.objects.filter(aluno_id=aluno.id)
    minhas_disciplinas = []
    for ad in aluno_disciplina :
        minhas_disciplinas.extend(list(Disciplina.objects.filter(id=ad.disciplina_id)))

    minhas_disciplinas = sorted(minhas_disciplinas, key=lambda disciplina: disciplina.titulo)

    data = {}
    data['disciplinas_list'] = minhas_disciplinas
    return render(request, template_name, data)


def aluno_disciplina_inscrever(request, pk, template_name='programacao/aluno_disciplina_list.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    disciplina = get_object_or_404(Disciplina, pk=pk)
    
    inscricao = AlunoDisciplina.objects.create(aluno=aluno, disciplina=disciplina)
    inscricao.save()
    
    return redirect('programacao:aluno_minhas_disciplinas')


def aluno_disciplina_desinscrever(request, pk, template_name='programacao/aluno_minhas_disciplinas.html'):
    aluno = Aluno.objects.get(user_id=request.user.id)
    disciplina = get_object_or_404(Disciplina, pk=pk)
    
    inscricao = AlunoDisciplina.objects.get(disciplina=disciplina)
    inscricao.delete()

    return redirect('programacao:aluno_minhas_disciplinas')


def aluno_disciplina(request, pk, template_name='programacao/aluno_disciplina.html'):
    disciplina = get_object_or_404(Disciplina, pk=pk)

    objetivos = ObjetivoProgramacao.objects.filter(disciplina_id=disciplina.id)

    topicos = []
    for obj in objetivos :
        topicos.extend(list(TopicoProgramacao.objects.filter(objetivo_id=obj.id)))

    atividades = []
    for t in topicos :
        tas = TopicoAtividade.objects.filter(topico_id=t.id)
        for ta in tas :
            atividades.extend(list(AtividadeProgramacao.objects.filter(id=ta.atividade.id)))
    
    data = {}
    data['disciplina'] = disciplina
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
    disciplinas = Disciplina.objects.filter(professor_id=professor.id)

    objetivos = []
    for d in disciplinas :
        objetivos.extend(list(ObjetivoProgramacao.objects.filter(disciplina_id=d.id)))

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
def professor_minhas_disciplinas(request, template_name='programacao/professor_minhas_disciplinas.html'):
    professor = Professor.objects.get(user_id=request.user.id)
    minhas_disciplinas = Disciplina.objects.filter(professor_id=professor.id).order_by('titulo')
    
    if request.method=='POST':
        form = DisciplinaForm(request.POST or None)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.professor = professor
            disciplina.save()
    else :
        form = DisciplinaForm()

    data = {}
    data['obj_list'] = minhas_disciplinas
    data['form'] = form
    return render(request, template_name, data)

def professor_disciplina_alunos(request, template_name='programacao/professor_disciplina_alunos.html'):
    professor = Professor.objects.get(user_id=request.user.id)
    minhas_disciplinas = Disciplina.objects.filter(professor_id=professor.id).order_by('titulo')

    if request.method=='POST':
        id_disciplina = request.POST.get('disciplina')
        disciplina = Disciplina.objects.get(id=id_disciplina)
        aluno_disciplina = AlunoDisciplina.objects.filter(disciplina_id=id_disciplina)
        alunos = []
        for ad in aluno_disciplina :
            alunos.extend(list(Aluno.objects.filter(id=ad.aluno_id)))

        data = {}
        data['disciplina_list'] = minhas_disciplinas
        data['alunos_list'] = alunos
        data['disciplina'] = disciplina
        return render(request, template_name, data)

    data = {}
    data['disciplina_list'] = minhas_disciplinas
    return render(request, template_name, data)

# @login_required()
def professor_minhas_atividades(request, template_name='programacao/professor_minhas_disciplinas.html'):
    data = {}
    return render(request, template_name, data)


def professor_atividade(request, pk, template_name='programacao/professor_atividade.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk)
    
    data = {}
    data['atividade'] = atividade
    return render(request, template_name, data)


def professor_disciplina_atividade_exercicio(request, pk, template_name='programacao/professor_disciplina_atividade_exercicio_edit.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk)
    form = ExercicioForm(request.POST or None, request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            exercicio = form.save(commit=False)
            exercicio.atividade = atividade
            exercicio.save()
            
            return redirect('programacao:disciplina_atividade_edit', pk)
    
    data = {}
    data['form'] = form
    data['atividade'] = atividade
    return render(request, template_name, data)


def professor_disciplina_atividade_exercicio_edit(request, pk1, pk2, template_name='programacao/professor_disciplina_atividade_exercicio_edit.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)
    form = ExercicioForm(request.POST or None, request.FILES or None, instance=exercicio)

    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:disciplina_atividade_edit', pk=atividade.id)
   
    data = {}
    data['form'] = form
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['disciplina_id'] = pk1
    return render(request, template_name, data)


def professor_disciplina_atividade_exercicio_delete(request, pk, template_name='programacao/professor_disciplina_atividade_exercicio_confirm_delete.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)
    if request.method=='POST':
        exercicio.delete()
        return redirect('programacao:disciplina_atividade_edit', pk=atividade.id)
    
    data = {}
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    return render(request, template_name, data)

def professor_disciplina_atividade_exercicio_testes(request, pk1, pk2, template_name='programacao/professor_disciplina_atividade_exercicio_testes.html'):
    exercicio = get_object_or_404(ExercicioPratico, pk=pk2)
    atividade = AtividadeProgramacao.objects.get(id=exercicio.atividade_id)

    submissoes = AlunoSubmissaoExercicioPratico.objects.filter(exercicio_id=exercicio.id)

    testFile = exercicio.arquivo
    for submissao in submissoes:
#       p = subprocess.Popen(['python', settings.MEDIA_ROOT + testFile])

        with open(settings.MEDIA_ROOT + '/submissao/teste1.py', 'r+') as f:
            arqtest = File(f)
            
            for line in arqtest.readlines():
                if 'file =' in line.rstrip():
                    arqtest.write("file = os.path.dirname(os.path.dirname(__file__))" + str(submissao.arquivo))
                    print(line)
        arqtest.close()

        p = subprocess.Popen(['python', settings.MEDIA_ROOT + '/submissao/teste1.py'])
        p.wait()

        with open(settings.MEDIA_ROOT + '/submissao/result.txt', 'rb') as f:
            resultFile = File(f)
            errors = int(resultFile.readline().rstrip())
            failures = int(resultFile.readline().rstrip())
            tests = int(resultFile.readline().rstrip())
        resultFile.close()

        result = ((float(tests) - (float(errors) + float(failures))) / tests) * 100
        submissao.avaliacao = result
        submissao.save()

    data = {}
    data['disciplina_id'] = pk1
    data['exercicio'] = exercicio
    data['atividade'] = atividade
    data['submissoes_list'] = submissoes
   
    return render(request, template_name, data)


# @login_required()
def professor_minhas_intervencoes(request, template_name='programacao/professor_minhas_disciplinas.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_quadro_notas(request, template_name='programacao/professor_minhas_disciplinas.html'):
    data = {}
    return render(request, template_name, data)


# @login_required()
def professor_comentarios(request, template_name='programacao/professor_minhas_disciplinas.html'):
    data = {}
    return render(request, template_name, data)


## Disciplina
# @login_required()
def professor_disciplina_edit(request, pk, template_name='programacao/professor_disciplina_edit.html'):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    form = DisciplinaEditForm(request.POST or None, instance=disciplina)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_edit', pk=pk)
        else :
            form = DisciplinaEditForm()

    objetivos = ObjetivoProgramacao.objects.filter(disciplina_id=disciplina.id).order_by('ordem')
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
    data['disciplina'] = disciplina
    data['objetivos_list'] = objetivos
    data['topicos_list'] = topicos
    data['atividades_list'] = atividades
    data['suportes_list'] = suportes
    return render(request, template_name, data)


# @login_required()
def professor_disciplina_delete(request, pk, template_name='programacao/professor_disciplina_confirm_delete.html'):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method=='POST':
        disciplina.delete()
        return redirect('programacao:professor_minhas_disciplinas')
    
    data = {}
    data['disciplina'] = disciplina
    return render(request, template_name, data)


def professor_disciplina_objetivo(request, template_name='programacao/professor_disciplina_objetivo_edit.html'):   
    if request.method=='POST':
        form = DisciplinaObjetivoForm(request.POST or None)
        professor = Professor.objects.get(user_id=request.user.id)
        form.fields["disciplina"].queryset = Disciplina.objects.filter(professor_id=professor.id)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_objetivo_edit')
        else : 
            form = DisciplinaObjetivoForm()

    form = DisciplinaObjetivoForm(request.POST or None)
    professor = Professor.objects.get(user_id=request.user.id)
    form.fields["disciplina"].queryset = Disciplina.objects.filter(professor_id=professor.id)

    data = {}
    data['form'] = form
    return render(request, template_name, data)

def professor_disciplina_objetivo_edit(request, pk1, pk2, template_name='programacao/professor_disciplina_objetivo_edit.html'):
    objetivo = get_object_or_404(ObjetivoProgramacao, pk=pk2)
    form = DisciplinaObjetivoForm(request.POST or None, instance=objetivo)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_objetivo_edit', pk=pk1)
        else : 
            form = DisciplinaObjetivoForm()

    data = {}
    data['objetivo'] = objetivo
    data['disciplina_id'] = pk1
    data['form'] = form
    return render(request, template_name, data)


# @login_required()
def professor_disciplina_objetivo_delete(request, pk1, pk2, template_name='programacao/professor_disciplina_objetivo_confirm_delete.html'):
    objetivo = get_object_or_404(ObjetivoProgramacao, pk=pk2)
    if request.method=='POST':
        objetivo.delete()
        return redirect('programacao:professor_disciplina_edit', pk=pk1)
    
    data = {}
    data['objetivo'] = objetivo
    return render(request, template_name, data)


def professor_disciplina_topico(request, template_name='programacao/professor_disciplina_topico_edit.html'):
    if request.method=='POST':
        form = DisciplinaTopicoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_topico_edit')
        else : 
            form = DisciplinaTopicoForm()

    form = DisciplinaTopicoForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_disciplina_topico_edit(request, pk1, pk2, template_name='programacao/professor_disciplina_topico_edit.html'):
    topico = get_object_or_404(TopicoProgramacao, pk=pk2)
    form = DisciplinaTopicoForm(request.POST or None, instance=topico)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_topico_edit', pk=pk2)
        else : 
            form = DisciplinaTopicoForm()

    data = {}
    data['topico'] = topico
    data['disciplina_id'] = pk1
    data['form'] = form
    return render(request, template_name, data)


def professor_disciplina_topico_delete(request, pk1, pk2, template_name='programacao/professor_disciplina_topico_confirm_delete.html'):
    topico = get_object_or_404(TopicoProgramacao, pk=pk2)
    if request.method=='POST':
        topico.delete()
        return redirect('programacao:professor_disciplina_edit', pk=pk1)
    
    data = {}
    data['topico'] = topico
    data['disciplina_id'] = pk1
    return render(request, template_name, data)


def professor_disciplina_atividade(request, template_name='programacao/professor_disciplina_atividade.html'):
    if request.method=='POST':
        form = DisciplinaAtividadeForm(request.POST or None)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.autor = Professor.objects.get(user_id=request.user.id)
            atividade.save()

            return redirect('programacao:professor_disciplina_atividade')
        else : 
            form = DisciplinaAtividadeForm()

    form = DisciplinaAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_disciplina_atividade_edit(request, pk1, pk2, template_name='programacao/professor_disciplina_atividade_edit.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk2)
    form = DisciplinaAtividadeForm(request.POST or None, instance=atividade)
    exercicios = ExercicioPratico.objects.filter(atividade_id=atividade.id)

    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_atividade_edit', pk=pk2)
        else :
            form = DisciplinaAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    data['atividade'] = atividade
    data['disciplina_id'] = pk1
    data['exercicios_list'] = exercicios
    return render(request, template_name, data)


def professor_disciplina_atividade_delete(request, pk1, pk2, template_name='programacao/professor_disciplina_atividade_confirm_delete.html'):
    atividade = get_object_or_404(AtividadeProgramacao, pk=pk2)
    topico_atividade = TopicoAtividade.objects.get(atividade_id=pk2)

    if request.method=='POST':
        topico_atividade.delete()
        return redirect('programacao:professor_disciplina_edit', pk=pk1)
    
    data = {}
    data['atividade'] = atividade
    data['disciplina_id'] = pk1
    return render(request, template_name, data)


def professor_disciplina_topico_atividade(request, template_name='programacao/professor_disciplina_topico_atividade.html'):
    if request.method=='POST':
        form = DisciplinaTopicoAtividadeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_topico_atividade')
        else : 
            form = DisciplinaTopicoAtividadeForm()

    form = DisciplinaTopicoAtividadeForm(request.POST or None)

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_disciplina_suporte(request, template_name='programacao/professor_disciplina_suporte_edit.html'):
    form = DisciplinaSuporteForm(request.POST or None, request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_suporte')
        else : 
            form = DisciplinaSuporteForm()

    data = {}
    data['form'] = form
    return render(request, template_name, data)


def professor_disciplina_suporte_edit(request, pk1, pk2, template_name='programacao/professor_disciplina_suporte_edit.html'):
    suporte = get_object_or_404(Suporte, pk=pk2)
    form = DisciplinaSuporteForm(request.POST or None, request.FILES or None, instance=suporte)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('programacao:professor_disciplina_suporte_edit', pk=pk2)
        else : 
            form = DisciplinaSuporteForm()

    data = {}
    data['form'] = form
    data['suporte'] = suporte
    data['disciplina_id'] = pk1
    return render(request, template_name, data)


def professor_disciplina_suporte_delete(request, pk1, pk2, template_name='programacao/professor_disciplina_suporte_confirm_delete.html'):
    suporte = get_object_or_404(Suporte, pk=pk2)
    if request.method=='POST':
        topicos = TopicoProgramacao.objects.filter(suportes=suporte) 
        for t in topicos :
            t.suportes.remove(suporte)
        atividades = AtividadeProgramacao.objects.filter(suportes=suporte) 
        for a in atividades :
            a.suportes.remove(suporte)
        return redirect('programacao:professor_disciplina_edit', pk=pk1)
    
    data = {}
    data['suporte'] = suporte
    data['disciplina_id'] = pk1
    return render(request, template_name, data)

