from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.http import QueryDict
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from .models import Veiculo

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
        return render(request, self.retorno)


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

        newVeiculo = Veiculo(apelido=var_apelido, placa=var_placa, user=request.user)
        newVeiculo.save()

        veiculos = Veiculo.objects.all().filter(user=request.user.id)
        return render(request, self.retorno, {
            "veiculos": veiculos,
            "sucesso": "Cadastro de veículo com sucesso.",
        })

    def delete(self, request):
        
        var_delete = QueryDict(request.body)
        id_veiculo = var_delete.get('id_veiculo')

        # id_veiculo = request.POST.get('id_veiculo')
        delVeiculos = Veiculo.objects.get(id=id_veiculo)
        delVeiculos.delete()

        veiculos = Veiculo.objects.all().filter(user=request.user.id)
        return render(request, self.retorno, {
            "veiculos": veiculos,
            "sucesso": "Cadastro de veículo com sucesso.",
        })


class PageCarteira(View):
    retorno = 'carteira.html'
    def get(self, request):
        return render(request, self.retorno)


class PageComprar(View):
    retorno = 'comprar.html'
    def get(self, request):
        return render(request, self.retorno)