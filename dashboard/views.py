from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now

from notes.form import *


@login_required(login_url='login')
def index_dash(request):
    notatki = Note.objects.order_by('-created_at')[0:20]
    gadgets_all = Gadget.objects.all()
    qnt_gadgetsq = gadgets_all.__len__()
    gadgets_ok = gadgets_all.filter(status__icontains='GOTOWY').__len__()
    gadgets_serwis = gadgets_all.filter(status__icontains='NAPRAWIENIE').__len__()
    gadgets_czeka = gadgets_all.filter(status__icontains='CZEKA NA CZĘŚCI').__len__()

    context = {
        'gadgets_serwis': gadgets_serwis,
        'gadgets_ok': gadgets_ok,
        'qnt_gadgets': qnt_gadgetsq,
        'gadgets_czeka': gadgets_czeka,
        'notatki': notatki,
    }

    return render(request, 'dashboard.html', context=context)

