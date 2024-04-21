from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from gadgets.forms import GadgetForm, OpisNaprawyForm
from gadgets.models import Gadget, SetingsCRM
from notes.models import Note
from notes.form import NoteForm
from workers.models import Workers
from workers.views import add_gadget_to_worker
from klienty.models import Klient
import re


@login_required(login_url='login')
def index_manager(request):
    user = request.user
    global gadget_in_serwis
    search_query = request.GET.get('q', '')
    if search_query.isnumeric():
        search_query_int = int(search_query)
    else:
        search_query_int = 0

    # cleaned_phone_number = re.sub(r'\D', '', search_query)

    warning_list_gadget = Gadget.objects.filter(in_serwis=True, alarm_on=True).order_by('-alarm_at')
    all_gadget_list = Gadget.objects.filter(in_serwis=True)

    if not SetingsCRM.objects.filter(user_id=user.id).exists():
        SetingsCRM.objects.create(user_id=user.id)

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == 'CAŁY CZAS':
        gadget_in_serwis = warning_list_gadget

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '1 DZIEŃ':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=1))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '2 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=2))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '7 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=7))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '14 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=14))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '30 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=30))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == '60 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__gt=timezone.now() - timedelta(days=60))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == 'PONAD 60 DNI':
        gadget_in_serwis = warning_list_gadget.filter(alarm_at__lt=timezone.now() - timedelta(days=60))

    if SetingsCRM.objects.get(user_id=user.id).filter_manager == 'WSZYSTKIE':
        gadget_in_serwis = all_gadget_list

    if len(str(search_query_int)) <= 5 and search_query_int > 0:
        serching_gad = gadget_in_serwis.filter(id=search_query_int)

    elif search_query:
        serching_gad = gadget_in_serwis.filter(Q(brand_gadget__icontains=search_query) |
                                               Q(model_gadget__icontains=search_query) |
                                               Q(serial_gadget__icontains=search_query) |
                                               Q(klient__name_klient__icontains=search_query) |
                                               Q(password_gadget__icontains=search_query) |
                                               Q(klient__telefon_klient__icontains=search_query))
    else:
        serching_gad = gadget_in_serwis

    paginator = Paginator(serching_gad, 300)

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

    setings_filter = SetingsCRM.objects.get(user_id=user.id)
    users = User.objects.all()

    context = {
        'filters': setings_filter,
        'users': users,
        'gadgets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'manager/index_manager.html', context)


@login_required(login_url='login')
def alarm_at_change(request, pk):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    if gadget.alarm_on is True:
        gadget.alarm_on = False
    else:
        gadget.alarm_on = True
    gadget.alarm_at = timezone.now()
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def settings_manager_status_filter_change(request, status_filter, status_filter_id):
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    if status_filter_id == 'G':
        setings_f.filter_manager_gotowy = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'N':
        setings_f.filter_manager_nowy = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'Z':
        setings_f.filter_manager_zaliczka = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'R':
        setings_f.filter_manager_rezygnacja = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'O':
        setings_f.filter_manager_czeka_na_zgode = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'W':
        setings_f.filter_manager_wycena = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'D':
        setings_f.filter_manager_diagnostyka = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'C':
        setings_f.filter_manager_czeka_na_części = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'A':
        setings_f.filter_manager_naprawienie = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if status_filter_id == 'L':
        setings_f.filter_manager_all = status_filter
        setings_f.filter_manager_gotowy = status_filter
        setings_f.filter_manager_diagnostyka = status_filter
        setings_f.filter_manager_naprawienie = status_filter
        setings_f.filter_manager_rezygnacja = status_filter
        setings_f.filter_manager_nowy = status_filter
        setings_f.filter_manager_czeka_na_części = status_filter
        setings_f.filter_manager_czeka_na_zgode = status_filter
        setings_f.filter_manager_wycena = status_filter
        setings_f.filter_manager_zaliczka = status_filter
        setings_f.save()
        return redirect(request.META.get('HTTP_REFERER'))
