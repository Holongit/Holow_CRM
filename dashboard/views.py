from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from gadgets.models import SetingsCRM
from notes.form import *
from workers.models import *


@login_required(login_url='login')
def index_dash(request):
    notatki = Note.objects.order_by('-created_at')[0:20]
    gadgets_all = Gadget.objects.all()
    techniki = User.objects.all()
    tpl = User.objects.get(id=1)
    qnt_gadgetsq = gadgets_all.__len__()
    gadgets_ok = gadgets_all.filter(status__icontains='GOTOWY').__len__()
    gadgets_serwis = gadgets_all.filter(status__icontains='NAPRAWIENIE').__len__()
    gadgets_czeka = gadgets_all.filter(status__icontains='CZEKA NA CZĘŚCI').__len__()

    context = {
        'tpl': tpl,
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
def kartka_napraw(request, pk, kartka):
    global gadgets_list_all
    global serching_gad
    if request.method == 'GET':
        user = User.objects.get(pk=pk)

        if kartka == 'płatne':
            gadgets_list_all = user.kartkaplatne_set.all()
        if kartka == 'gwarancja':
            gadgets_list_all = user.kartkagwarancja_set.all()
        if kartka == 'reklamacja':
            gadgets_list_all = user.kartkareklamacja_set.all()
        if kartka == 'rezygnacja':
            gadgets_list_all = user.kartkarezygnacja_set.all()

        gadgets_list_month = gadgets_list_all.filter(created_at__month=TODAY.month)

        if SetingsCRM.objects.get(pk=1).filter_dashboar == 'MIESIĄC':
            serching_gad = gadgets_list_month

        if SetingsCRM.objects.get(pk=1).filter_dashboar == 'WSZYSCY':
            serching_gad = gadgets_list_all

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
            'now': TODAY,
            'filters': setings_filter,
            'users': users,
            'gadgets': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
            'technik': user,
        }

        return render(request, 'dashboard/kartka_napraw.html', context=context)


@login_required(login_url='login')
def filters_dashboard_change(request, status):
    setings_f = get_object_or_404(SetingsCRM.objects.all(), pk=1)
    setings_f.filter_dashboar = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))