from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import ArquivosNFe


def _parse_arquivos_text(arquivos_text: str | None) -> list[str]:
    if not arquivos_text:
        return []
    return [line.strip() for line in arquivos_text.splitlines() if line.strip()]

def gerenciar_nfe(request, pk=None):
    if pk:
        nfe = get_object_or_404(NFe, pk=pk)
    else :
        nfe = None
    
    if request.method == 'POST':
        acao = request.POST.get('action')
        # Salvar arquivos enviados na aba "Arquivos da NFe"
        if acao == 'salvar_arquivos' and nfe is not None:
            uploaded_files = request.FILES.getlist('arquivos_nfe_files')
            if uploaded_files:
                dir_name = f"nfe_{nfe.id}"
                storage_location = Path(settings.MEDIA_ROOT) / dir_name
                storage_location.mkdir(parents=True, exist_ok=True)

                storage = FileSystemStorage(location=str(storage_location))

                arquivos_obj = ArquivosNFe.objects.filter(nfe=nfe).first()
                if arquivos_obj is None:
                    arquivos_obj = ArquivosNFe(nfe=nfe)

                existing = set(_parse_arquivos_text(arquivos_obj.arquivos))
                saved_names: list[str] = []

                for f in uploaded_files:
                    saved_name = storage.save(f.name, f)  # retorna o nome salvo (pode incluir sufixo)
                    saved_names.append(saved_name)

                # Unifica nomes (sem duplicar)
                for name in saved_names:
                    existing.add(name)

                arquivos_obj.arquivos = "\n".join(sorted(existing))
                arquivos_obj.save()

        nfe_form = NFeForm(request.POST, instance=nfe)
        transporte_form = TransportadoraForm(request.POST, instance=getattr(nfe, 'transporte', None))
        cobranca_form = CobrancaForm(request.POST, instance=getattr(nfe, 'cobranca', None))
        base_calculo_form = BaseCalculoForm(request.POST, instance=getattr(nfe, 'base_calculo_totais', None))
        info_form = InfoStatusForm(request.POST, instance=getattr(nfe, 'info_status', None))
        item_formset = ProdutoFormSet(request.POST, instance=nfe)
        pagamento_formset = PagamentoFormSet(request.POST, instance=nfe)
        
        if nfe_form.is_valid() and transporte_form.is_valid() and cobranca_form.is_valid() and base_calculo_form.is_valid() and info_form.is_valid() and item_formset.is_valid() and pagamento_formset.is_valid():
            nfe = nfe_form.save()
            transporte = transporte_form.save(commit=False)
            transporte.nfe = nfe
            transporte.save()
            cobranca = cobranca_form.save(commit=False)
            cobranca.save()
            base_calc = base_calculo_form.save(commit=False)
            base_calc.nfe = nfe
            base_calc.save()
            info = info_form.save(commit=False)
            info.nfe = nfe
            info.save()
            item_formset.save()
            pagamento_formset.save()
            if acao == 'salvar_arquivos' and nfe is not None:
                return redirect('gerenciar_nfe', pk=nfe.pk)
            if acao == 'carta_correcao' and nfe is not None:
                # Carta de Correção (evento 135): mantém o mesmo número e registra o evento no cadastro
                nfe.status_sefaz = '135'
                nfe.cce = True
                nfe.save()
                return redirect('gerenciar_nfe', pk=nfe.pk)

            return redirect('emitir_nfe')  # or appropriate URL
    else:
        nfe_form = NFeForm(instance=nfe)
        transporte_form = TransportadoraForm(instance=getattr(nfe, 'transporte', None))
        cobranca_form = CobrancaForm(instance=getattr(nfe, 'cobranca', None))
        base_calculo_form = BaseCalculoForm(instance=getattr(nfe, 'base_calculo_totais', None))
        info_form = InfoStatusForm(instance=getattr(nfe, 'info_status', None))
        item_formset = ProdutoFormSet(instance=nfe)
        pagamento_formset = PagamentoFormSet(instance=nfe)

    arquivos_obj = ArquivosNFe.objects.filter(nfe=nfe).first() if nfe is not None else None
    arquivos_list = _parse_arquivos_text(arquivos_obj.arquivos if arquivos_obj else None)
    media_url_nfe = f"{settings.MEDIA_URL}nfe_{nfe.id}/" if nfe is not None else ""
    
    context = {
        'nfe': nfe,
        'nfe_form': nfe_form,
        'transporte_form': transporte_form,
        'cobranca_form': cobranca_form,
        'base_calculo_form': base_calculo_form,
        'info_form': info_form,
        'item_formset': item_formset,
        'pagamento_formset': pagamento_formset,
        'arquivos_list': arquivos_list,
        'media_url_nfe': media_url_nfe,
    }
    return render(request, 'form_nfe.html', context)

def emitir_nfe(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        nfe_form = NFeForm(request.POST)
        cobranca_form = CobrancaForm(request.POST)
        base_calculo_form = BaseCalculoForm(request.POST)
        item_formset = ProdutoFormSet(request.POST)
        pagamento_formset = PagamentoFormSet(request.POST)

        if cliente_form.is_valid() and nfe_form.is_valid() and cobranca_form.is_valid() and base_calculo_form.is_valid() and item_formset.is_valid() and pagamento_formset.is_valid():
            cliente = cliente_form.save()
            nfe = nfe_form.save(commit=False)
            nfe.cliente = cliente
            nfe.save()

            cobranca = cobranca_form.save(commit=False)
            cobranca.save()

            base_calc = base_calculo_form.save(commit=False)
            base_calc.nfe = nfe
            base_calc.save()
            
            item_formset.instance = nfe
            item_formset.save()

            pagamento_formset.instance = nfe
            pagamento_formset.save()
            
            return redirect('gerenciar_nfe', pk=nfe.pk) 
    else:
        cliente_form = ClienteForm()
        nfe_form = NFeForm()
        cobranca_form = CobrancaForm()
        base_calculo_form = BaseCalculoForm()
        item_formset = ProdutoFormSet()
        pagamento_formset = PagamentoFormSet()

    return render(request, 'form_nfe.html', {
        'cliente_form': cliente_form,
        'nfe_form': nfe_form,
        'cobranca_form': cobranca_form,
        'base_calculo_form': base_calculo_form,
        'item_formset': item_formset,
        'pagamento_formset': pagamento_formset,
        'info_form': InfoStatusForm(),
    })

def iniciar(request):
    nfes = NFe.objects.all()
    nfe_selecionada = None

    nfe_id = request.GET.get('nfe_id') or request.POST.get('nfe_id')
    if nfe_id:
        nfe_selecionada = NFe.objects.filter(id=nfe_id).first()

    context = { 
        'nfes': nfes,
        'nfe_selecionada': nfe_selecionada,
        'nfe_form': NFeForm(instance=nfe_selecionada) if nfe_selecionada else None,
        'cobranca_form': CobrancaForm(instance=getattr(nfe_selecionada, 'cobranca', None)) if nfe_selecionada else CobrancaForm(),
        'base_calculo_form': BaseCalculoForm(instance=getattr(nfe_selecionada, 'base_calculo_totais', None)) if nfe_selecionada else BaseCalculoForm(),
        'info_form': InfoStatusForm(instance=getattr(nfe_selecionada, 'info_status', None)) if nfe_selecionada else InfoStatusForm(),
    }
    return render(request, 'form_nfe.html', context)


def abrir_pasta_arquivos(request, nfe_id: int):
    nfe = get_object_or_404(NFe, pk=nfe_id)
    arquivos_obj = ArquivosNFe.objects.filter(nfe=nfe).first()
    arquivos_list = _parse_arquivos_text(arquivos_obj.arquivos if arquivos_obj else None)
    media_url_nfe = f"{settings.MEDIA_URL}nfe_{nfe.id}/"

    return render(
        request,
        'arquivos_pasta.html',
        {
            'nfe': nfe,
            'arquivos_list': arquivos_list,
            'media_url_nfe': media_url_nfe,
        },
    )
