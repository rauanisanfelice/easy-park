from django.db import models
from django.contrib.auth.models import User

class InfoUsuario(models.Model):
    db_table = 'infoUsuario'
    
    cidade =  models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Funcionario(models.Model):
    db_table = 'funcionario'

    setor = models.CharField(max_length=20)
    fiscal = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class Carteira(models.Model):
    db_table = 'carteira'

    valor = models.DecimalField(max_digits=15, decimal_places=2)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    cho_status = [
        ('en', 'entrada'),
        ('sa', 'saida'),
    ]
    tipo_lancamento = models.CharField(choices=cho_status, max_length=2, default=cho_status[0][0])
    data_insercao = models.DateTimeField(auto_now_add=True)

class Veiculo(models.Model):
    db_table = 'veiculo'
    
    placa = models.CharField(max_length=7)
    apelido = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class Parada(models.Model):
    db_table = 'parada'
    
    veiculos = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    data_parada = models.DateTimeField(auto_now_add=True)
    hora_parada = models.TimeField(auto_now_add=True)
    
    cho_quantidade_horas = [
        ('1h', 'uma hora'),
        ('1h:30min', 'uma hora e trinta minutos'),
        ('2h', 'duas horas'),
        ('2h:30min', 'duas horas e trinta minutos'),
        ('3h', 'três hora'),
        ('3h:30min', 'três horas e trinta minutos'),
        ('4h', 'quatro hora'),
    ]
    quantidade_horas = models.CharField(choices=cho_quantidade_horas, max_length=8, default=cho_quantidade_horas[0][0])

class Notificacao(models.Model):
    db_table = 'notificacao'
    verbose_name_plural = 'notificacoes'

    paradas = models.ForeignKey(Parada, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_notificacao = models.TimeField(auto_now_add=True)
    descricao_notificao =models.CharField(max_length=100)
    data_lida = models.TimeField(null=True)