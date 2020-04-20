from django.shortcuts import render
from django.views.generic import View

class Dashboard(View):
    retorno = 'dashboard-summary.html'
    
    def get(self, request):
        return render(request, self.retorno)
    
    def post(self, request):
        return render(request, self.retorno)

