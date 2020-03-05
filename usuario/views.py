from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views import generic
from .forms import *



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


class Perfil(View):
    retorno = 'perfil.html'
    def get(self, request):
        return render(request, self.retorno)


class Informacoes(View):
    retorno = 'info.html'
    def get(self, request):
        return render(request, self.retorno)


class Notificacoes(View):
    retorno = 'notificacoes.html'
    def get(self, request):
        return render(request, self.retorno)


class Historico(View):
    retorno = 'historico.html'
    def get(self, request):
        return render(request, self.retorno)


class Estacionar(View):
    retorno = 'estacionar.html'
    def get(self, request):
        return render(request, self.retorno)

class Veiculo(View):
    retorno = 'veiculo.html'
    def get(self, request):
        return render(request, self.retorno)

class Carteira(View):
    retorno = 'carteira.html'
    def get(self, request):
        return render(request, self.retorno)


class Comprar(View):
    retorno = 'comprar.html'
    def get(self, request):
        return render(request, self.retorno)