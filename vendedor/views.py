from django.shortcuts import render
from django.views.generic import View

from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Veiculo, Notificacao, TipoNotificacao, HorasEstacionar, Parada
from usuario.views import check_veiculo_horario
from .models import PesquisaVeiculo, VendaFuncionario
from .forms import FormCompraCreditos

import logging
import datetime

logger = logging.getLogger(__name__)

class VerificaVeiculo(View):
    template_name = 'verifica.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        placa = request.POST.get('placa')
        pesquisa = PesquisaVeiculo(funcionario=request.user,placa_pesquisa=placa)
        context = {}
        if not placa:
            pesquisa.save()

            context['error'] = True
            context['error_mensagem'] = "Campos vazios."
            context['acao'] = ""
        else:
            veiculo = Veiculo.objects.filter(placa=placa, ativo=True)[:1]
            try: # verifica se possui veiculo cadastrado
                veiculo = veiculo[0]
            except:
                veiculo = None
            
            # SALVA PESQUISA COM O VEICULO
            pesquisa.veiculo = veiculo
            pesquisa.save()

            if veiculo:
                if veiculo.user:
                    if check_veiculo_horario(request, None, veiculo):
                        tipo_not = TipoNotificacao.objects.get(id=3)
                        notificacao = Notificacao(parada=None, tipo_notificacao=tipo_not, user=veiculo.user)
                        notificacao.save()

                        context['error'] = True
                        context['error_mensagem'] = "Veículo não realizou uma parada."
                        context['acao'] = "Já realizamos a notificação via aplicativo!"
                        context['aplicativo'] = "aplicativo"
                    else:
                        context['sucesso'] = True
                        context['sucesso_mensagem'] = "Veículo possui uma parada."
                else:
                    context['error'] = True
                    context['error_mensagem'] = "Veículo não esta cadastrado."
                    context['acao'] = "Realizar notificação via talão!"
            else:
                # VEICULO NÃO CADASTRADO
                try:
                    tipo_not = TipoNotificacao.objects.get(id=4)
                    notificacao = Notificacao(parada=None, tipo_notificacao=tipo_not, placa=placa)
                    notificacao.save()
                except:
                    logger.error(f'Erro ao noticar veiculo nao cadastrado - Placa ({placa}) - Id Funcionario ({request.user.id})')
                context['error'] = True
                context['error_mensagem'] = "Veículo não esta cadastrado."
                context['acao'] = "Realizar notificação via talão!"
                
        return render(request, self.template_name, context=context)
            

class VenderCreditos(View):
    template_name = 'vender.html'
    
    def get(self, request):
        form_class = FormCompraCreditos(user=request.user)
        return render(request, self.template_name, { "form": form_class, })

    def post(self, request):
        context = {}
        placa = request.POST.get('placa')
        hora = request.POST.get('horarios')
        hora_selecionada = HorasEstacionar.objects.get(id=hora)
        form_class = FormCompraCreditos(user=request.user)
        context['form'] = form_class

        # CRIA VEICULO DA VENDA DO FUNCIONARIO
        veiculo = Veiculo(placa=placa, apelido='venda funcionario', ativo=True,user=None)
        parada = Parada(veiculo=veiculo,user=None,quantidade_horas=hora_selecionada)
        venda = VendaFuncionario(funcionario=request.user, veiculo=veiculo, parada=parada)
        
        # REALIZA A PARADA
        try:
            veiculo.save()
            parada.save()
            venda.save()
            context['sucesso'] = True
            context['sucesso_mensagem'] = "Compra de créditos realizada com sucesso."

        except:
            context['error'] = True
            context['error_mensagem'] = "Algo aconteceu de errado! Por gentileza tentar novamente mais tarde."
            logger.error(f'Erro gerar Parada - Placa do Veiculo ({placa}) - Id Hora ({hora}) - Funcionario {request.user.id}')

        return render(request, self.retorno, context=context)