# -*- coding: utf-8 -*-
from django.contrib import admin
from mathema.models import TipoSuporte, Suporte, Atividade, Topico, Objetivo,\
    TopicoAtividade

admin.site.register(TipoSuporte)
admin.site.register(Suporte)
admin.site.register(Atividade)
admin.site.register(Topico)
admin.site.register(TopicoAtividade)
admin.site.register(Objetivo)

