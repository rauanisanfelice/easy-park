from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.http import QueryDict, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .models import Veiculo, InfoUsuario, ValoresCompra, Carteira
from .forms import *

import json

def index(request):
    return redirect('login')


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
        return render(request, self.retorno)


class PageEstacionar(View):
    retorno = 'estacionar.html'
    def get(self, request):
        return render(request, self.retorno)

class PageVeiculo(View):
    retorno = 'veiculo.html'
    def get(self, request):
        veiculos = Veiculo.objects.all().filter(user=request.user.id)
        return render(request, self.retorno, {
            "veiculos": veiculos
        })
    
    def post(self, request):
        var_apelido = request.POST.get('apelido')
        var_placa = request.POST.get('placa')
        veiculos = Veiculo.objects.all().filter(user=request.user.id)

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
        delVeiculos.delete()

        retorno = { "retorno" : True }
        return HttpResponse(json.dumps(retorno), content_type="application/json")


class PageCarteira(View):
    retorno = 'carteira.html'

    def get(self, request):

        carteira_usuario = Carteira.objects.filter(user=request.user.id).order_by('-data_insercao')
        ultima_compra = carteira_usuario[:1]
        saldo_atual = list(ultima_compra.values('saldo'))[0]['saldo']

        return render(request, self.retorno, {
            "saldo": saldo_atual,
            "carteira_usuario": carteira_usuario,
        })


class PageComprar(View):
    retorno = 'comprar.html'

    def get(self, request):
        form_class = FormCompras
        carteira_usuario = Carteira.objects.filter(user=request.user.id).order_by('-data_insercao')[:1]
        saldo_atual = list(carteira_usuario.values('saldo'))[0]['saldo']
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

        carteira_usuario = Carteira(saldo=float(saldo_atual), valor=float(valor_compra.valor), user=request.user, tipo_lancamento='en')
        carteira_usuario.save()
        
        form_class = FormCompras
        return render(request, self.retorno, {
            "form": form_class,
            "saldo": saldo_atual,
            "sucesso": "True",
            "sucesso_mensagem": "Compra realizada.",
        })
