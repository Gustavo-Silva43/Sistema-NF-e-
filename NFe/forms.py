from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import *
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class NFeForm(forms.ModelForm):
    class Meta:
        model = NFe
        fields = '__all__'
        widgets = {
            'data_emisssão': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-nfe'}),
            'justificativa': forms.Textarea(attrs={'rows': 2, 'class': 'textarea-nfe'}),
        }

class TransportadoraForm(forms.ModelForm):
    class Meta:
        model = Transportadora_Volumes
        fields = '__all__'
        exclude = ['nfe']
        widgets = {
            'tipo_frete': forms.TextInput(attrs={'class': 'input-nfe-blue'}),
            'nome_transportadora': forms.TextInput(attrs={'class': 'input-nfe-blue'}),
            'cnpj_transporadora': forms.TextInput(attrs={'class': 'input-nfe-blue'}),
            'placa_video': forms.TextInput(attrs={'class': 'input-nfe-blue'})
        }
class CobrancaForm(forms.ModelForm):
    class Meta:
        model = Cobranca
        fields = '__all__'
        widgets = {
            'id_banco': forms.TextInput(attrs={'class': 'input-nfe-blue'}),
        }
class InfoStatusForm(forms.ModelForm):
    class Meta:
        model = Info_nfe
        fields = ['informacoes_nfe', 'retorno']
        widgets ={
            'informacoes_nfe': forms.Textarea(attrs={'rows': 4, 'class': 'textarea-status'}),
            'retorno': forms.Textarea(attrs={'rows': 4, 'class': 'textarea-status'}),
        }

class ProdutoForm(forms.ModelForm):
   class Meta:
        model = Produto
        fields = ['item_pedido', 'codigo_produto', 'descricao', 'ncm', 'cfop', 'unidade', 'quantidade', 'valor_unitario', 'valor_total_bruto', 'unidade_tributo', 'quantidade_tributo', 'valor_unitario_tributo']
        widgets = {}

ProdutoFormSet = inlineformset_factory(NFe, Produto, form=ProdutoForm, extra=1)
