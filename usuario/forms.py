from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ValoresCompra

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
