# Generated by Django 3.0.3 on 2020-03-10 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pesquisaVeiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pesquisa', models.TimeField(auto_now_add=True)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('paradas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuario.Parada')),
            ],
        ),
    ]
