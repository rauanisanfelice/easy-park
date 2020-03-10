from django.db import models

from usuario.models import User, Parada

class pesquisaVeiculo(models.Model):
    db_table = 'pesquisaVeiculo'
    verbose_name_plural = 'pesquisasVeiculos'

    funcionario = models.ForeignKey(User, on_delete=models.PROTECT)
    paradas = models.ForeignKey(Parada, on_delete=models.PROTECT)
    data_pesquisa = models.TimeField(auto_now_add=True)