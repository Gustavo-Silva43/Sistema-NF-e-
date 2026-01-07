from django.db import models
from decimal import Decimal

# class Emitente(models.Model): Define a criação da classe (tabela). Ao herdar de models.Model, o Django entende que deve criar uma tabela no banco de dados para esse objeto.
# nome_razao = models.CharField("Nome / Razão Social", max_length=200) Cria um campo de texto curto (CharField). O primeiro argumento é o "verbose name", que é o nome que aparecerá nos formulários do Django Admin. O max_length=200 limita o nome a 200 caracteres.
# nome_fantasia = mod
# els.CharField(max_length=200, blank=True) Outro campo de texto. O blank=True indica que este campo não é obrigatório, ou seja, você pode deixar o nome fantasia em branco.
# cnpj = models.CharField("CNPJ", max_length=14) Campo para armazenar os 14 dígitos do CNPJ. Geralmente usamos CharField em vez de IntegerField para documentos para manter zeros à esquerda e evitar problemas de cálculo.
# inscricao_estadual = models.CharField("IE", max_length=20) Campo para a Inscrição Estadual da empresa.
# logradouro, numero, bairro, municipio: Campos de texto padrão para o endereço (Rua, Número, Bairro e Cidade).
# uf = models.CharField(max_length=2) Campo para a Unidade Federativa (Estado), limitado a 2 caracteres (ex: "SP", "RJ").
# cep = models.CharField(max_length=8) Campo para o CEP, armazenando apenas os 8 números.
# telefone - models.CharField(max_length=20, blank=True). Atenção: Aqui há um erro de sintaxe. Você usou um sinal de menos - em vez de igual =. O correto é telefone = models.CharField(...). Serve para salvar o contato telefônico
# def __str__(self): Este é um método especial do Python. Ele define como o objeto será exibido como uma "string" (texto) quando você o visualizar no Django Admin ou em um print.
class Emitente(models.Model):
    nome_razao = models.CharField("Nome / Razão Social", max_length=200)
    nome_fantasia = models.CharField(max_length= 200, blank=True)
    cnpj = models.CharField("CNPJ", max_length=14)
    inscricao_estadual = models.CharField("IE", max_length=20)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.razao_social

# O primeiro bloco de codigo
# então, ele e um bloco de codigo que mostra como vai ser o banco, de forma que o django puxer para o framework que o django e são a mesma. 
# voltando, ele vai mostrar par o db.sqlite3, como deve ser o banco de dados atraves do model, que foi colocando no bloco de codigo para leia de forma mais facil que é o sqlite3
# O Django utiliza um conceito chamado ORM (Object-Relational Mapper). Em português, é como um "Mapeador de Objetos para o Relacional".

# Sem o método __str__, quando o Django precisasse mostrar um cliente (no painel administrativo ou em um erro), ele exibiria algo genérico e difícil de ler, como: <Cliente: Cliente object (1)>.


#Este modelo Cliente é muito parecido com o anterior, mas traz alguns conceitos novos e importantes do Django, como o tratamento de campos vazios no banco de dados (null) e tipos de campos diferentes (EmailField e TextField).

# Campos de Texto Curto (CharField): A maioria dos campos usa models.CharField, que é para textos de uma única linha.

# nome_razão = models.CharField("Nome / Razão Social", max_length=200) O primeiro texto entre aspas é o "apelido" do campo que aparece no sistema (label). Atenção: Evite usar acentos em nomes de variáveis (use nome_razao).

# nome_fantasia = ... blank=True, null=True blank=True: O formulário aceita ficar vazio. null=True: O banco de dados aceita gravar o valor como "Nulo" (ausência de dado).

# cpf_cnpj, inscricao_estadual, inscricao_municipal: Campos para documentos fiscais. Note que inscricao_municipal tem um erro de digitação no seu código: falta o ponto (models.CharField).

# logradouro, numero, complemento, bairro, Municipio, uf, cep: Bloco de informações de endereço.

# cod_ibge_municipio: Campo específico para o código numérico do IBGE (usado em Notas Fiscais Eletrônicas).

# email = models.EmailField(blank=True, null=True) Diferente do CharField, o Django valida automaticamente se o que foi digitado é um e-mail válido (contém "@", domínio, etc).

# informacao_estrangeira = models.TextField(blank=True, null=True) TextField: É usado para textos longos ou observações. Ao contrário do CharField, ele não tem um limite rígido de caracteres e cria uma caixa de texto maior na tela.

# def __str__(self): return self.nome_razao Diz ao Django: "Sempre que precisar mostrar este cliente em uma lista, mostre o Nome/Razão Social dele".

class Cliente(models.Model):
    nome_razão = models.CharField("Nome / Razão Social", max_length=200)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=200, blank=True, null=True)
    cpf_cnpj = models.CharField("CPF/ CNPJ", max_length=14)
    inscricao_estadual = models.CharField("Inscrição Estadual", max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField("Inscrição Municipal", max_length=20, blank=True, null=True)
    logradouro = models.CharField("Logradouro", max_length=200)
    numero = models.CharField("Número", max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField("Bairro",max_length=100)
    cod_ibge_municipio = models.CharField("Cód. IBGE Município", max_length=7, blank=True)
    Municipio = models.CharField("Município", max_length=100)
    uf = models.CharField("UF", max_length=2)
    cep = models.CharField("CEP", max_length=8)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    informacao_estrangeira = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_razao

# esse model, dessa parte do codigo, esta mostrando como deve ser o banco, que na verdade ele vai ser assim já. esse e a tabela cliente, como vai ficar ele.
# "Você está 100% certo! Esse código é exatamente o "mapa" ou a "planta baixa" que diz ao banco de dados: "Crie uma tabela chamada Cliente com estas colunas e estas regras"."

# Sem o método __str__, quando o Django precisasse mostrar um cliente (no painel administrativo ou em um erro), ele exibiria algo genérico e difícil de ler, como: <Cliente: Cliente object (1)>.

# class Produto(models.Model): Declara que a classe Produto é um modelo de banco de dados. O Django usará isso para criar uma tabela chamada, geralmente, appname_produto.

# codigo (CharField): Armazena o código de identificação do produto.
# max_length=20: Define o limite máximo de 20 caracteres.
#"Cód. Produto": É o nome amigável (verbose name) que aparecerá em formulários ou no painel administrativo.

# descricao (CharField): Um campo de texto para o nome ou detalhamento do produto, com limite de 300 caracteres.

# ncm e cfop: Campos de texto curtos para códigos fiscais brasileiros (Nomenclatura Comum do Mercosul e Código Fiscal de Operações e Prestações). Note que o ncm tem 8 caracteres e o cfop tem 4, seguindo o padrão nacional.

# unidade (CharField): Para armazenar a unidade de medida (ex: "UN", "KG", "L").

# valor_unitario (DecimalField): Usado para valores monetários/financeiros.
# max_digits=12: O número total de dígitos permitidos (ex: 999.999.999,99).
# decimal_places=2: Fixa duas casas decimais após a vírgula (centavos).

class Produto(models.Model):
    codigo = models.CharField("Cód. Produto", max_length=20)
    descricao = models.CharField("Descrição do Produto", max_length=300)
    ncm = models.CharField("NCM", max_length=8)
    cfop = models.CharField("CFOP", max_length=4)
    unidade = models.CharField("Unidade", max_length=6)
    valor_unitario = models.DecimalField("Valor Unitário", max_digits=12, decimal_places=2)

# Sim, você está corretíssimo novamente!

# Este bloco de código é a "planta" da sua tabela de Produtos. Embora você tenha mencionado "tabela cliente" no texto, o código que você postou define a tabela Produto.

def __str__(self):
    return f"{self.codigo} - {self.descricao}"

# Assim como no código anterior, lembre-se de adicionar o método __str__ para que, quando você olhar a lista de produtos no Django, apareça o nome do produto e não algo como <Produto: Produto object (1)>.

class NFe(models.Model):
    numero = models.PositiveIntegerField("Número da NF-e")
    serie = models.CharField("Série", max_length=3, default="")
    data_emissao = models.DateTimeField(auto_now_add=True)
    emitente = models.ForeignKey(Emitente, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

# numero = models.PositiveIntegerField(...): Armazena o número da nota. O tipo PositiveIntegerField é ideal porque garante que nunca teremos uma nota com número negativo.

# serie = models.CharField(...): Define a série da nota (ex: "001"). O default="" evita que o campo fique nulo caso não seja preenchido.

# data_emissao = models.DateTimeField(auto_now_add=True):
# O parâmetro auto_now_add=True é muito útil: ele salva automaticamente a data e a hora exata em que a nota foi criada no sistema, impedindo alterações retroativas manuais.

# models.ForeignKey(Emitente, ...): Liga esta nota a quem está vendendo/emitindo.

# models.ForeignKey(Cliente, ...): Liga esta nota a quem está comprando.1

# on_delete=models.PROTECT: Este é um recurso de segurança essencial. Ele impede que você apague um Cliente ou um Emitente do sistema se houver uma Nota Fiscal vinculada a eles. Isso protege a integridade dos seus dados fiscais.


    # Dados Gerais
    natureza_operacao = models.CharField("Natureza da Operação", max_length=100, default="VENDA")
    informacoes_complementares = models.TextField("Informações Complementares da NF", blank=True)
    informacoes_fisico = models.TextField("Informações Adicionais ao Fisico", blank=True)
    informacoes_nfe = models.TextField("Informações sobre a NF-e", blank=True)

# natureza_operacao (CharField): Representa o motivo da emissão da nota (ex: "VENDA", "DEVOLUÇÃO", "REMESSA").
# max_length=100: Limita o texto a 100 caracteres.
# default="VENDA": Caso você não preencha nada, o sistema automaticamente salvará como "VENDA", que é o uso mais comum.
# informacoes_complementares (TextField): É um campo de texto longo para observações que aparecem na DANFE para o cliente (ex: dados bancários para depósito, número do pedido de compra, etc.).

# blank=True: Permite que o campo fique vazio no formulário.

# informacoes_fisico (TextField): Campo destinado a notas específicas para o Fisco (autoridades fiscais). Também é um campo de texto longo e opcional (blank=True).

# informacoes_nfe (TextField): Parece ser um campo interno para anotações extras sobre o processamento da nota.


    # Totais
    valor_total = models.DecimalField("Valor Total", max_digits=12, decimal_places=2, default=0)
    valor_desconto = models.DecimalField("Desconto", max_digits=12, decimal_places=2, default=0)
    valor_liquido = models.DecimalField("Valor Líquido", max_digits=12, decimal_places=2, default=0)

   
   # ADICIONE ESTES CAMPOS:
    valor_frete = models.DecimalField("Valor do Frete", max_digits=12, decimal_places=2, default=0)
    valor_seguro = models.DecimalField("Valor do Seguro", max_digits=12, decimal_places=2, default=0)
    outras_despesas = models.DecimalField("Outras Despesas", max_digits=12, decimal_places=2, default=0)

#  Esses campos finalizam a parte financeira do seu modelo de Nota Fiscal. Eles utilizam o tipo DecimalField, que é o padrão ouro para lidar com dinheiro em programação, pois evita erros de arredondamento que ocorrem com números do tipo "float".

# valor_total: Representa o valor bruto da nota (a soma de todos os produtos antes dos descontos).

# valor_desconto: Armazena quanto foi subtraído do valor total.

# valor_liquido: É o resultado final que o cliente realmente deve pagar ($Total - Desconto$).


    def __str__(self):
        return f"NF-e {self.numero}/{self.serie}"

# 

class ItemNFe(models.Model):
    nfe = models.ForeignKey(NFe, on_delete=models.CASCADE, related_name="itens")
    item_pedido = models.PositiveIntegerField("N° do Item do Pedido de Compra")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField("Qtd.", max_digits=12, decimal_places=2)
    valor_unitario = models.DecimalField("Vr. Unitário", max_digits=12, decimal_places=2)
    valor_total_bruto = models.DecimalField("Vr. Total Bruto", max_digits=12, decimal_places=2)
    valor_tributo = models.DecimalField("Und. Tributo", max_digits=12, decimal_places=2, default=0)

# nfe = models.ForeignKey(...): Cria a conexão de "Muitos para Um". Muitos itens pertencem a uma única NFe.
# Ajuste Técnico: O termo correto é ForeignKey (com "K" maiúsculo).
# on_delete=models.CASCADE: Este é um comportamento de "cascata". Se você excluir a Nota Fiscal, o Django apagará automaticamente todos os itens vinculados a ela. Isso mantém o banco de dados limpo.
# related_name="itens": É um atalho poderoso. No seu código Python, se você tiver uma nota chamada nota1, você pode acessar todos os itens dela usando nota1.itens.all().

# produto = models.ForeignKey(Produto, ...): Liga este item ao cadastro geral de produtos que você criou anteriormente.
# on_delete=models.PROTECT: Diferente do anterior, aqui usamos o "Proteger". Ele impede que alguém apague um Produto do sistema se ele já estiver registrado em alguma nota fiscal. Isso é essencial para auditorias fiscais.

# item_pedido: Um campo de número inteiro positivo. Geralmente usado para numerar as linhas da nota (Item 1, Item 2...) ou para bater com o número do item em um pedido de compra externo.

# quantidade: O volume vendido. Note que é um DecimalField, permitindo vender quantidades fracionadas (ex: 1.500 kg ou 10.75 metros).

# valor_unitario: O preço de cada unidade. Importante: Você grava o preço aqui, no momento da venda, porque se o preço do produto mudar no cadastro principal amanhã, o valor histórico desta nota fiscal deve permanecer o mesmo.

# valor_total_bruto: É o resultado da conta: $Quantidade \times Valor Unitário$.

# valor_tributo: Espaço para armazenar o valor dos impostos (ICMS, IPI, etc.) aplicados especificamente a este item.

class Transportadora(models.Model):
    nfe = models.OneToOneField(NFe, on_delete=models.CASCADE, related_name="tranportadora")
    nome = models.CharField("Nome da Transportadora", max_length=200,blank=True)
    cnpj = models.CharField("CNPJ", max_length=14, blank=True)
    ie = models.CharField("IE", max_length=20, blank=True)
    logradouro = models.CharField(max_length=200, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    tipo_frete = models.CharField("Tipo de Frete", max_length=20, default="0 - Por conta do emitente")

# nfe = models.OneToOneField(NFe, ...) Esta é a linha mais importante. O OneToOneField cria uma relação de 1 para 1.
# on_delete=models.CASCADE: Se a Nota Fiscal for apagada, os dados da transportadora vinculados a ela também serão excluídos automaticamente.
# related_name="tranportadora": Permite que, dentro de um objeto da NFe, você acesse os dados de transporte facilmente (ex: nfe.tranportadora.nome). Nota: Há um erro de digitação aqui, o ideal seria "transportadora" com 's'.

# nome = models.CharField(..., max_length=200, balnk=True) Nome da empresa de transporte.

# cnpj = models.CharField(..., max_length=14, blank=True) Armazena os 14 dígitos do CNPJ da transportadora.

# ie = models.CharField(..., max_length=20, blank=True) Armazena a Inscrição Estadual da empresa.

# logradouro, municipio e uf Campos de texto para Rua/Avenida, Cidade e Estado (UF).
# max_length=2: No campo uf, limita o texto a apenas duas letras (ex: "SP", "MG", "RJ").


# tipo_frete = models.CharField(..., default="0 - Por conta do emitente") Define a modalidade do frete conforme os padrões da SEFAZ.

# default: Define que, se você não escolher nada, o sistema marcará automaticamente como frete por conta de quem vende (Emitente), que é o padrão mais comum em muitos negócios.


class Volume(models.Model):
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE, related_name="volumes")
    quantidade = models.PositiveIntegerField("Qtd. Volumes")
    especie = models.CharField("Espécie Volume", max_length=50)
    marca = models.CharField("Marca", max_length=50, blank=True)
    numeracao = models.CharField("N° Volumes", max_length=50, blank=True)
    peso_liquido = models.DecimalField("Peso Líquido", max_digits=10, decimal_places=3)
    peso_bruto = models.DecimalField("Peso Bruto", max_digits=10, decimal_places=3)

# class Volume(models.Model): Define a tabela no banco de dados que guardará as informações físicas da carga (peso, quantidade de caixas, etc.).
# transportadora = models.ForeignKey(Transprportadora, ...) Cria um relacionamento de Muitos para Um. Isso significa que uma transportadora pode ter vários volumes cadastrados para uma única entrega.
# on_delete=models.CASCADE: Se os dados da transportadora forem apagados, os volumes vinculados a ela também serão excluídos.
# related_name="volumes": Permite que você acesse todos os volumes de uma transportadora usando transportadora.volumes.all().

# quantidade = models.PositiveIntegerField("Qtd. Volumes") Um número inteiro positivo que indica quantas unidades daquele volume estão sendo enviadas (ex: 10).

# peso_bruto = models.DecimalField("Peso Bruto", max_digits=10, decimal_places=3)

# marca = models.CharField("Marca", max_length=50, blank=True) Campo opcional para identificar marcas impressas nas embalagens.

# numeracao = models.CharField("N° Volumes", max_length=50, blank=True) Campo opcional para identificar a numeração sequencial dos volumes (ex: "001 a 010").

# peso_liquido e peso_bruto (DecimalField) Campos numéricos precisos para o peso da mercadoria.
# max_digits=10: O número pode ter até 10 dígitos no total.
# decimal_places=3: Importante! Na nota fiscal brasileira, pesos geralmente usam 3 casas decimais (gramas), como em 15.550 kg.



class Duplicata(models.Model):
    nfe = models.ForeignKey(NFe, on_delete=models.CASCADE, related_name="duplicatas")
    numero = models.CharField("N° Duplicata", max_length=20)
    data_vencimento = models.DateField("Data Vencimento")
    valor = models.DecimalField("Valor", max_digits=12, decimal_places=2)

# class Duplicata(models.Model): Cria a tabela no banco de dados para armazenar as informações de cobrança (contas a receber) vinculadas à NF-e.

# nfe = models.ForeignKey(NFe, on_delete=models.CASCADE, related_name="duplicatas") Cria um relacionamento de Muitos para Um.
# on_delete=models.CASCADE: Se a Nota Fiscal for excluída, todas as suas parcelas (duplicatas) também serão apagadas do sistema automaticamente.
# related_name="duplicatas": Permite que você acesse as parcelas direto pela nota. Por exemplo, no seu código Python, você poderá usar minha_nfe.duplicatas.all() para ver todo o financeiro daquela nota.

# numero = models.CharField("N° Duplicata", max_length=20) Armazena a identificação da duplicata. Geralmente segue um padrão como "001/01", "001/02", etc., indicando o número da nota e o número da parcela

# data_vencimento = models.DateField("Data Vencimento") Diferente do DateTimeField (que guarda horas), o DateField armazena apenas a data (dia, mês e ano). É o campo ideal para prazos de pagamento.

# valor = models.DecimalField("Valor", max_digits=12, decimal_places=2) O valor financeiro daquela parcela específica.
# max_digits=12: Permite valores até 999.999.999,99.
#decimal_places=2: Garante a precisão de duas casas decimais para os centavos.
