from django.contrib import admin

from programacao.models import Aluno, Professor, Disciplina, AlunoDisciplina, \
    ObjetivoProgramacao, TopicoProgramacao, AtividadeProgramacao,\
    AlunoSubmissaoExercicioPratico, ExercicioPratico


admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(AlunoDisciplina)
admin.site.register(ObjetivoProgramacao)
admin.site.register(TopicoProgramacao)
admin.site.register(AtividadeProgramacao)
admin.site.register(ExercicioPratico)
admin.site.register(AlunoSubmissaoExercicioPratico)
