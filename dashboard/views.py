from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now

from gadgets.forms import GadgetForm
from gadgets.models import SetingsCRM
from klienty.models import Klient
from notes.form import *
from workers.models import *


@login_required(login_url='login')
def index_dash(request):
    notatki = Note.objects.order_by('-created_at')[0:20]
    gadgets_all = Gadget.objects.all()
    techniki = User.objects.all()
    qnt_gadgetsq = gadgets_all.__len__()
    gadgets_ok = gadgets_all.filter(status__icontains='GOTOWY').__len__()
    gadgets_serwis = gadgets_all.filter(status__icontains='NAPRAWIENIE').__len__()
    gadgets_czeka = gadgets_all.filter(status__icontains='CZEKA NA CZĘŚCI').__len__()

    context = {
        'now': TODAY,
        'techniki': techniki,
        'gadgets_serwis': gadgets_serwis,
        'gadgets_ok': gadgets_ok,
        'qnt_gadgets': qnt_gadgetsq,
        'gadgets_czeka': gadgets_czeka,
        'notatki': notatki,
    }

    return render(request, 'dashboard/dashboard.html', context=context)

@login_required(login_url='login')
def kartka_napraw(request, pk):

    global serching_gad
    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        gadgets_list = klient.gadget_set.all()
        gadgets_list_in_serwis = klient.gadget_set.filter(in_serwis=True)

        if SetingsCRM.objects.get(pk=1).filter_gadget == 'WSZYSCY':
            serching_gad = gadgets_list

        if SetingsCRM.objects.get(pk=1).filter_gadget == 'W SERWISIE':
            serching_gad = gadgets_list_in_serwis

        paginator = Paginator(serching_gad, 50)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())

        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())

        else:
            next_url = ''
        setings_filter = SetingsCRM.objects.get(pk=1)
        users = User.objects.all()
        context = {
            'filters': setings_filter,
            'users': users,
            'gadgets': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
            'klient': klient,
        }

        return render(request, 'klienty/add_serwise.html', context=context)