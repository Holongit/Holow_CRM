from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from gadgets.forms import GadgetForm, OpisNaprawyForm
from gadgets.models import Gadget, SetingsCRM
from workers.models import Workers
from workers.views import add_gadget_to_worker
from klienty.models import Klient


@login_required(login_url='login')
def index_gad(request):
    search_query = request.GET.get('q', '')
    if search_query.isnumeric():
        search_query_int = int(search_query)
    else:
        search_query_int = 0

    if SetingsCRM.objects.get(pk=1).filter_gadget == 'WSZYSCY':
        gadget_in_serwis = Gadget.objects.all()

    if SetingsCRM.objects.get(pk=1).filter_gadget == 'W SERWISIE':
        gadget_in_serwis = Gadget.objects.filter(in_serwis=True)


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
    }

    return render(request, 'gadgets/gadgets.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddGadgets(View):
    def get(self, request):
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

        return render(request, 'gadgets/add_gadget.html', context=context)

    # def post(self, request):
    #     bound_form_gad = GadgetForm(request.POST)
    #
    #     if bound_form_gad.is_valid():
    #         bound_form_gad.save()
    #
    #         return redirect('gadgets')
    #     return redirect('add_gadget')





@method_decorator(login_required(login_url='login'), name="dispatch")
class EditGadget(View):
    def get(self, request, **kwargs):
        gadget_id = Gadget.objects.get(id=kwargs['pk'])

        bound_form_gad = GadgetForm(initial={
            'opis_naprawy': gadget_id.opis_naprawy,
            'serial_gadget': gadget_id.serial_gadget,
            'model_gadget': gadget_id.model_gadget,
            'brand_gadget': gadget_id.brand_gadget,
            'password_gadget': gadget_id.password_gadget,
            'opis_problem': gadget_id.opis_problem,
            'zestaw': gadget_id.zestaw,
            'type_gadget': gadget_id.type_gadget
            })

        return render(request, 'gadgets/edit_gadget.html', context={'gadget': gadget_id, 'form_class': bound_form_gad})

    def post(self, request, **kwargs):
        bound_form_gad = GadgetForm(request.POST)
        gadget_edit = Gadget.objects.get(id=kwargs['pk'])
        if bound_form_gad.is_valid():
            gadget_edit.serial_gadget = request.POST['serial_gadget']
            gadget_edit.model_gadget = request.POST['model_gadget']
            gadget_edit.brand_gadget = request.POST['brand_gadget']
            gadget_edit.password_gadget = request.POST['password_gadget']
            gadget_edit.opis_problem = request.POST['opis_problem']
            gadget_edit.zestaw = request.POST['zestaw']
            gadget_edit.type_gadget = request.POST['type_gadget']
            gadget_edit.type_service = request.POST['type_service']
            gadget_edit.opis_naprawy = request.POST['opis_naprawy']
            gadget_edit.save()

            return redirect('outgo_gadget', pk=kwargs['pk'])
        return redirect(request.META.get('HTTP_REFERER'), pk=kwargs['pk'])


@method_decorator(login_required(login_url='login'), name='dispatch')
class OutgoGadget(View):
    def get(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        notes = gadget.note_set.all()
        return render(request, 'gadgets/outgo_gadget.html', context={'gadget': gadget, 'notes': notes})

    def post(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        if gadget.in_serwis:
            gadget.in_serwis = False
            gadget.save()
        elif not gadget.in_serwis:
            gadget.in_serwis = True
            gadget.save()
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def delete_gadget(request, pk):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def gadget_status_change(request, pk, status):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.status = status
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def service_status_change(request, pk, status):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.type_service = status
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def filters_gadget_change(request, status):
    setings_f = get_object_or_404(SetingsCRM.objects.all(), pk=1)
    setings_f.filter_gadget = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def print_gadget(request, pk):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    return render(request, 'gadgets/print_gadget.html', context={'gadget': gadget})


@login_required(login_url='login')
def pilne_status_change(request, pk, status):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.pilne = status
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def technik_change(request, gadget_id, user_id):
    if Workers.objects.filter(gadget__id=gadget_id):
        worker_change = Workers.objects.get(gadget__id=gadget_id)
        worker_change.worker = User.objects.get(pk=user_id)
        worker_change.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        add_gadget_to_worker(request, gadget_id)
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def add_opis_naprawy(request, pk):
    if request.method == "GET":
        gadget = Gadget.objects.get(pk=pk)
        form = OpisNaprawyForm(initial={'opis_naprawy': gadget.opis_naprawy})
        notes = gadget.note_set.all()
        return render(request, 'gadgets/add_opis_naprawy.html', context={'form': form, 'gadget': gadget, 'notes': notes})

    if request.method == "POST":
        bound_form = OpisNaprawyForm(request.POST)
        if bound_form.is_valid():
            gadget = Gadget.objects.get(pk=pk)
            gadget.opis_naprawy = request.POST['opis_naprawy']
            gadget.save()
            return redirect('outgo_gadget', pk=pk)
        return redirect(request.META.get('HTTP_REFERER'))
