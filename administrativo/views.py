from django.shortcuts import render
from django.views.generic import View

from django.db.models import Sum, Count

from usuario.models import Carteira, Parada, TipoNotificacao, Notificacao, Funcionario
from vendedor.models import PesquisaVeiculo, VendaFuncionario
import calendar
import datetime

HORAS_VALIDAS_DIA = 8
DIAS_UTEIS_SEMANA = 6

class Dashboard(View):
    retorno = 'dashboard-summary.html'
    
    def get(self, request):
        mes_dias = datetime.datetime.now().month
        ano_dias = datetime.datetime.now().year
        if 'limpar' in request.GET:
            ano = None
            mes = None
        else:    
            ano = request.GET.get('ano', None)
            mes = request.GET.get('mes', None)    
            if ano: ano_dias = int(ano)
            if mes: mes_dias = int(mes)
                

        # NOTIFICAÇÕES E INFRAÇÕES
        tp_notificacao = TipoNotificacao.objects.get(tipo='NOTIC')
        tp_infracao = TipoNotificacao.objects.get(tipo='ALERT')

        # DESEMPENHO
        dias_mes = calendar.monthrange(ano_dias, mes_dias)[1]
        dias_validos = dias_mes - (DIAS_UTEIS_SEMANA % dias_mes)
        horas_validas = dias_validos * HORAS_VALIDAS_DIA

        # TODO DEIXAR UM FILTRO DE MES E ANO INICIALMENTE SELECIONADO PARA NAO FICAR PESADO AO CARREGAR A PAGINA
        # OBJETOS
        sum_valor_entradas = Carteira.objects.filter(tipo_lancamento='en')
        sum_valor_saidas = Carteira.objects.filter(tipo_lancamento='sa')
        sum_total_paradas = Parada.objects.all()
        sum_total_paradas_ativas = Parada.objects.filter(valido=True)
        sum_total_notificacoes = Notificacao.objects.filter(tipo_notificacao=tp_notificacao)
        sum_total_infracoes = Notificacao.objects.filter(tipo_notificacao=tp_infracao)
        sum_total_horas_paradas = Parada.objects.all()
        pesquisasFuncionarios = PesquisaVeiculo.objects.all()
        vendasFuncionarios = VendaFuncionario.objects.all()

        ##########################################
        # FILTROS
        if ano:
            # CREDITOS
            sum_valor_entradas = sum_valor_entradas.filter(data_insercao__year=ano)
            sum_valor_saidas = sum_valor_saidas.filter(data_insercao__year=ano)

            # PARADAS
            sum_total_paradas = sum_total_paradas.filter(data_parada__year=ano)
            sum_total_paradas_ativas = sum_total_paradas_ativas.filter(data_parada__year=ano)

            # NOTIFICAÇÕES E INFRAÇÕES
            sum_total_notificacoes = sum_total_notificacoes.filter(data_notificacao__year=ano)
            sum_total_infracoes = sum_total_infracoes.filter(data_notificacao__year=ano)

            # DESEMPENHO
            sum_total_horas_paradas = sum_total_horas_paradas.filter(data_parada__year=ano)

            # RANKING
            pesquisasFuncionarios = pesquisasFuncionarios.filter(data_pesquisa__year=ano)
            vendasFuncionarios = vendasFuncionarios.filter(data_venda__year=ano)
            
        if mes:
            # CREDITOS
            sum_valor_entradas = sum_valor_entradas.filter(data_insercao__month=mes)
            sum_valor_saidas = sum_valor_saidas.filter(data_insercao__month=mes)

            # PARADAS
            sum_total_paradas = sum_total_paradas.filter(data_parada__month=mes)
            sum_total_paradas_ativas = sum_total_paradas_ativas.filter(data_parada__month=mes)

            # NOTIFICAÇÕES E INFRAÇÕES
            sum_total_notificacoes = sum_total_notificacoes.filter(data_notificacao__month=mes)
            sum_total_infracoes = sum_total_infracoes.filter(data_notificacao__month=mes)

            # DESEMPENHO
            sum_total_horas_paradas = sum_total_horas_paradas.filter(data_parada__month=mes)

            # RANKING
            pesquisasFuncionarios = pesquisasFuncionarios.filter(data_pesquisa__month=mes)
            vendasFuncionarios = vendasFuncionarios.filter(data_venda__month=mes)

        
        ##########################################
        # AGGREGATE
        sum_valor_entradas = sum_valor_entradas.aggregate(Sum('valor'))['valor__sum']
        sum_valor_saidas = sum_valor_saidas.aggregate(Sum('valor'))['valor__sum']
        sum_total_paradas = sum_total_paradas.aggregate(Count('valido'))['valido__count']
        sum_total_paradas_ativas  = sum_total_paradas_ativas.aggregate(Count('valido'))['valido__count']
        sum_total_notificacoes = sum_total_notificacoes.aggregate(Count('tipo_notificacao'))['tipo_notificacao__count']
        sum_total_infracoes = sum_total_infracoes.aggregate(Count('tipo_notificacao'))['tipo_notificacao__count']
        sum_total_horas_paradas = sum_total_horas_paradas.aggregate(Sum('quantidade_horas__horas'), Sum('quantidade_horas__minutos'))
        pesquisasFuncionarios = pesquisasFuncionarios.values('funcionario__first_name').annotate(total=Count('funcionario__first_name')).order_by('total')[:5]
        vendasFuncionarios = vendasFuncionarios.values('funcionario__first_name', 'parada__quantidade_horas__valor').annotate(total=Count('funcionario__first_name'), sum=Count('parada__quantidade_horas__valor')).order_by('funcionario__first_name')[:5]

        ##########################################
        # CALCULOS
        if sum_valor_entradas == None: sum_valor_entradas = 0
        if sum_valor_saidas == None: sum_valor_saidas = 0
        if sum_total_paradas == None: sum_total_paradas = 0
        if sum_total_paradas_ativas == None: sum_total_paradas_ativas = 0
        if sum_total_notificacoes == None: sum_total_notificacoes = 0
        if sum_total_infracoes == None: sum_total_infracoes = 0

        # CREDITOS
        sum_valor_carteira = sum_valor_entradas - sum_valor_saidas

        # NOTIFICAÇÕES E INFRAÇÕES
        if sum_total_paradas ==  0:
            taxa_notificacoes = 0
            taxa_infracoes = 0
        else:
            taxa_notificacoes = float(((sum_total_notificacoes * 1) / sum_total_paradas) * 100)
            taxa_infracoes = float(((sum_total_infracoes * 1) / sum_total_paradas) * 100)

        # DESEMPENHO
        if not sum_total_horas_paradas['quantidade_horas__horas__sum'] and not sum_total_horas_paradas['quantidade_horas__minutos__sum']:
            total_horas_paradas = 0
        else:
            total_horas_paradas = sum_total_horas_paradas['quantidade_horas__horas__sum'] + (sum_total_horas_paradas['quantidade_horas__minutos__sum'] / 60)
        delta_horas_paradas = total_horas_paradas - horas_validas
                
        ##########################################
        return render(request, self.retorno, {
            "sum_valor_entradas": sum_valor_entradas,
            "sum_valor_carteira": sum_valor_carteira,
            "sum_valor_saidas": sum_valor_saidas,
            "sum_total_paradas": sum_total_paradas,
            "sum_total_paradas_ativas": sum_total_paradas_ativas,
            "sum_total_notificacoes": sum_total_notificacoes,
            "sum_total_infracoes": sum_total_infracoes,
            "taxa_notificacoes": format(taxa_notificacoes, '.2f'),
            "taxa_infracoes": format(taxa_infracoes, '.2f'),
            "horas_validas": horas_validas,
            "total_horas_paradas": total_horas_paradas,
            "delta_horas_paradas": delta_horas_paradas,
            "pesquisasFuncionarios": pesquisasFuncionarios,
            "vendasFuncionarios": vendasFuncionarios,
        })
    
    def post(self, request):
        return render(request, self.retorno)

