from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from gadgets.models import SetingsCRM
from notes.form import *
from workers.models import *



@login_required(login_url='login')
def index_dash(request):
    notatki = Note.objects.order_by('-created_at')[0:20]
    gadgets_all = Gadget.objects.all()
    techniki = User.objects.all()
    tpl = User.objects.get(id=1)

    gadgets_in_serwis = gadgets_all.filter(in_serwis=True)
    gadgets_in_serwis_count = gadgets_in_serwis.count()
    # qnt_gadgets_month = gadgets_all.filter(created_at__month=TODAY.month).count()
    gadgets_ok = gadgets_in_serwis.filter(workers__in_work=False).count()
    gadgets_serwis = Workers.objects.filter(in_work=True, gadget__in_serwis=True).count()
    gadgets_new_count = gadgets_in_serwis.filter(status__icontains='NOWY').count()

    context = {
        'gadgets_all': gadgets_all,
        'tpl': tpl,
        'now': TODAY,
        'techniki': techniki,
        'gadgets_serwis': gadgets_serwis,
        'gadgets_ok': gadgets_ok,
        'qnt_gadgets': gadgets_in_serwis_count,
        'gadgets_new_count': gadgets_new_count,
        'notatki': notatki,

    }

    return render(request, 'dashboard/dashboard.html', context=context)


@login_required(login_url='login')
def kartka_napraw(request, pk):

    if request.method == 'GET':
        month_select = request.GET.get('month', TODAY.month)
        technik = User.objects.get(pk=pk)
        curent_user = request.user
        setings_filter = SetingsCRM.objects.get(user_id=curent_user.id)
        users = User.objects.all()

        if TODAY.month - int(month_select) >= 0:
            month = int(month_select)
        else:
            month = TODAY.month

        płatne = technik.kartkaplatne_set.filter(created_at__month=month)
        gwarancja = technik.kartkagwarancja_set.filter(created_at__month=month)
        reklamacja = technik.kartkareklamacja_set.filter(created_at__month=month)
        rezygnacja = technik.kartkarezygnacja_set.filter(created_at__month=month)

        context = {
            'month': month,
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

