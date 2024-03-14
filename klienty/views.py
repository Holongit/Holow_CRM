from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from gadgets.forms import GadgetForm
from gadgets.models import SetingsCRM, Gadget
from klienty.forms import KlientForm
from klienty.models import Klient


@login_required(login_url='login')
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddKlient(View):
    def get(self, request):
        form_kli = KlientForm()

        return render(request, 'klienty/add_klient.html', context={'form_kli': form_kli})

    def post(self, request):
        bound_form_kli = KlientForm(request.POST)

        if bound_form_kli.is_valid():
            bound_form_kli.save()
            pk = Klient.objects.first().id

            return redirect('add_gadget_serwis', pk=pk)

        return redirect('add_klient')


@login_required(login_url='login')
def kartka_klienta(request, pk):
    global serching_gad, gadget_in_serwis
    user = request.user

    if request.method == 'GET':

        search_query = request.GET.get('q', '')
        if search_query.isnumeric():
            search_query_int = int(search_query)
        else:
            search_query_int = 0

        klient = Klient.objects.get(pk=pk)
        gadgets_list = klient.gadget_set.all()
        gadgets_list_in_serwis = klient.gadget_set.filter(in_serwis=True)

        if not SetingsCRM.objects.filter(user_id=user.id).exists():
            SetingsCRM.objects.create(user_id=user.id)

        if SetingsCRM.objects.get(user_id=user.id).filter_klient == 'WSZYSCY':
            gadget_in_serwis = gadgets_list

        if SetingsCRM.objects.get(user_id=user.id).filter_klient == 'W SERWISIE':
            gadget_in_serwis = gadgets_list_in_serwis

        if len(str(search_query_int)) <= 5 and search_query_int > 0:
            serching_gad = gadget_in_serwis.filter(id=search_query_int)

        elif search_query:
            serching_gad = gadget_in_serwis.filter(Q(brand_gadget__icontains=search_query) |
                                                   Q(model_gadget__icontains=search_query) |
                                                   Q(serial_gadget__icontains=search_query) |
                                                   Q(password_gadget__icontains=search_query))
        else:
            serching_gad = gadget_in_serwis

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
        setings_filter = SetingsCRM.objects.get(user_id=user.id)
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


        return render(request, 'klienty/kartka_klienta.html', context=context)



@login_required(login_url='login')
def add_gadget_serwis(request, pk):
    user = request.user
    location = SetingsCRM.objects.get(user_id=user.id).filter_dashboar
    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        notes = klient.note_set.all()
        form_gad = GadgetForm()
        context = {'klient': klient,
                   'notes': notes,
                   'form_gad': form_gad
                   }
        return render(request, 'gadgets/add_gadget_serwis.html', context=context)

    if request.method == 'POST':
        bound_form_gad = GadgetForm(request.POST)

        if bound_form_gad.is_valid():
            bound_form_gad.save()
            gadget = Gadget.objects.first()
            gadget.klient = Klient.objects.get(pk=pk)
            gadget.location = location
            gadget.save()

            return redirect('outgo_gadget', pk=gadget.id)
        return redirect(request.META.get('HTTP_REFERER'), pk=pk)


@login_required(login_url='login')
def edit_klient(request, pk):
    if request.method == 'GET':
        klient = Klient.objects.get(pk=pk)
        form_kli = KlientForm(initial={
            'name_klient': klient.name_klient,
            'telefon_klient': klient.telefon_klient,
            'email_klient': klient.email_klient,
            'opis_klient': klient.opis_klient,
            'type_klient': klient.types_klient,
        })
        return render(request, 'klienty/edit_klient.html', context={'klient': klient, 'form_class': form_kli})

    if request.method == 'POST':
        boun_form_kli = KlientForm(request.POST)
        klient_edit = Klient.objects.get(pk=pk)
        if boun_form_kli.is_valid():
            klient_edit.name_klient = request.POST['name_klient']
            klient_edit.telefon_klient = request.POST['telefon_klient']
            klient_edit.email_klient = request.POST['email_klient']
            klient_edit.opis_klient = request.POST['opis_klient']
            klient_edit.types_klient = request.POST['types_klient']
            klient_edit.save()

            return redirect('kartka_klienta', pk=pk)
        return redirect(request.META.get('HTTP_REFERER'), pk=pk)


@login_required(login_url='login')
def delete_klient(request, pk):
    klient = Klient.objects.get(pk=pk)
    try:
        klient.delete()
    except:
        messages.success(request, 'Klient ma urządzenia. Najpierw usuń wszystkie urządzenia klienta!')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def filters_klient_change(request, status):
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    setings_f.filter_klient = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))
