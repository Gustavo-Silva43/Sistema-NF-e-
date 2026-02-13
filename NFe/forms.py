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
        fields = [
            'item_pedido',
            'codigo_produto',
            'ean',
            'descricao',
            'ncm',
            'nve',
            'tipi',
            'cfop',
            'unidade',
            'quantidade',
            'valor_unitario',
            'valor_total_bruto',
            'unidade_tributo',
            'quantidade_tributo',
            'valor_unitario_tributo',
            'valor_frete',
            'valor_seguro',
            'valor_desconto',
            'valor_outros',
            'numero_pedido_compra',
            'item_pedido_compra',
            'fci',
            'valor_tributos_estimado',
            'origem_mercadoria',
            'cst_operacao',
            'icms_bc',
            'icms_percentual',
            'icms_valor',
            'icms_st_bc',
            'icms_st',
            'icms_st_red_bc',
            'icms_st_valor',
            'icms_st_percentual',
            'pis_cst',
            'pis_bc',
            'pis_percentual',
            'pis_valor',
            'cofins_cst',
            'cofins_bc',
            'cofins_percentual',
            'cofins_valor',
            'icms_uf_dest_bc',
            'icms_uf_dest_p_fcp',
            'icms_uf_dest_p_inter',
            'icms_uf_dest_p_inter_part',
            'icms_uf_dest_v_fcp',
            'icms_uf_dest_v_icms',
            'icms_uf_remet_v_icms',
            'di_numero',
            'di_data',
            'di_local_desemb',
            'di_uf_desemb',
            'di_data_desemb',
        ]
        widgets = {}

ProdutoFormSet = inlineformset_factory(NFe, Produto, form=ProdutoForm, extra=10)
