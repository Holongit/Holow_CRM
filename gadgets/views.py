from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy

from gadgets.forms import GadgetForm
from gadgets.models import Gadget, SetingsCRM


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
                                               Q(master_gadget__icontains=search_query) |
                                               Q(id=search_query_int) |
                                               Q(telefon_master_gadget__icontains=search_query))
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

    context = {
        'filters': setings_filter,
        'gadgets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'gadgets/gadgets.html', context)


class AddGadgets(View):
    def get(self, request):
        form_gad = GadgetForm()

        return render(request, 'gadgets/add_gadget.html', context={'form_gad': form_gad})

    def post(self, request):
        bound_form_gad = GadgetForm(request.POST)

        if bound_form_gad.is_valid():
            bound_form_gad.save()

            return redirect('gadgets')
        return redirect('add_gadget')


class EditGadget(View):
    def get(self, request, **kwargs):
        bound_form_gad = GadgetForm(initial={'master_gadget': Gadget.objects.get(id=kwargs['pk']).master_gadget,
                                             'telefon_master_gadget': Gadget.objects.get(
                                                 id=kwargs['pk']).telefon_master_gadget,
                                             'serial_gadget': Gadget.objects.get(id=kwargs['pk']).serial_gadget,
                                             'model_gadget': Gadget.objects.get(id=kwargs['pk']).model_gadget,
                                             'brand_gadget': Gadget.objects.get(id=kwargs['pk']).brand_gadget,
                                             'password_gadget': Gadget.objects.get(id=kwargs['pk']).password_gadget,
                                             'opis_problem': Gadget.objects.get(id=kwargs['pk']).opis_problem,
                                             'zestaw': Gadget.objects.get(id=kwargs['pk']).zestaw,
                                             'type_gadget': Gadget.objects.get(id=kwargs['pk']).type_gadget
                                             })
        gadget_id = Gadget.objects.get(id=kwargs['pk'])
        return render(request, 'gadgets/edit_gadget.html', context={'gadget': gadget_id, 'form_class': bound_form_gad})

    def post(self, request, **kwargs):
        bound_form_gad = GadgetForm(request.POST)
        gadget_edit = Gadget.objects.get(id=kwargs['pk'])
        if bound_form_gad.is_valid():
            gadget_edit.master_gadget = request.POST['master_gadget']
            gadget_edit.telefon_master_gadget = request.POST['telefon_master_gadget']
            gadget_edit.serial_gadget = request.POST['serial_gadget']
            gadget_edit.model_gadget = request.POST['model_gadget']
            gadget_edit.brand_gadget = request.POST['brand_gadget']
            gadget_edit.password_gadget = request.POST['password_gadget']
            gadget_edit.opis_problem = request.POST['opis_problem']
            gadget_edit.zestaw = request.POST['zestaw']
            gadget_edit.type_gadget = request.POST['type_gadget']
            gadget_edit.type_service = request.POST['type_service']
            gadget_edit.save()

            return redirect('outgo_gadget', pk=kwargs['pk'])
        return redirect(request.META.get('HTTP_REFERER'), pk=kwargs['pk'])


class OutgoGadget(View):
    def get(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        return render(request, 'gadgets/outgo_gadget.html', context={'gadget': gadget})

    def post(self, request, pk):
        gadget = Gadget.objects.get(id=pk)

        if gadget.in_serwis:
            gadget.in_serwis = False
            gadget.save()
        elif not gadget.in_serwis:
            gadget.in_serwis = True
            gadget.save()

        return redirect(request.META.get('HTTP_REFERER'))


def delete_gadget(request, pk):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def gadget_status_change(request, pk, status):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.status = status
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


def service_status_change(request, pk, status):
    gadget = get_object_or_404(Gadget.objects.all(), pk=pk)
    gadget.type_service = status
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))


def filters_gadget_change(request, status):
    setings_f = get_object_or_404(SetingsCRM.objects.all(), pk=1)
    setings_f.filter_gadget = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))
