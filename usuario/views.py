from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

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
    retorno = 'blank.html'
    def get(self, request):
        return render(request, self.retorno)
