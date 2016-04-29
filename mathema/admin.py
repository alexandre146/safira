# -*- coding: utf-8 -*-
from django.contrib import admin
from mathema.models import TipoSuporte, Suporte, Atividade, Topico, Objetivo,\
    TopicoAtividade, TopicoSuporte, AtividadeSuporte, Curriculum

admin.site.register(TipoSuporte)
admin.site.register(Suporte)
admin.site.register(Atividade)
admin.site.register(AtividadeSuporte)
admin.site.register(Topico)
admin.site.register(TopicoAtividade)
admin.site.register(TopicoSuporte)
admin.site.register(Objetivo)
admin.site.register(Curriculum)