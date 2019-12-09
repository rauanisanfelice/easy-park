from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
    return redirect('login')

class home(View):
    retorno = 'home.html'
    def get(self, request):
        return render(request, self.retorno)


def novoUsuario():
    usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    usuario.save()

def changePassword():
    try:
        usuario = User.objects.get(username='')
        usuario.set_password('')
        usuario.save()
        return True
    except:
        return False

def authenticateUser():

    user = authenticate(username='john', password='secret')
    if user is not None:
        # A backend authenticated the credentials
        pass
    else:
        # No backend authenticated the credentials
        pass