from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Funcionario, HorasEstacionar, TipoNotificacao, ValoresCompra

admin.site.index_title = 'Easy Park'
admin.site.site_header = 'Painel administrativo - Easy Park'
admin.site.site_title = 'Painel administrativo'
admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(User)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_superuser')
    ordering = ('username',)
    search_fields = ('username', 'email',)
    fields = ('username', 'first_name', 'email', 'last_login', 'date_joined' , 'is_active', 'is_superuser')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'setor', 'fiscal', 'ativo',)
    ordering = ('user',)
    search_fields = ('user', 'setor', 'fiscal',)


@admin.register(HorasEstacionar)
class HorasEstacionarAdmin(admin.ModelAdmin):
    list_display = ('descricao_horas', 'descricao_valor', 'ativo')
    ordering = ('valor', )


@admin.register(TipoNotificacao)
class TipoNotificacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descricao_titulo', 'ativo')
    ordering = ('tipo', )


@admin.register(ValoresCompra)
class ValoresCompraAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'ativo')
    ordering = ('valor', )
