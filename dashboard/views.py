from django.shortcuts import render

from gadgets.models import *

def index_dash(request):
    gadgets_all = Gadget.objects.all()
    qnt_gadgetsq = gadgets_all.__len__()
    gadgets_ok = gadgets_all.filter(status__icontains='GOTOWY').__len__()
    gadgets_serwis = gadgets_all.filter(status__icontains='NAPRAWIENIE').__len__()
    gadgets_czeka = gadgets_all.filter(status__icontains='CZEKA NA CZĘŚCI').__len__()

    context = {
        'gadgets_serwis': gadgets_serwis,
        'gadgets_ok': gadgets_ok,
        'qnt_gadgets': qnt_gadgetsq,
        'gadgets_czeka': gadgets_czeka
    }

    return render(request, 'dashboard.html', context=context)