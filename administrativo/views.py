from django.shortcuts import render
from django.views.generic import View

from django.db.models import Sum, Count

from usuario.models import Carteira, Parada, TipoNotificacao, Notificacao

import calendar
import datetime

HORAS_VALIDAS_DIA = 8
DIAS_UTEIS_SEMANA = 6

class Dashboard(View):
    retorno = 'dashboard-summary.html'
    
    def get(self, request):
        
        # CRÉDITOS
        sum_valor_entradas = Carteira.objects.filter(tipo_lancamento='en').aggregate(Sum('valor'))
        sum_valor_saidas = Carteira.objects.filter(tipo_lancamento='sa').aggregate(Sum('valor'))
        sum_valor_carteira = sum_valor_entradas['valor__sum'] - sum_valor_saidas['valor__sum']
        
        # PARADAS
        sum_total_paradas = Parada.objects.all().aggregate(Count('valido'))
        sum_total_paradas_ativas = Parada.objects.filter(valido=True).aggregate(Count('valido'))

        # NOTIFICAÇÕES E INFRAÇÕES
        tp_notificacao = TipoNotificacao.objects.get(tipo='NOTIC')
        tp_infracao = TipoNotificacao.objects.get(tipo='ALERT')
        sum_total_notificacoes = Notificacao.objects.filter(tipo_notificacao=tp_notificacao).aggregate(Count('tipo_notificacao'))
        sum_total_infracoes = Notificacao.objects.filter(tipo_notificacao=tp_infracao).aggregate(Count('tipo_notificacao'))

        taxa_notificacoes = float(((sum_total_notificacoes['tipo_notificacao__count'] * 1) / sum_total_paradas['valido__count']) * 100)
        taxa_infracoes = float(((sum_total_infracoes['tipo_notificacao__count'] * 1) / sum_total_paradas['valido__count']) * 100)

        # DESEMPENHO
        ano_atual = datetime.datetime.now().year
        mes_atual = datetime.datetime.now().month
        dias_mes = calendar.monthrange(ano_atual, mes_atual)

        dias_validos = dias_mes[1] - (DIAS_UTEIS_SEMANA % dias_mes[1])
        horas_validas = dias_validos * HORAS_VALIDAS_DIA

        sum_total_horas_paradas = Parada.objects.all().aggregate(Sum('quantidade_horas__horas'), Sum('quantidade_horas__minutos'))
        total_horas_paradas = sum_total_horas_paradas['quantidade_horas__horas__sum'] + (sum_total_horas_paradas['quantidade_horas__minutos__sum'] / 60)
        delta_horas_paradas = total_horas_paradas - horas_validas

        return render(request, self.retorno, {
            "sum_valor_entradas": sum_valor_entradas['valor__sum'],
            "sum_valor_carteira": sum_valor_carteira,
            "sum_valor_saidas": sum_valor_saidas['valor__sum'],
            "sum_total_paradas": sum_total_paradas['valido__count'],
            "sum_total_paradas_ativas": sum_total_paradas_ativas['valido__count'],
            "sum_total_notificacoes": sum_total_notificacoes['tipo_notificacao__count'],
            "sum_total_infracoes": sum_total_infracoes['tipo_notificacao__count'],
            "taxa_notificacoes": format(taxa_notificacoes, '.2f'),
            "taxa_infracoes": format(taxa_infracoes, '.2f'),
            "horas_validas": horas_validas,
            "total_horas_paradas": total_horas_paradas,
            "delta_horas_paradas": delta_horas_paradas,
        })
    
    def post(self, request):
        return render(request, self.retorno)

