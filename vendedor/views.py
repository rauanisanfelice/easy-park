from django.shortcuts import render
from django.views.generic import View

from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Veiculo, Notificacao, TipoNotificacao, HorasEstacionar, Parada
from usuario.views import check_veiculo_horario
from .models import PesquisaVeiculo
from .forms import FormCompraCreditos

import logging
import datetime

logger = logging.getLogger(__name__)

class VerificaVeiculo(View):
    retorno = 'verifica.html'
    
    def get(self, request):
        return render(request, self.retorno)

    def post(self, request):
        placa = request.POST.get('placa')
        pesquisa = PesquisaVeiculo(funcionario=request.user,placa_pesquisa=placa)
        if not placa:
            pesquisa.save()
            return render(request, self.retorno, {
                "error": "True",
                "error_mensagem": "Campos vazios.",
                "acao": ""
            })
        else:
            veiculo = Veiculo.objects.filter(placa=placa)[:1]
            try: # verifica se possui veiculo cadastrado
                veiculo = veiculo[0]
            except:
                veiculo = None
            
            # SALVA PESQUISA COM O VEICULO
            pesquisa.veiculo = veiculo
            pesquisa.save()

            if not veiculo:
                return render(request, self.retorno, {
                    "error": "True",
                    "error_mensagem": "Veículo não esta cadastrado.",
                    "acao": "Realizar notificação via talão!",
                })
            else:
                if not veiculo.ativo:
                    return render(request, self.retorno, {
                        "error": "True",
                        "error_mensagem": "Veículo não esta cadastrado.",
                        "acao": "Realizar notificação via talão!",
                    })
                
                if check_veiculo_horario(request, None, veiculo):
                    tipo_not = TipoNotificacao.objects.get(tipo='ALERT')
                    notificacao = Notificacao(parada=None, tipo_notificacao=tipo_not, user=veiculo.user)
                    notificacao.save()
                    return render(request, self.retorno, {
                        "error": "True",
                        "error_mensagem": "Veículo não realizou uma parada.",
                        "acao": "Já realizamos a notificação via aplicativo!",
                    })
                else:
                    return render(request, self.retorno, {
                        "sucesso": "True",
                        "sucesso_mensagem": "Veículo possui uma parada.",
                    })
            

class VenderCreditos(View):
    retorno = 'vender.html'
    
    def get(self, request):
        form_class = FormCompraCreditos(user=request.user)
        return render(request, self.retorno, {
            "form": form_class,
        })

    def post(self, request):
        placa = request.POST.get('placa')
        hora = request.POST.get('horarios')
        hora_selecionada = HorasEstacionar.objects.get(id=hora)
        form_class = FormCompraCreditos(user=request.user)

        # CRIA VEICULO DA VENDA DO FUNCIONARIO
        try:
            veiculo = Veiculo(placa=placa, apelido='venda funcionario', ativo=True,user=None)
            veiculo.save()
        except:
            logger.error(f'Erro ao criar veiculo -  Placa do Veiculo ({placa})')
            return render(request, self.retorno, {
                "form": form_class,
                "error": "True",
                "error_mensagem": "Algo aconteceu de errado! Por gentileza tentar novamente mais tarde.",
            })
        
        # REALIZA A PARADA
        try:
            parada = Parada(veiculo=veiculo,user=None,quantidade_horas=hora_selecionada)
            parada.save()
        except:
            logger.error(f'Erro gerar Parada - Palca do Veiculo ({placa.id})')
            return render(request, self.retorno, {
                "form": form_class,
                "error": "True",
                "error_mensagem": "Algo aconteceu de errado! Por gentileza tentar novamente mais tarde.",
            })
        
        return render(request, self.retorno, {
            "form": form_class,
            "sucesso": "True",
            "sucesso_mensagem": "Compra de créditos realizada com sucesso.",
        })