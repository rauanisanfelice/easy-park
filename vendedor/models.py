from django.db import models

from usuario.models import User, Parada, Veiculo

class PesquisaVeiculo(models.Model):
    db_table = 'pesquisaVeiculo'
    verbose_name_plural = 'pesquisasVeiculos'

    funcionario = models.ForeignKey(User, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, null=True)
    placa_pesquisa = models.CharField(max_length=10)
    data_pesquisa = models.TimeField(auto_now_add=True)

class VendaFuncionario(models.Model):
    db_table = 'vendafuncionario'
    verbose_name_plural = 'vendasfuncionario'

    funcionario = models.ForeignKey(User, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    parada = models.ForeignKey(Parada, on_delete=models.PROTECT)

    data_venda = models.TimeField(auto_now_add=True)