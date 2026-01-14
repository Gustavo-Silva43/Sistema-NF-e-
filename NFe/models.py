from django.db import models
from decimal import Decimal
from django.core.validators import RegexValidator

class End_Entrega(models.Model):
    cliente = models.CharField("Cliente", max_length=200)
    cep = models.CharField("CEP",max_length=8)
    logradouro = models.CharField("Logradouro",max_length=200)
    numero = models.CharField("Nº ",max_length=20)
    complemento = models.CharField("Complemento", max_length=100)
    bairro = models.CharField("Bairro",max_length=100)
    IBGE = models.CharField("Cód.IBGE", max_length=100)
    municipio = models.CharField("Município",max_length=100)
    uf = models.CharField("UF",max_length=2)
    

    def __str__(self):
        return self.nome_razao


class Cliente(models.Model):
    TIPO_PESSOA_CHOICES = [
        ('f', 'Física'),
        ('J', 'Jurídica'),
    ]

    tipo_pessoa = models.CharField(
        'Tipo Pessoa', 
        max_length=1,
        choices=TIPO_PESSOA_CHOICES,
        default='J'
    )


    TIPO_CONTRIBUINTE_CHOICES = [
        ('1', 'Contribuinte ICMS'),
        ('2', 'Contribuinte Isento'),
        ('9', 'Não Contribuinte'),
    ]

    tipo_contribuinte = models.CharField(
        'Tipo de Contribuinte',
        max_length=1,
        choices=TIPO_CONTRIBUINTE_CHOICES,
        default='1'
    )

    cnpj = models.CharField(
        'CNPJ / CPF',
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                r'^\d{11}|\d{14}$',
                message='CPF deve ter 11 digitos ou CNPJ 14 digitos (sem pontos/máscara)'
            )
        ],
        help_text='Informe apenas números (com máscara: 00.000.000/0000-00 ou 000.000.000-00)'
    )

    inscricao_estadual = models.CharField(
        'Inscrição Estadual',
        max_length=20,
        blank=True,
        help_text='Preenchimento obrigatório se contribuinte ICMS',
        null=True
    )

    inscricao_municipal = models.CharField(
        'Inscrição Municipal',
        max_length=20,
        blank=True
    )

    nome = models.CharField(
        'Cliente',
        max_length=200  
    )
    
    informacao_estrangeira = models.CharField(
        'Informação Estrangeira',
        max_length=200,
        blank=True,
        help_text='Preenchimento quando destinatário for estrangeiro'
    )

    cep = models.CharField('CEP', max_length=9, help_text='Formato: 00000-000 (será limpo no save)')
    logradouro = models.CharField('Logradouro', max_length=200)
    numero = models.CharField('N°', max_length=20, blank=True)
    bairro = models.CharField('Bairro', max_length=100)

    cod_ibge = models.CharField(
        'Cód. IBGE',
        max_length=7,
        help_text='Código do município no IBGE (7 digitos)'
    )

    municipio = models.CharField('Município', max_length=100)
    uf = models.CharField('UF', max_length=2)

    cod_pais = models.CharField(
        'Cód. País',
        max_length=4,
        default='1058',
        help_text='Código do pais (1058 = Brasil)'
    )

    pais = models.CharField(
        'Pais',
        max_length=60,
        default='Brasil'
    )
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    inscri_suframa = models.CharField(
        'Inscr. SUFRAMA',
        max_length=20,
        blank=True
    )
    lote_suframa = models.CharField("Lote SUFRAMA", max_length=50, blank=True, default='0')

    email = models.EmailField('E-mail', blank=True)
    email_contador = models.EmailField('E-mail Contador', blank=True, null=True)


    # criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    # atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cnpj}"
    
    def save(self, *args, **kwargs):
        self.cnpj = ''.join(filter(str.isdigit, self.cnpj)) if self.cnpj else ''
        self.cep = ''.join(filter(str.isdigit, self.cep)) if self.cep else ''
        super().save(*args, **kwargs)


class Produto(models.Model):
    
    item_pedido = models.IntegerField(" Nº do Item ")
    codigo_produto = models.CharField("Cd. Produto", max_length=60)
    ean = models.CharField("EAN", max_length=14, blank=True, null=True)
    descricao = models.CharField(" Descrição do Produto", max_length=120)
    ncm = models.CharField("NCM", max_length=8)
    nve = models.CharField("NVE", max_length=6, blank=True, null=True)
    tipi = models.CharField("TIPI", max_length=3, blank=True, null=True)
    cfop = models.CharField("CFOP", max_length=4)
    unidade = models.CharField("Unidade", max_length=6)
    quantidade = models.DecimalField("Qtd", mmax_digits=15, decimal_places=4)
    valor_unitario = models.DecimalField("Vr. Untário", max_digits=15)
    valor_total_bruto = models.DecimalField("Vr. Total Bruto", max_digits=15, decimal_places=2)

    unidade_tributo = models.CharField("Und.Tributo", max_length=6)
    quantidade_tributo = models.DecimalField("Qtd. Tributo", max_digits=15, decimal_places=4)
    valor_unitario_tributo = models.DecimalField("Vr. Unt Trib", max_length=15, decimal_places=10)

    valor_frete = models.DecimalField("Vr Frete", max_digits=15, decimal_places=2, default=0)
    valor_seguro = models.DecimalField("Vr Seguro", max_digits=15, decimal_places=2, default=0)
    valor_desconto = models.DecimalField("Vr.Desconto", max_digits=15, decimal_places=2, default=0)
    valor_outros = models.DecimalField("Vr. Outros", max_digits=15, decimal_places=2, default=0)

    numero_pedido_compra = models.CharField("Nº do Pedido de Compra", max_length=15, blank=True, null=True)
    item_pedido_compra = models.CharField("Nº do Item do Pedido de Compra", blank=True, null=True)
    fci = models.CharField("FCI", max_length=36, blank=True, null=True)
    valor_tributos_estimado = models.DecimalField("Vr.Tributos", max_digits=15, decimal_places=2, default=0)

    origem_mercadoria = models.CharField("Origem da Mercadoria", max_length=1)
    cst_operacao = models.CharField("CST Operação", max_length=3)
    icms_bc = models.DecimalField("ICMS BC", max_digits=15, decimal_places=2, default=0)
    icms_percentual = models.CharField("% ICMS", max_digits=5, decimal_places=2, default=0)
    icms_valor = models.DecimalField("Vr. ICMS", max_digits=15, decimal_places=2, default=0)

    icms_st_bc = models.DecimalField("BC CST (ST)", max_digits=15, decimal_places=2, default=0)
    icms_st = models.DecimalField("ICMS ST", max_length=15, decimal_places=2, default=0)
    icms_st_red_bc = models.DecimalField("Red.BC ICMS ST", max_digits=5, decimal_places=2, default=0)
    icms_st_valor = models.DecimalField("Vr. ICMS ST", max_digits=15, decimal_places=2, default=0)

    icms_st_percentual = models.DecimalField("% ICMS ST", max_digits=5, decimal_places=2, default=0)
    icms_st_valor = models.DecimalField("Vr. ICMS ST", max_digits=15, decimal_places=2, default=0)
    pis_cst = models.CharField("PIS CST", max_length=2)
    pis_bc = models.CharField("BC PIS", max_digits=15, decimal_places=2, default=0)
    
    pis_percentual = models.CharField("%PIS", max_digits=5, decimal_places=2, default=0)
    pis_valor = models.DecimalField("Vr. PIS", max_digits=15, decimal_places=2, default=0)
    cofins_cst = models.DecimalField("CONFINS CST", max_length=2)
    cofins_bc = models.DecimalField("CONFINS BC", max_digits=15, decimal_places=2, default=0)

    cofins_percentual = models.DecimalField("%CONFINS", max_digits=5, decimal_places=2, default=0)
    icms_uf_dest_bc = models.DecimalField("ICMSUFDest_vBCUFDest",max_digits=15, decimal_places=2, default=0)
    icms_uf_dest_p_fcp = models.DecimalField("ICMSUFDest_pFCPUFDest", max_digits=5, decimal_places=2, default=0)
    icms_uf_dest_p_inter = models.DecimalField("ICMSUFDest_pICMSInter", max_length=5, decimal_places=2, default=0)
    icms_uf_dest_p_inter_part = models.DecimalField("ICMSUFDest_pICMSInterPart", max_length=5, decimal_places=2, default=0)
    icms_uf_dest_v_fcp = models.DecimalField("ICMSUFDest_vFCPUFDest", max_digits=15, decimal_places=2, default=0)

    icms_uf_dest_v_icms = models.DecimalField("ICMSUFDest_vICMSUFDest", max_digits=15, decimal_places=2, default=0)
    icms_uf_remet_v_icms = models.DecimalField("ICMSUFDest_vICMSUFRemet", max_digits=15, decimal_places=2, default=0)

    di_numero = models.CharField("Nº DI", max_length=12, blank=True, null=True)
    di_data = models.DateField("Data DI", blank=True, null=True)
    di_local_desemb = models.CharField("Local Desemb.", max_length=60, blank=True)
    di_uf_desemb = models.CharField("UF Desemb.", max_length=2, blank=True)
    di_data_desemb = models.CharField("Data Desemb.", blank=True, null=True)
    di_via_transporte = models.CharField("Via Transporte", max_length=2, blank=True, null=True)
    afrmm = models.DecimalField("AFRMM", max_digits=15, decimal_places=2, default=0)
    forma_importacao = models.CharField("Forma Importação", max_length=1, blank=True, null=True)
    importa_cnpj = models.CharField("CNPJ", max_length=14, blank=True)
    importa_uf_terceiro = models.CharField("UF TErceiro", max_length=14, blank=True, null=True)
    cod_exportador = models.CharField("Cód. Exportador", max_length=60, blank=True, null=True)
    n_adicao = models.CharField("nAdicao", blank=True, null=True)
    n_seq_adic = models.IntegerField("nSeqAdic", blank=True, null=True)
    c_fabricante = models.CharField("cFabricante", max_length=60, blank=True)
    v_desc_di = models.DecimalField("vDescDI", max_digits=15, decimal_places=2, default=0)

    ipi_cst = models.CharField("IPI_CST", max_length=2, blank=True, null=True)
    ipi_bc = models.DecimalField("IPI_vBC", max_digits=15, decimal_places=2, default=0)
    ipi_percentual = models.DecimalField("IPI_pIPI", max_digits=5, decimal_places=2, default=0)
    ipi_valor = models.DecimalField("IPI_vIPI", max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.codigo_produto} - {self.descricao}"

class NFe(models.Model):
    MODELO_CHOICES = [('55', '55 - NF-e'), ('65', '65 - NFC-e')]
    TP_EMIS_CHOICES = [('1', 'Normal'), ('9', 'Contingência')]
    TP_NF_CHOICES = [('0', 'Entrada'), ('1', 'Saída')]
    FIN_NF_CHOICES = [('1', 'Normal'), ('2', 'Complementar'), ('3', 'Ajuste'), ('4', 'Devolução')]
    DESTINO_CHOICES = [('1', 'Interna'), ('2', 'Interestadual'), ('3', 'Exterior')]
    PRESENCA_CHOICES = [('0', 'Não se aplica'), ('1', 'Presencial'),('2', 'Internet')]
    OP_CONSUMIDOR_CHOICES = [('S', 'Sim'), ('N', 'Não')]
    STATUS_CHOICES = [
        ('100', '100 - Autorizado o uso da NF-e'),
        ('101', '101 - Cancelamento de NF-e homologado'),
        ('102', '102 - Inutilização de número homologado'),
        ('135', '135 - Evento averbado'),
    ]

    pedido = models.CharField("Pedido", max_length=20, blank=True, null=True)
    numero = models.IntegerField("NF-e", max_length=20, blank=True, null=True)
    serie = models.IntegerField("Sèrie", max_length=20, blank=True, null=True)
    modelo = models.CharField("Modelo NF-e", max_length=2, choices=MODELO_CHOICES, default='55')
    tipo_emissão = models.CharField("Tipo Emissão", max_length=1, choices=TP_EMIS_CHOICES, default='1')
    tipo_nfe = models.CharField("Tipo NF-e", max_length=1, choices=TP_NF_CHOICES, default='1')
    finalidade = models.CharField("Finalidade NF-e", max_length=1, choices=FIN_NF_CHOICES, default='1')
    natureza_operacao = models.CharField("Natureza Operação", max_length=60)

    presenca_comprador = models.CharField("Presença Comprador?", max_length=1, choices=PRESENCA_CHOICES, default='1')
    operacao_consumidor = models.BooleanField("Operação com Consumidor?", max_length=1, choices=OP_CONSUMIDOR_CHOICES, default='N')
    local_destino = models.CharField("Local Destino da Operação", max_length=1, choices=DESTINO_CHOICES, default='1')
    referenciar_nfe = models.CharField("Referenciar NF-e?", max_length=1, choices=OP_CONSUMIDOR_CHOICES, default='N')

    chave_acesso = models.CharField("Chave de Acesso", max_length=44, blank=True, null=True)
    cdv = models.CharField("cDV", max_length=1, blank=True, null=True)
    recibo = models.CharField("Recibo", max_length=20, blank=True, null=True)
    protocolo = models.CharField("Protocolo", max_length=10, blank=True, null=True)
    digito_validador = models.CharField("Digito Validador", max_length=10, blank=True, null=True)

    data_emissão = models.DateTimeField("Data/Hora Emissão")
    data_receebimento = models.DataTimeField("Data/Hora Recebimento", blank=True, null=True)
    status_sefaz = models.CharField("Status SEFAZ", max_length=3, choices=STATUS_CHOICES, blank=True, null=True)
    codigo_retorno = models.IntegerField("Código Retorno", blank=True, null=True)

    transmitir = models.BooleanField("Transmitir", default=False)
    cce = models.BooleanField("CCe", default=False)
    cancelar = models.BooleanField("Cancelar", default=False)

    tipo_evento = models.CharField("Tipo Evento", max_length=20, blank=True, null=True)
    protocolo_evento = models.CharField("Protocolo Evento", max_length=20, blank=True, null=True)
    sequencia_evento = models.IntegerField("Seq. Evento", default=1)

    emitente = models.ForeignKey('Emitente', on_delete=models.PROTECT)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)

    justificativa = models.TextField("Justificativa", blank=True, null=True)

    valor_total = models.DecimalField(max_digits=15, decimal_places=2,default=0.00)

    class Meta:
        verbose_name = "NF-e"
        verbose_name_plural = "NF-e"
    
    def __str__(self):
        return f"{self.numero} - {self.natureza_operacao}"



# class ItemNFe(models.Model):
#     nfe = models.ForeignKey(NFe, on_delete=models.CASCADE, related_name="itens")
#     item_pedido = models.PositiveIntegerField("N° do Item do Pedido de Compra")
#     produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
#     quantidade = models.DecimalField("Qtd.", max_digits=12, decimal_places=2)
#     valor_unitario = models.DecimalField("Vr. Unitário", max_digits=12, decimal_places=2)
#     valor_total_bruto = models.DecimalField("Vr. Total Bruto", max_digits=12, decimal_places=2)
#     valor_tributo = models.DecimalField("Und. Tributo", max_digits=12, decimal_places=2, default=0)



class Transportadora(models.Model):
    nfe = models.OneToOneField(NFe, on_delete=models.CASCADE, related_name="tranportadora")
    nome = models.CharField("Nome da Transportadora", max_length=200,blank=True)
    cnpj = models.CharField("CNPJ", max_length=14, blank=True)
    ie = models.CharField("IE", max_length=20, blank=True)
    logradouro = models.CharField(max_length=200, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    tipo_frete = models.CharField("Tipo de Frete", max_length=20, default="0 - Por conta do emitente")



class Volume(models.Model):
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE, related_name="volumes")
    quantidade = models.PositiveIntegerField("Qtd. Volumes")
    especie = models.CharField("Espécie Volume", max_length=50)
    marca = models.CharField("Marca", max_length=50, blank=True)
    numeracao = models.CharField("N° Volumes", max_length=50, blank=True)
    peso_liquido = models.DecimalField("Peso Líquido", max_digits=10, decimal_places=3)
    peso_bruto = models.DecimalField("Peso Bruto", max_digits=10, decimal_places=3)


class Pagamento(models.Model):
    IND_PAGTO_CHOICES = [
        ('0', '0 - Pagamento á Vista'),
        ('1', '1 - Pagamento á Prazo'),
    ]

    FORMA_PAGTO_CHOICES = [
        ('01', '01 - Dinheiro')
        ('02', '02 - Cheque'),
        ('03', '03 - Cartão de Credito'),
        ('04', '04 - Cartão de Débito'),
        ('15', '15 - Boleto Bancário'),
        ('90', '90 - Sem pagamento'),
        ('99', '99 - Outros'),
    ]

    nfe = models.ForeignKey('NFe', related_name='pagamentos', on_delete=models.CASCADE)

    numero_forma = models.IntegerField("Nº Forma")
    indicador_pagamento = models.CharField("Ind. Forma Pagto.", max_length=1, choices=IND_PAGTO_CHOICES)
    forma_pagamento = models.CharField("Forma Pagto",max_length=2, choices=FORMA_PAGTO_CHOICES)
    valor_pagamento = models.DecimalField("Valor Pagto", max_digits=15, decimal_places=2)

    tipo_integracao = models.CharField("Tipo Integração CC", max_length=1, blank=True, null=True)
    cnpj_credenciadora = models.CharField("CNPJ Credenciadora CC",max_length=14, blank=True, null=True)
    bandeira_cc = models.CHarField("Bandeira CC", max_length=2, blank=True, null=True)
    autorizacao_transacao = models.CharField("Nº Autorização Transação",max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Pagamento da NF-e"
        verbose_name_plural = "Pagamento da NF-e"

        def __str__(self):
            return f"{self.numero_forma} - {self.get_forma_pagamento_display()} - R$ {self.valor_pagamento}"



