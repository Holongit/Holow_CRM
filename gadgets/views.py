from datetime import datetime

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
from workers.views import add_gadget_to_worker, odstawic_gadget
from klienty.models import Klient


@login_required(login_url='login')
def index_gad(request):
    user = request.user
    global gadget_in_serwis
    search_query = request.GET.get('q', '')
    date_range = request.GET.get('date_range', '')
    if search_query.isnumeric():
        search_query_int = int(search_query)
    else:
        search_query_int = 0

    date_one = date_range[:10]
    date_two = date_range[14:]

    if not SetingsCRM.objects.filter(user_id=user.id).exists():
        SetingsCRM.objects.create(user_id=user.id)

    if date_range:
        date_one_date_time_obj = datetime.strptime(date_one, '%Y-%m-%d')
        date_two_date_time_obj = datetime.strptime(date_two, '%Y-%m-%d')
        gadget_date_range = Gadget.objects.filter(created_at__gt=date_one_date_time_obj,
                                                  created_at__lt=date_two_date_time_obj,
                                                  )

        if SetingsCRM.objects.get(user_id=user.id).filter_gadget == 'WSZYSCY':
            gadget_in_serwis = gadget_date_range

        if SetingsCRM.objects.get(user_id=user.id).filter_gadget == 'W SERWISIE':
            gadget_in_serwis = gadget_date_range.filter(in_serwis=True)
    else:
        if SetingsCRM.objects.get(user_id=user.id).filter_gadget == 'WSZYSCY':
            gadget_in_serwis = Gadget.objects.all()

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

    paginator = Paginator(serching_gad, 80)

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

        paginator = Paginator(serching_kli, 40)

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
            'usterki_zewn': gadget_id.usterki_zewn,
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
            gadget_edit.usterki_zewn = request.POST['usterki_zewn']
            gadget_edit.save()

            return redirect('outgo_gadget', pk=kwargs['pk'])
        return redirect(request.META.get('HTTP_REFERER'), pk=kwargs['pk'])


@method_decorator(login_required(login_url='login'), name='dispatch')
class OutgoGadget(View):
    def get(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        notes = gadget.note_set.all()
        form = NoteForm(initial={'title': 'none'})
        return render(request, 'gadgets/outgo_gadget.html', context={'gadget': gadget, 'form': form, 'notes': notes})

    def post(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        user = request.user
        if gadget.in_serwis:
            gadget.in_serwis = False
            gadget.updated_at = timezone.now()
            if Workers.objects.filter(gadget=gadget) and gadget.workers.in_work:
                worker_pk = gadget.workers.id
                odstawic_gadget(request, worker_pk)
                Note.objects.create(
                    author=User.objects.get(username='TPL'),
                    title='URZĄDZENIE WYDANE KLIENTOWI',
                    content=f'{user} menedżer, urządzenie zostało wydane, ale technik nie odłożył go na półkę!',
                    gadget=gadget,
                )
            else:
                Note.objects.create(
                    author=User.objects.get(username='TPL'),
                    title='URZĄDZENIE WYDANE KLIENTOWI',
                    content=f'{user} menedżer',
                    gadget=gadget,
                )
            gadget.save()
        elif not gadget.in_serwis:
            gadget.in_serwis = True
            gadget.updated_at = timezone.now()
            gadget.status = 'NOWY'
            Note.objects.create(
                author=User.objects.get(username='TPL'),
                title='URZĄDZENIE PRZYJĘTE OD KLIENTA',
                content=f'{user} menedżer',
                gadget=gadget,
            )
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
    gadget.managed_at = timezone.now()
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
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    setings_f.filter_gadget = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def filters_manager_change(request, status):
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    setings_f.filter_manager = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def filters_dashboar_change(request, status):
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    setings_f.filter_dashboar = status
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
        user = User.objects.get(pk=user_id)
        gadget = Gadget.objects.get(pk=gadget_id)
        worker_change = Workers.objects.get(gadget__id=gadget_id)
        Note.objects.create(
            author=User.objects.get(username='TPL'),
            title='ZMIANA TECHNIKA',
            content=f'{user} wziął do naprawy {gadget.id} {gadget} od {worker_change.worker}',
            gadget=gadget,
        )
        worker_change.worker = user
        worker_change.updated_at = timezone.now()
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
        return render(request, 'gadgets/add_opis_naprawy.html',
                      context={'form': form, 'gadget': gadget, 'notes': notes})

    if request.method == "POST":
        bound_form = OpisNaprawyForm(request.POST)
        if bound_form.is_valid():
            gadget = Gadget.objects.get(pk=pk)
            gadget.opis_naprawy = request.POST['opis_naprawy']
            gadget.save()
            return redirect('gadget_info', pk=pk)
        return redirect(request.META.get('HTTP_REFERER'))
