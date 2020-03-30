# Generated by Django 3.0.3 on 2020-03-30 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HorasEstacionar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_horas', models.CharField(max_length=100)),
                ('horas', models.IntegerField()),
                ('minutos', models.IntegerField()),
                ('descricao_valor', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoNotificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('NOTIC', 'NOTIFICACAO'), ('ESGOT', 'ESGOTOU O TEMPO'), ('RETCA', 'RETIRAR O CARRO')], max_length=5)),
                ('descricao_titulo', models.CharField(max_length=100)),
                ('descricao_full', models.CharField(max_length=150)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValoresCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=7)),
                ('apelido', models.CharField(max_length=100)),
                ('ativo', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_parada', models.DateTimeField(auto_now_add=True)),
                ('hora_parada', models.TimeField(auto_now_add=True)),
                ('valido', models.BooleanField(default=True)),
                ('quantidade_horas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.HorasEstacionar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.Veiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_notificacao', models.DateTimeField(auto_now_add=True)),
                ('data_lida', models.DateTimeField(null=True)),
                ('funcionario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('paradas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.Parada')),
                ('tipo_notificao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.TipoNotificacao')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='notificao_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InfoUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(max_length=20)),
                ('fiscal', models.CharField(max_length=20)),
                ('ativo', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carteira',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tipo_lancamento', models.CharField(choices=[('en', 'entrada'), ('sa', 'saida')], default='en', max_length=2)),
                ('data_insercao', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
