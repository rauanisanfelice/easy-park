from django.db import models
from django.contrib.auth.models import User


class InfoUsuario(models.Model):
    db_table = 'infoUsuario'
    
    estado =  models.CharField(max_length=100)
    cidade =  models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    telefone_ativo = models.BooleanField(default=False)
    email_ativo = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Funcionario(models.Model):
    db_table = 'funcionario'
    
    setor = models.CharField(max_length=20)
    fiscal = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Funcionários"


class Carteira(models.Model):
    db_table = 'carteira'

    valor = models.DecimalField(max_digits=6, decimal_places=2)
    saldo = models.DecimalField(max_digits=6, decimal_places=2)

    cho_status = [
        ('en', 'entrada'),
        ('sa', 'saida'),
    ]
    tipo_lancamento = models.CharField(choices=cho_status, max_length=2, default=cho_status[0][0])
    data_insercao = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Veiculo(models.Model):
    db_table = 'veiculo'
    
    placa = models.CharField(max_length=7)
    apelido = models.CharField(max_length=100)
    
    ativo = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)


class ValoresCompra(models.Model):
    db_table = 'valorescompra'

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    ativo = models.BooleanField(default=True)
    ordem = models.IntegerField()

    class Meta:
        verbose_name_plural = "Valores compras"

class HorasEstacionar(models.Model):
    db_table = 'horasestacionar'
    
    descricao_horas = models.CharField(max_length=100)
    horas = models.IntegerField()
    minutos = models.IntegerField()

    descricao_valor = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    
    ativo = models.BooleanField(default=True)
    ordem = models.IntegerField()

    class Meta:
        verbose_name_plural = "Horas estacionar"

class Parada(models.Model):
    db_table = 'parada'
    
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    quantidade_horas = models.ForeignKey(HorasEstacionar, on_delete=models.PROTECT)

    data_parada = models.DateTimeField(auto_now_add=True)
    hora_parada = models.TimeField(auto_now_add=True)
    valido = models.BooleanField(default=True)


class TipoNotificacao(models.Model):
    
    observacao_interna = models.CharField(max_length=150, null=True)
    descricao_titulo = models.CharField(max_length=100)
    descricao_full = models.CharField(max_length=250)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tipo notificações"


class Notificacao(models.Model):
    db_table = 'notificacao'
    verbose_name_plural = 'notificacoes'

    parada = models.ForeignKey(Parada, on_delete=models.PROTECT, null=True)
    placa = models.CharField(max_length=7, null=True)
    tipo_notificacao = models.ForeignKey(TipoNotificacao, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="notificao_user", null=True)
    funcionario = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    data_notificacao = models.DateTimeField(auto_now_add=True)
    data_lida = models.DateTimeField(null=True)