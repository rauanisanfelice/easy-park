from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class index(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)
