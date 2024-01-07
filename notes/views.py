from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy

from gadgets.forms import GadgetForm
from gadgets.models import Gadget, SetingsCRM
from notes.form import NoteForm
from notes.models import Note


class NoteAdd(View):
    def get(self, request, **kwargs):
        gadget = Gadget.objects.get(id=kwargs['pk'])
        notes = gadget.note_set.all()
        form = NoteForm(initial={'title': 'none'})

        return render(request, 'notes/add_note.html', context={'gadget': gadget, 'form': form, 'notes': notes})

    def post(self, request, **kwargs):
        bound_form_note = NoteForm(request.POST)
        gadget_id = Gadget.objects.get(id=kwargs['pk'])
        if bound_form_note.is_valid():
            bound_form_note.save()
            note_last = Note.objects.first()
            note_last.gadget_id = gadget_id
            note_last.save()
            return redirect('outgo_gadget', pk=kwargs['pk'])
        return redirect(request.META.get('HTTP_REFERER'))



def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return redirect(request.META.get('HTTP_REFERER'))