from django.contrib import admin
from .models import Morador, Visitante, AreaComum, HorariosFuncionamento, Reserva, Encomenda, Veiculo

# Inline do horário (apenas para ser usado dentro da Área Comum)
class HorariosFuncionamentoInline(admin.TabularInline):
    model = HorariosFuncionamento
    extra = 1 # Define quantas linhas vazias aparecem por padrão

@admin.register(AreaComum)
class AreaComumAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',) 
    inlines = [HorariosFuncionamentoInline]

@admin.register(Morador)
class MoradorAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartamento', 'cpf') 
    search_fields = ('user__username', 'apartamento', 'cpf')

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'apartamento')
    search_fields = ('nome', 'cpf', 'apartamento__apartamento')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('area', 'apartamento', 'data', 'hora_inicio', 'hora_fim')
    list_filter = ('data',)
    search_fields = ('area__nome', 'apartamento__user__username')

@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'descricao', 'recebido_em')
    list_filter = ('recebido_em',)
    search_fields = ('apartamento__user__username', 'descricao')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'placa', 'tipo_veiculo', 'modelo', 'cor')
    list_filter = ('tipo_veiculo',)
    search_fields = ('apartamento__user__username', 'placa', 'modelo')