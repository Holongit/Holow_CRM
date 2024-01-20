from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from gadgets.forms import GadgetForm
from gadgets.models import SetingsCRM, Gadget
from klienty.forms import KlientForm
from klienty.models import Klient




def index_kli(request):
    search_query = request.GET.get('q', '')

    if search_query:
        serching_kli = Klient.objects.filter(Q(name_klient__icontains=search_query) |
                                             Q(telefon_klient__icontains=search_query))
    else:
        serching_kli = Klient.objects.all()
    paginator = Paginator(serching_kli, 14)
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
    context = {
        'klients': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'klienty/klienty.html', context=context)


class AddKlient(View):
    def get(self, request):
        form_kli = KlientForm()

        return render(request, 'klienty/add_klient.html', context={'form_kli': form_kli})

    def post(self, request):
        bound_form_kli = KlientForm(request.POST)

        if bound_form_kli.is_valid():
            bound_form_kli.save()

            return redirect('add_gadget')

        return redirect('add_klient')


def kartka_klienta(request, pk):

    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        notes = klient.note_set.all()

        return render(request, 'klienty/kartka_klienta.html', context={'klient': klient, 'notes': notes})

def add_serwis(request, pk):

    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        notes = klient.note_set.all()
        gadgets_list = klient.gadget_set.all()
        gadgets_list_in_serwis = klient.gadget_set.filter(in_serwis=True)
        search_query = request.GET.get('q', '')

        if search_query.isnumeric():
            search_query_int = int(search_query)
        else:
            search_query_int = 0

        if SetingsCRM.objects.get(pk=1).filter_gadget == 'WSZYSCY':
            gadget_in_serwis = gadgets_list

        if SetingsCRM.objects.get(pk=1).filter_gadget == 'W SERWISIE':
            gadget_in_serwis = gadgets_list_in_serwis

        if search_query:
            serching_gad = gadget_in_serwis.filter(Q(brand_gadget__icontains=search_query) |
                                                   Q(model_gadget__icontains=search_query) |
                                                   Q(serial_gadget__icontains=search_query) |
                                                   Q(klient__name_klient__icontains=search_query) |
                                                   Q(id=search_query_int) |
                                                   Q(klient__telefon_klient__icontains=search_query))
        else:
            serching_gad = gadget_in_serwis
        paginator = Paginator(serching_gad, 14)
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
            'notes': notes,
        }

        return render(request, 'klienty/add_serwise.html', context=context)

def add_gadget_serwis(request, pk):
    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        notes = klient.note_set.all()
        form_gad = GadgetForm()
        return render(request, 'gadgets/add_gadget_serwis.html', {'klient': klient, 'notes': notes, 'form_gad': form_gad})

    if request.method == 'POST':
        bound_form_gad = GadgetForm(request.POST)

        if bound_form_gad.is_valid():
            bound_form_gad.save()
            gadget = Gadget.objects.first()
            gadget.klient = Klient.objects.get(pk=pk)
            gadget.save()

            return redirect('outgo_gadget', pk=gadget.id)
        return redirect(request.META.get('HTTP_REFERER'), pk=pk)

