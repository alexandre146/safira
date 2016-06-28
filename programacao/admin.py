# -*- coding: utf-8 -*-
import os

from django.contrib import admin
from django.conf import settings

from programacao.models import Aluno, Professor, Curso, AlunoCurso, \
    AlunoSubmissaoExercicioPratico, ExercicioPratico

class ProfessorAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.save()
        try:
            os.mkdir(settings.MEDIA_ROOT + "/teste/" + obj.user.username)
        except Exception, e:
            #print repr(e)
            pass


admin.site.register(Aluno)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Curso)
admin.site.register(AlunoCurso)
admin.site.register(ExercicioPratico)
admin.site.register(AlunoSubmissaoExercicioPratico)
