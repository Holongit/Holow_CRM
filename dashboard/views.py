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
    qnt_gadgetsq = gadgets_all.filter(in_serwis=True).count()
    gadgets_ok = gadgets_all.filter(status__icontains='GOTOWY').count()
    gadgets_serwis = gadgets_all.filter(status__icontains='NAPRAWIENIE').count()
    gadgets_czeka = gadgets_all.filter(status__icontains='CZEKA NA CZĘŚCI').count()

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
def kartka_napraw(request, pk):

    if request.method == 'GET':
        technik = User.objects.get(pk=pk)
        curent_user = request.user
        setings_filter = SetingsCRM.objects.get(user_id=curent_user.id)
        users = User.objects.all()

        płatne = technik.kartkaplatne_set.all()
        gwarancja = technik.kartkagwarancja_set.all()
        reklamacja = technik.kartkareklamacja_set.all()
        rezygnacja = technik.kartkarezygnacja_set.all()

        context = {
            'now': TODAY,
            'filters': setings_filter,
            'users': users,
            'płatne': płatne,
            'gwarancja': gwarancja,
            'reklamacja': reklamacja,
            'rezygnacja': rezygnacja,
            'technik': technik,
        }

        return render(request, 'dashboard/kartka_napraw.html', context=context)


@login_required(login_url='login')
def filters_dashboard_change(request, status):
    curent_user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=curent_user.id)
    setings_f.filter_dashboar = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))