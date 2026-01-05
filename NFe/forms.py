from django import forms
from django.forms import inlineformset_factory
from. models import NFe, Cliente, ItemNFe, Transportadora, Volume, Duplicata

# Form principal da NF-e - só os campos gerais
class NFeForm(forms.ModelForm):
    class Meta:
        model = NFe
        fields = [
            'numero', 'serie','natureza_operacao',
            'valor_desconto', 'valor_frete', 'valor_seguro', 'outras_despesas',
            'informacoes_complementares', 'infornacoes_fisico'
        ]
        widgets = {
            'informacoes_complementares': forms.Textarea(attrs={'rows':4}),
            'informacoes_fisico': forms.Textarea(attrs={'rows': 3}),
        }
# Cliente pode ser novoou existente - Vamos permitir criar na hora
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'completamento': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }
# Itens da NF-e - vários
class ItemNFeForm(forms.ModelForm):
    class Meta:
        model = ItemNFe
        fields = ['numero_item', 'codigo_produto', 'descricao', 'ncm', 'cfop', 'unidade', 'valor_unitario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'size':'60'})

# Formsets - pra lidar com múltiplos itens, volumes e duplicatas
ItemNFeFormSet = inlineformset_factory( 
    NFe, ItemNFe, form=ItemNFeForm,
    extra=5, can_delete=True, min_num=1, validade_min=True
)

VolumeFormSet = inlineformset_factory(
    Transportadora, Volume,
    fields = ['quantidade', 'especie', 'marca', 'numeracao', 'peso_liquido', 'peso_bruto'],
    extra=3, can_delete=True
)

DuplicataFormSet = inlineformset_factory(
    NFe, Duplicata,
    fields = ['numero', 'data_vecimento', 'valor'],
    extra=3, can_delete=True
)

class TransPortadoraForm(forms.ModelFrom):
    class Meta:
        model = Transportadora
        fields = ['nome', 'cnpj', 'ie', 'logradouro', 'municipio', 'uf', 'tipo-frete']

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
