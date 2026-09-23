from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from .models import Prato, Combo, Mesa, Comanda, Item
from .forms import PratoForm


def inicio(request):
    return render(request, 'restaurante/inicio.html')


def lista_pratos(request):
    pratos = Prato.objects.all()

    q = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')

    if q:
        pratos = pratos.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))

    if categoria:
        pratos = pratos.filter(categoria=categoria)

    return render(
        request,
        'restaurante/lista_pratos.html',
        {
            'pratos': pratos,
            'categorias': Prato.CATEGORIA_CHOICES, 
        }
    )


def criar_prato(request):
    if request.method == 'POST':
        form = PratoForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('lista_pratos')
    else:
        form = PratoForm()

    return render(request, 'restaurante/form_prato.html', {'form': form, 'titulo': 'Cadastrar Prato'})


def editar_prato(request, prato_id):
    prato = get_object_or_404(Prato, id=prato_id)

    if request.method == 'POST':
        form = PratoForm(request.POST, instance=prato)
        if form.is_valid():
            form.save()
            return redirect('lista_pratos')
    else:
        form = PratoForm(instance=prato)

    return render(request, 'restaurante/form_prato.html', {'form': form, 'titulo': 'Editar Prato'})


def excluir_prato(request, prato_id):
    prato = get_object_or_404(Prato, id=prato_id)
    prato.delete()
    return redirect('lista_pratos')


def lista_combos(request):
    combos = Combo.objects.all()

    return render(
        request,
        'restaurante/lista_combos.html',
        {'combos': combos}
    )


def lista_mesas(request):
    mesas = Mesa.objects.all().order_by('numero')

    return render(
        request,
        'restaurante/lista_mesas.html',
        {'mesas': mesas}
    )


def abrir_comanda(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    comanda = Comanda.objects.filter(
        mesa=mesa,
        status='ABERTA'
    ).first()

    if not comanda:
        comanda = Comanda.objects.create(mesa=mesa)

        mesa.status = 'OCUPADA'
        mesa.save()

    pratos = Prato.objects.filter(disponivel=True)
    combos = Combo.objects.filter(disponivel=True)

    itens = comanda.itens.all()

    total = 0

    for item in itens:
        if item.prato:
            total += item.prato.preco * item.quantidade

        elif item.combo:
            total += item.combo.preco * item.quantidade

    return render(
        request,
        'restaurante/comanda.html',
        {
            'mesa': mesa,
            'comanda': comanda,
            'pratos': pratos,
            'combos': combos,
            'itens': itens,
            'total': total,
        }
    )


def adicionar_prato(request, comanda_id, prato_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    prato = get_object_or_404(Prato, id=prato_id)

    item = Item.objects.filter(
        comanda=comanda,
        prato=prato
    ).first()

    if item:
        item.quantidade += 1
        item.save()
    else:
        Item.objects.create(
            comanda=comanda,
            prato=prato,
            quantidade=1
        )

    return redirect('abrir_comanda', mesa_id=comanda.mesa.id)


def adicionar_combo(request, comanda_id, combo_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    combo = get_object_or_404(Combo, id=combo_id)

    item = Item.objects.filter(
        comanda=comanda,
        combo=combo
    ).first()

    if item:
        item.quantidade += 1
        item.save()
    else:
        Item.objects.create(
            comanda=comanda,
            combo=combo,
            quantidade=1
        )

    return redirect('abrir_comanda', mesa_id=comanda.mesa.id)


def fechar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)

    comanda.status = 'FECHADA'
    comanda.save()

    mesa = comanda.mesa
    mesa.status = 'LIVRE'
    mesa.save()

    return redirect('lista_mesas')


def remover_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    mesa_id = item.comanda.mesa.id

    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()

    return redirect('abrir_comanda', mesa_id=mesa_id)
