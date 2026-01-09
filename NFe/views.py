from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import NFe, Emitente
from .forms import(
    NFeForm, ClienteForm, ItemNFeFormSet,
    TransportadoraForm, VolumeFormSet, DuplicataFormSet
)

def emitir_nfe(request, pk=None):
    nfe = None
    if pk:
        nfe = get_object_or_404(NFe, pk=pk)
    
    emitente = Emitente.objects.first()
    # if not emitente and not pk:
    #     messages.error(request, "Cadastre o emitente da empresa primeiro!")
    #     return redirect('admin:nfe_emitente_add')

    if request.method == 'POST':
        nfe_form = NFeForm(request.POST, instance=nfe)
        cliente_form = ClienteForm(request.POST, instance=nfe.cliente if nfe else None)
        item_formset = ItemNFeFormSet(request.POST, instance=nfe)
        transportadora_form = TransportadoraForm(request.POST, instance=nfe.transportadora if nfe else None)
        volume_formset = VolumeFormSet(request.POST, instance=nfe.transportadora if nfe else None)
        duplicata_formset = DuplicataFormSet(request.POST, instance=nfe)

        if (nfe_form.is_valid() and cliente_form.is_valid() and
            item_formset.is_valid() and transportadora_form.is_valid() and
            volume_formset.is_valid() and duplicata_formset.is_valid()):

            try:
                with transaction.atomic(): 
                    cliente = cliente_form.save()
                    nfe = nfe_form.save(commit=False)
                    nfe.emitente = emitente
                    nfe.cliente = cliente
                    nfe.save()
                    itens = item_formset.save(commit=False)
                    total_itens = 0
                    for item in itens:
                        item.nfe = nfe
                        item.save()
                        total_itens += item.valor_total
                    item_formset.save_m2m() if hasattr(item_formset, 'save_m2m') else None

                    if any(transportadora_form.cleaned_data.values()):
                        transportadora = transportadora_form.save(commit=False)
                        transportadora.nfe = nfe
                        transportadora.save()
                        volumes = volume_formset.save(commit=False)
                        for v in volumes:
                            v.transportadora = transportadora
                            v.save()

                    duplicatas = duplicata_formset.save(commit=False)
                    for d in duplicatas:
                        d.nfe = nfe
                        d.save()

                    nfe.valor_total = (total_itens - 
                                       nfe.valor_desconto +
                                       nfe.valor_frete +
                                       nfe.valor_seguro +
                                       nfe.outros_despesas)
                    nfe.save()

                    messages.success(request, f"NF-e {nfe.numero}/{nfe.serie} Salva com sucesso!")
                    return redirect('emitir_nfe', pk=nfe.pk)
            except Exception as e:
                messages.error(request,f"Erro ao salvar: {e}")
    else:
        nfe_form = NFeForm(instance=nfe)
        cliente_form = ClienteForm(instance=nfe)
        item_formset = ItemNFeFormSet(instance=nfe)
        transportadora_form = TransportadoraForm(instance=nfe.transportadora if nfe else None)      
        volume_formset = VolumeFormSet(instance=nfe.transportadora if nfe else None)
        duplicata_formset = DuplicataFormSet(instance=nfe)

    context = {
        'nfe_form':nfe_form,
        'cliente_form': cliente_form,
        'item_formset':item_formset,
        'transportadora_form':transportadora_form,
        'volume_formset':volume_formset,
        'duplicata_formset': duplicata_formset,
        'nfe': nfe,
        'emitente':emitente,
    }      

    return render(request,'form_nfe.html', context)
    
# 1. Preparação e Verificação do Emitente
# def emitir_nfe(request, pk=None):: Define a função. Se receber um pk (Primary Key), ela edita uma nota; se for None, cria uma nova.

# nfe = get_object_or_404(NFe, pk=pk): Tenta buscar a nota no banco. Se não achar, mostra erro 404.

# emitente = Emitente.objects.first(): Busca a sua empresa no banco. Como uma empresa geralmente emite suas próprias notas, assume-se que só existe um emitente cadastrado.

# if not emitente...: Se você esqueceu de cadastrar sua própria empresa, o sistema te impede de continuar e te manda para a tela de cadastro.


# 2. Recebendo os Dados (O bloco if request.method == 'POST')
# Quando você clica em "Salvar", o Django entra aqui para processar o que foi digitado:

# nfe_form = NFeForm(request.POST, instance=nfe): Carrega os dados gerais da nota vindos do navegador.

# cliente_form, item_formset, etc.: Carregam os dados do cliente, os produtos, a transportadora e as duplicatas. O request.POST contém os valores digitados e o instance garante que estamos editando o objeto certo.


# 3. Validação e Segurança (transaction.atomic)
# if (nfe_form.is_valid() and ...): Verifica se todos os campos obrigatórios foram preenchidos corretamente e se não há erros (como CPF inválido).

# with transaction.atomic():: Isso é crucial. Significa "Tudo ou Nada". Se houver um erro ao salvar o último item, o Django desfaz tudo o que salvou antes para não deixar "lixo" no banco de dados.


# 4. O Processo de Salvamento
# O código segue uma ordem lógica de dependência:

# Salva o Cliente: Primeiro salva quem está comprando.

# Salva a NF-e: Salva a nota, vinculando ela ao emitente (você) e ao cliente salvo no passo anterior.

# Salva Itens: Percorre a lista de produtos, calcula o total_itens e vincula cada um à nota.

# Transporte: Verifica se os dados da transportadora foram preenchidos (any(...)). Se sim, salva a transportadora e seus respectivos volumes (caixas).

# Duplicatas: Salva as parcelas de pagamento vinculadas à nota.


# 5. Cálculo Final e Resposta
# nfe.valor_total = (...): Faz a conta matemática final (Produtos - Desconto + Frete + Seguro + Outros) para garantir que o total da nota esteja correto antes de salvar definitivamente.

# messages.success(...): Mostra uma barrinha verde de sucesso no topo do site.

# return redirect(...): Recarrega a página com os dados salvos.


# 6. O bloco else e o render
# O else: Se você estiver apenas entrando na página (sem clicar em salvar), ele cria os formulários limpos (ou preenchidos para edição) para serem exibidos.

# context = { ... }: Organiza todos os formulários e dados para que o arquivo HTML consiga "enxergá-los".

# return render(...): Pega o arquivo form_nfe.html, coloca os formulários dentro dele e entrega a página pronta no seu navegador.
