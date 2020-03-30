from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.http import QueryDict, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .models import Veiculo, InfoUsuario, ValoresCompra, Carteira, Parada, Notificacao, TipoNotificacao
from .forms import *

import logging
import datetime
import pytz
import json
import threading
import time

logger = logging.getLogger(__name__)

@login_required
def index(request):
    return redirect('login')


def get_saldo_atual(request):
    carteira_usuario = Carteira.objects.filter(user=request.user.id).order_by('-data_insercao')
    if carteira_usuario.count() >= 1:
        ultima_compra = carteira_usuario[:1]
        saldo_atual = list(ultima_compra.values('saldo'))[0]['saldo']
    else:
        saldo_atual  = 0
    return format(saldo_atual, '.2f')


@login_required
def check_veiculo_horario(request, veiculo):
    paradas_veiculos = Parada.objects.filter(user=request.user.id, veiculo__id=veiculo.id).order_by('-id')[:1]
    if paradas_veiculos.count() == 0:
        return True
    else:
        data_parada = list(paradas_veiculos.values('data_parada'))[0]['data_parada']
        id_horas = list(paradas_veiculos.values('quantidade_horas'))[0]['quantidade_horas']

        quantidade_horas = HorasEstacionar.objects.get(id=id_horas)
        data_validar = data_parada + datetime.timedelta(hours=quantidade_horas.horas, minutes=quantidade_horas.minutos)
        
        # CONVERTE DATA PARA SAO PAULO
        hoje = datetime.datetime.now()
        hoje = hoje.astimezone(pytz.timezone('America/Sao_Paulo'))
        data_parada = data_parada.astimezone(pytz.timezone('America/Sao_Paulo'))
        data_validar = data_validar.astimezone(pytz.timezone('America/Sao_Paulo'))

        if hoje > data_parada and hoje < data_validar:
            # DENTRO DO PERIDO
            return False
        else:
            # FORA DO PERIDO
            return True


def triggerAlertaUsuario(request, parada, tipo_da_notificacao):
    id_veiculo = request.POST.get('veiculos')
    id_horarario = request.POST.get('horarios')
    
    veiculo = Veiculo.objects.get(id=id_veiculo)
    horarario = HorasEstacionar.objects.get(id=id_horarario)
    tipo_not = TipoNotificacao.objects.get(tipo=tipo_da_notificacao)

    notificacao = Notificacao(parada=parada, tipo_notificacao=tipo_not, user=request.user)
    notificacao.save()

    if tipo_da_notificacao == 'NOTIC':
        # AGENDA NOTIFICACAO
        data_notificar = parada.data_parada + datetime.timedelta(hours=parada.quantidade_horas.horas, minutes=parada.quantidade_horas.minutos)
        delay = (data_notificar.replace(tzinfo=None) - datetime.datetime.utcnow()).total_seconds()
        t = threading.Timer(delay, triggerAlertaUsuario, [request, parada.id, 'NOTIC'])
        t.start()

class Home(View):
    retorno = 'home.html'
    def get(self, request):
        return render(request, self.retorno)


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'


class PagePerfil(View):
    retorno = 'perfil.html'
    
    def get(self, request):
        usuario = User.objects.get(id=request.user.id)
        try:
            infousuario = InfoUsuario.objects.get(user=usuario)
            return render(request, self.retorno, {
                "infousuario": infousuario,
            })
        except:
            return render(request, self.retorno, {
                "infousuario": None,
            })
    
    def post(self, request):
        
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cidade = request.POST.get('cidade')
        
        usuario = User.objects.get(id=request.user.id)
        infousuario = InfoUsuario.objects.get(user=usuario)
        
        try:
            usuario.first_name = nome
            usuario.email = email
            if password:
                usuario.set_password(password)
                request.user.set_password(password)
            
            request.user.id = usuario.id
            request.user.first_name = nome
            request.user.email = email
            
            usuario.save()
            request.user.save()

            telefone = telefone.replace("(", "").replace(")","").replace(" ","").replace("-","")
            if infousuario:
                infousuario.telefone = telefone
                infousuario.cidade = cidade
                infousuario.save()
            else:
                telefone = "+55"+telefone
                infousuario = InfoUsuario(telefone=telefone, user=usuario, cidade=cidade)
                infousuario.save()

            
            return render(request, self.retorno, {
                "infousuario": infousuario,
                "sucesso": "True",
                "sucesso_mensagem": "Dados atualizados com sucesso.",
            })
        except:
            logger.error(f'Erro - Ao atualizar dados do usuario_id: {request.user.id}')
            return render(request, self.retorno, {
                "infousuario": infousuario,
                "error": "True",
                "error_mensagem": "Erro ao atualizar, por gentileza tente mais tarde.",
            })


class PageInformacoes(View):
    retorno = 'info.html'
    def get(self, request):
        return render(request, self.retorno)


class PageNotificacoes(View):
    retorno = 'notificacoes.html'
    def get(self, request):
        return render(request, self.retorno)


class PageHistorico(View):
    retorno = 'historico.html'
    def get(self, request):
        paradas = Parada.objects.filter(user=request.user.id).order_by('-data_parada')
        return render(request, self.retorno,{
            "paradas": paradas,
        })


class PageEstacionar(View):
    retorno = 'estacionar.html'

    def get(self, request):
        form_class = FormEstacionar(user=request.user)
        saldo_atual = get_saldo_atual(request)
        veiculos_ativos = Parada.objects.filter(user=request.user, valido=True)

        return render(request, self.retorno, {
            "form": form_class,
            "saldo": saldo_atual,
            "veiculos_ativos": veiculos_ativos,
        })
    
    def post(self, request):
        form_class = FormEstacionar(user=request.user)

        hora = request.POST.get('horarios')
        placa = request.POST.get('veiculos')
        
        saldo_atual = get_saldo_atual(request)
        veiculos_ativos = Parada.objects.filter(user=request.user, valido=True)

        # VERIFICA SE FOI SELECIONADO OS CAMPOS
        if hora and placa:
            hora_selecionada = HorasEstacionar.objects.get(id=hora)
            veiculo = Veiculo.objects.get(id=placa)

            # VERIFICA SE POSSUI SALDO
            if float(saldo_atual) >= hora_selecionada.valor.real:
                # VERIFICA SE JA POSSUI UMA PARADA
                if check_veiculo_horario(request, veiculo):
                    try:
                        # REALIZA PARADA
                        parada = Parada(veiculo=veiculo, quantidade_horas=hora_selecionada, user=request.user)
                        parada.save()

                        # ATUALIZA SALDO
                        saldo_atualizado = float(saldo_atual) - float(hora_selecionada.valor.real)
                        saldo_atual = saldo_atualizado
                        carteira_atualizar = Carteira(valor=hora_selecionada.valor.real, saldo=saldo_atualizado, tipo_lancamento='sa', user=request.user)
                        # carteira_atualizar.save()

                        # AGENDA NOTIFICACAO
                        data_notificar = parada.data_parada + datetime.timedelta(hours=parada.quantidade_horas.horas, minutes=parada.quantidade_horas.minutos - 5)
                        delay = (data_notificar.replace(tzinfo=None) - datetime.datetime.utcnow()).total_seconds()
                        t = threading.Timer(delay, triggerAlertaUsuario, [request, parada, 'NOTIC'])
                        t.start()
                        
                        return render(request, self.retorno, {
                            "form": form_class,
                            "saldo": saldo_atual,
                            "veiculos_ativos": veiculos_ativos,
                            "sucesso": "True",
                            "sucesso_mensagem": "Veículo ativo com sucesso.",
                        })
                    except:
                        logger.error(f'Erro ao estacionar - Usuario ID ({request.user.id}), Veiculo ID ({veiculo.id}), Parada ID ({parada.id})')
                        return render(request, self.retorno, {
                            "form": form_class,
                            "saldo": saldo_atual,
                            "veiculos_ativos": veiculos_ativos,
                            "error": "True",
                            "error_mensagem": "Erro ao estacionar o veículo.",
                        })

                else:
                    return render(request, self.retorno, {
                        "form": form_class,
                        "saldo": saldo_atual,
                        "veiculos_ativos": veiculos_ativos,
                        "error": "True",
                        "error_mensagem": "Veículo já está ativo.",
                    })

            else:
                return render(request, self.retorno, {
                    "form": form_class,
                    "saldo": saldo_atual,
                    "veiculos_ativos": veiculos_ativos,
                    "error": "True",
                    "error_mensagem": "Saldo insuficiente.",
                })
        else:
            return render(request, self.retorno, {
                "form": form_class,
                "saldo": saldo_atual,
                "veiculos_ativos": veiculos_ativos,
                "error": "True",
                "error_mensagem": "Campos vazios.",
            })


class PageVeiculo(View):
    retorno = 'veiculo.html'
    def get(self, request):
        veiculos = Veiculo.objects.all().filter(user=request.user.id, ativo=True)
        return render(request, self.retorno, {
            "veiculos": veiculos
        })
    
    def post(self, request):
        var_apelido = request.POST.get('apelido')
        var_placa = request.POST.get('placa')
        veiculos = Veiculo.objects.all().filter(user=request.user.id, ativo=True)

        if var_apelido or var_placa:
            newVeiculo = Veiculo(apelido=var_apelido, placa=var_placa, user=request.user)
            newVeiculo.save()
            
            return render(request, self.retorno, {
                "veiculos": veiculos,
                "sucesso": "True",
                "sucesso_mensagem": "Cadastro de veículo com sucesso.",
            })

        else:
            return render(request, self.retorno, {
                "veiculos": veiculos,
                "error": "True",
                "error_mensagem": "Campos vazios.",
            })
    
    def delete(self, request):
        
        # BUSCA O ID NO BODY DA REQUISIÇÃO 
        var_delete = QueryDict(request.body)
        id_veiculo = var_delete.get('id_veiculo')

        delVeiculos = Veiculo.objects.get(id=id_veiculo)        
        if check_veiculo_horario(request, delVeiculos):
            delVeiculos.ativo = False
            delVeiculos.save()
            retorno = { "retorno" : True }

        else:
            # VEICULO JA ESTA EM USO
            retorno = { "retorno" : False }
        
        return HttpResponse(json.dumps(retorno), content_type="application/json")

class PageCarteira(View):
    retorno = 'carteira.html'

    def get(self, request):
        saldo_atual = get_saldo_atual(request)
        carteira_usuario = Carteira.objects.filter(user=request.user.id).order_by('-data_insercao')
        return render(request, self.retorno, {
            "saldo": saldo_atual,
            "carteira_usuario": carteira_usuario,
        })


class PageComprar(View):
    retorno = 'comprar.html'

    def get(self, request):
        form_class = FormCompras
        saldo_atual = get_saldo_atual(request)
        return render(request, self.retorno, {
            "form": form_class,
            "saldo": saldo_atual,
        })

    def post(self, request):
        valor_id = request.POST.get('valores')
        valor_compra = ValoresCompra.objects.get(id=valor_id)

        carteira_usuario = Carteira.objects.filter(user=request.user.id).order_by('-data_insercao')[:1]
        if carteira_usuario.count() == 1:
            saldo_atual = list(carteira_usuario.values('saldo'))[0]['saldo'] + valor_compra.valor
        else:
            saldo_atual  = valor_compra.valor

        usuario = User.objects.get(id=request.user.id)
        carteira_usuario = Carteira(saldo=float(saldo_atual), valor=float(valor_compra.valor), user=usuario, tipo_lancamento='en')
        carteira_usuario.save()
        
        form_class = FormCompras
        return render(request, self.retorno, {
            "form": form_class,
            "saldo": saldo_atual,
            "sucesso": "True",
            "sucesso_mensagem": "Compra realizada.",
        })
