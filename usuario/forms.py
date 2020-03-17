from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

from .models import ValoresCompra, HorasEstacionar, Veiculo

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2', )


class FormCompras(forms.Form):
    
    required_css_class = ''
    
    valores = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(FormCompras, self).__init__(*args, **kwargs)
        self.fields['valores'].choices = ValoresCompra.objects.filter(ativo=True).order_by('ordem').values_list('id','descricao')


class FormEstacionar(forms.Form):
    
    horarios = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.RadioSelect,
    )

    veiculos = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(),
    )

    def __init__(self, user, *args, **kwargs):
        super(FormEstacionar, self).__init__(*args, **kwargs)
        self.fields['horarios'].choices = HorasEstacionar.objects.filter(ativo=True).annotate(resultado=Concat('descricao_horas', V(' - '), 'descricao_valor')).order_by('ordem').values_list('id','resultado')
        self.fields['veiculos'].choices = Veiculo.objects.filter(user=user, ativo=True).values_list('id','placa')
