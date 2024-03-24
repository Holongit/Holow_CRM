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

    warning_list_gadget = Gadget.objects.filter(status='NOWY')

    if not SetingsCRM.objects.filter(user_id=user.id).exists():
        SetingsCRM.objects.create(user_id=user.id)

    if SetingsCRM.objects.get(user_id=user.id).filter_gadget == 'WSZYSCY':
        gadget_in_serwis = warning_list_gadget

    if SetingsCRM.objects.get(user_id=user.id).filter_gadget == 'W SERWISIE':
        gadget_in_serwis = Gadget.objects.filter(in_serwis=True)

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

    paginator = Paginator(serching_gad, 40)

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
