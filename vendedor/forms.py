from django import forms
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from usuario.models import HorasEstacionar

class FormCompraCreditos(forms.Form):
    
    horarios = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.RadioSelect,
    )
    
    def __init__(self, user, *args, **kwargs):
        super(FormCompraCreditos, self).__init__(*args, **kwargs)
        self.fields['horarios'].choices = HorasEstacionar.objects.filter(ativo=True).annotate(resultado=Concat('descricao_horas', V(' - '), 'descricao_valor')).order_by('ordem').values_list('id','resultado')
