from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import NFe, Emitente
from .forms import(
    NFeForm, ClienteForm, ItemNFeFormSet,
    TransportadoraForm, VolumeFormSet, DuplicataFormSet
)

def emitir_nfe(request, pk=None):
    # pk = None -> nova NF-e | pk = id -> editar existente
    nfe = None
    if pk:
        nfe = get_object_or_404(NFe, pk=pk)
    
    # Pega o emitente (assume que tem só um cadastrado)
    emitente = Emitente.objects.first()
    if not emitente and not pk:
        messages.error(request, "Cadastre o emitente da empresa primeiro!")
        return redirect('admin:nfe_emitente_add')

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
                with transaction.atomic(): # Tudo ou nada
                    # 1. Salva o cliente
                    cliente = cliente_form.save()

                    # 2.Salva a NF-e
                    nfe = nfe_form.save(commit=False)
                    nfe.emitente = emitente
                    nfe.cliente = cliente
                    nfe.save()

                    # 3. Salva itens
                    itens = item_formset.save(commit=False)
                    total_itens = 0
                    for item in itens:
                        item.nfe = nfe
                        item.save()
                        total_itens += item.valor_total
                    item_formset.save_m2m() if hasattr(item_formset, 'save_m2m') else None

                    # 4.Salva transporte e volumes
                    if any(transportadora_form.cleaned_data.values()):
                        transportadora = transportadora_form.save(commit=False)
                        transportadora.nfe = nfe
                        transportadora.save()
                        volumes = volume_formset.save(commit=False)
                        for v in volumes:
                            v.transportadora = transportadora
                            v.save()
                    
                    # 5. Salva duplicatas
                    duplicatas = duplicata_formset.save(commit=False)
                    for d in duplicatas:
                        d.nfe = nfe
                        d.save()
                    
                    # 6. Calcula o valor total da nota
                    nfe.valor_total = (total_itens - 
                                       nfe.valor_desconto +
                                       nfe.valor_frete +
                                       nfe;.valor_seguro +
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
            volume_formset = VolumeFormSet(instance=nfe.transportadora is nfe else None)
            duplicata_formset = DuplicataFormSet(instance=nfe)

        context = {
            'nfe_form':nfe_form,
            'cliente_form': cliente_form,
            'item_formset':item_formset,
            'transportadora_form':transportadora_form,
            'volume_formset':volume_formset,
            duplicata_formset
        }      
