from django import forms
from django.forms import inlineformset_factory
from. models import NFe, Cliente, ItemNFe, Transportadora, Volume, Duplicata, Emitente

class NFeForm(forms.ModelForm):
    class Meta:
        model = NFe
        # Certifique-se de incluir os novos campos na lista 'fields'
        fields = [
            'pedido', 'numero', 'serie', 'modelo', 'tipo_emissao', 
            'tipo_nfe', 'finalidade', 'natureza_operacao',
            'presenca_comprador', 'operacao_consumidor', 'local_destino',
            'referenciar_nfe', 'transmitir', 'cce', 'cancelar', # Novos campos aqui
            'justificativa', 'data_emissao'
        ]
        
        # Define como cada campo deve aparecer (Widgets)
        widgets = {
            # Os "quadradinhos" de marcar
            'transmitir': forms.CheckboxInput(attrs={'class': 'check-nfe'}),
            'cce': forms.CheckboxInput(attrs={'class': 'check-nfe'}),
            'cancelar': forms.CheckboxInput(attrs={'class': 'check-nfe'}),
            'operacao_consumidor': forms.CheckboxInput(attrs={'class': 'check-nfe'}),
            'referenciar_nfe': forms.CheckboxInput(attrs={'class': 'check-nfe'}),
            
            # Campos de texto com estilo de grade
            'pedido': forms.TextInput(attrs={'class': 'input-cell'}),
            'natureza_operacao': forms.TextInput(attrs={'class': 'input-cell'}),
            'justificativa': forms.Textarea(attrs={'class': 'input-cell', 'rows': 2}),
            
            # Campo de data especial para o navegador
            'data_emissao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-cell'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se quiser remover os labels automáticos para usar apenas os da tabela azul:
        # for field in self.fields:
        #     self.fields[field].label = '



        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'completamento': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }
class ItemNFeForm(forms.ModelForm):
    class Meta:
        model = ItemNFe
        fields = ['item_pedido', 'produto', 'descricao','quantidade', 'valor_unitario', 'valor_total_bruto']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'descricao' in self.fields:
            self.fields['descricao'].widget.attrs.update({'size':'60'})

ItemNFeFormSet = inlineformset_factory( 
    NFe, ItemNFe, form=ItemNFeForm,
    extra=5, can_delete=True, min_num=1, validate_min=True
)

VolumeFormSet = inlineformset_factory(
    Transportadora, Volume,
    fields = ['quantidade', 'especie', 'marca', 'numeracao', 'peso_liquido', 'peso_bruto'],
    extra=3, can_delete=True
)

DuplicataFormSet = inlineformset_factory(
    NFe, Duplicata,
    fields = ['numero', 'data_vencimento', 'valor'],
    extra=3, can_delete=True
)

class TransportadoraForm(forms.ModelForm):
    class Meta:
        model = Transportadora
        fields = ['nome', 'cnpj', 'ie', 'logradouro', 'municipio', 'uf', 'tipo_frete']

class EmitenteForm(forms.ModelForm):
    class Meta:
        model = Emitente
        fields = '__all__'
        widgets = {
            'cnpj':forms.TextInput(attrs={'class': 'input-cell'}),
            'nome_razao':forms.TextInput(attrs={'class': 'Input-cell'}),
        }

# Este arquivo forms.py é onde o Django define como os dados serão inseridos pelo usuário no navegador. Ele transforma os seus Models em formulários HTML automáticos e utiliza Formsets para permitir que você adicione vários itens (como produtos ou duplicatas) em uma única tela.

# # 1. Importações e Configurações Iniciais
# from django import forms: Importa as ferramentas básicas de formulário do Django.
# from django.forms import inlineformset_factory: Esta é uma função poderosa que cria um conjunto de formulários relacionados (ex: vários itens dentro de uma nota).
# from .models import ...: Importa os modelos que você criou anteriormente para que o formulário saiba quais campos exibir.

# 2. NFeForm (O Cabeçalho da Nota)
# class NFeForm(forms.ModelForm):: Define que este formulário é baseado no modelo NFe.
# fields = [...]: Lista apenas os campos gerais da nota (número, série, valores totais).
# widgets = { ... }: Personaliza a aparência. Aqui, ele transforma os campos de informações complementares em caixas de texto maiores (Textarea) com um número específico de linhas (rows).


# 3. ClienteForm (Dados do Destinatário)
# fields = '__all__': Diferente do anterior, este diz ao Django para exibir todos os campos da tabela Cliente.
# attrs={'placeholder': 'Opcional'}: Adiciona aquela dica cinza dentro da caixa de texto, avisando ao usuário que ele não é obrigado a preencher..

# 4. ItemNFeForm (Os Produtos na Nota)
# def __init__(self, ...):: Este é o inicializador do formulário.
# self.fields['descricao'].widget.attrs.update({'size':'60'}): Ele altera o tamanho visual do campo de descrição no navegador para que ele fique mais comprido (60 caracteres de largura).

# # 5. Os Formsets (Múltiplos Registros)
# O inlineformset_factory liga um modelo "Pai" a um "Filho".
    # ItemNFeFormSet: Liga a NFe aos seus ItemNFe.
        # extra=5: Mostra 5 linhas em branco por padrão para o usuário preencher.
        # can_delete=True: Adiciona uma caixinha para o usuário excluir um item da lista.
        # min_num=1: Obriga que a nota tenha pelo menos 1 item para ser válida.
# VolumeFormSet: Liga a Transportadora aos Volume (caixas, paletes, etc).
# DuplicataFormSet: Liga a NFe às parcelas de pagamento (Duplicata).

# 6. TransportadoraForm
# class TransportadoraForm(forms.ModelForm):: Cria o formulário para os dados da empresa que fará o frete.



from django import forms
from .models import *

class NfeForm(forms.ModelForm):
    class Meta:
        model = NFe
        fields = '__all_'
        widgets = {
            'data_emisssão': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-nfe'}),
            'justificativa': forms.Textearea(attrs={'rows': 2, 'class': 'textarea-nfe'}),
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
        widgets =
