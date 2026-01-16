from django.shortcuts import render, get_object_or_404, redirect
from .forms import *

def gerenciar_nfe(request, pk=None):
    if pk:
        nfe = get_object_or_404(NFe, pk=pk)
    else :
        nfe = None
    
    if request.method == 'POST':
        nfe_form = NFeForm(request.POST, instance=nfe)
        transporte_form = TransportadoraForm(request.POST, instance=getattr(nfe, 'transporte', None))
        cobranca_form = CobrancaForm(request.POST, instance=getattr(nfe, 'cobranca', None))
        info_form = InfoStatusForm(request.POST, instance=getattr(nfe, 'info_status', None))
        
        if nfe_form.is_valid() and transporte_form.is_valid() and cobranca_form.is_valid() and info_form.is_valid():
            nfe = nfe_form.save()
            transporte = transporte_form.save(commit=False)
            transporte.nfe = nfe
            transporte.save()
            cobranca = cobranca_form.save(commit=False)
            cobranca.nfe = nfe
            cobranca.save()
            info = info_form.save(commit=False)
            info.nfe = nfe
            info.save()
            return redirect('emitir_nfe')  # or appropriate URL
    else:
        nfe_form = NFeForm(instance=nfe)
        transporte_form = TransportadoraForm(instance=getattr(nfe, 'transporte', None))
        cobranca_form = CobrancaForm(instance=getattr(nfe, 'cobranca', None))
        info_form = InfoStatusForm(instance=getattr(nfe, 'info_status', None))
    
    context = {
        'nfe_form': nfe_form,
        'transporte_form': transporte_form,
        'cobranca_form': cobranca_form,
        'info_form': info_form,
    }
    return render(request, 'nfe/form_nfe.html', context)

def emitir_nfe(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        nfe_form = NFeForm(request.POST)
        item_formset = ProdutoFormSet(request.POST)

        if cliente_form.is_valid() and nfe_form.is_valid() and item_formset.is_valid():
            cliente = cliente_form.save()
            nfe = nfe_form.save(commit=False)
            nfe.cliente = cliente
            nfe.save()
            
            item_formset.instance = nfe
            item_formset.save() 
            return redirect('gerenciar_nfe', pk=nfe.pk) 
    else:
        cliente_form = ClienteForm()
        nfe_form = NFeForm()
        item_formset = ProdutoFormSet()

    return render(request, 'nfe/form_nfe.html', {
        'cliente_form': cliente_form,
        'nfe_form': nfe_form,
        'item_formset': item_formset,
    })
