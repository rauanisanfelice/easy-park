from django.shortcuts import render
from django.views.generic import View

from django.contrib.admin.views.decorators import staff_member_required

import logging
import datetime

logger = logging.getLogger(__name__)

class VerificaVeiculo(View):
    retorno = 'verifica.html'
    
    # @staff_member_required
    def get(self, request):
        return render(request, self.retorno)