from django import forms
from django.core.validators import RegexValidator
from django.forms import RadioSelect

from gadgets.models import *
from klienty.models import *



class GadgetForm(forms.Form):
    CHOICES = (
        ('Laptop', 'Laptop'),
        ('Telefone', 'Telefone'),
        ('Tablet', 'Tablet'),
        ('Komputer Stacjonarny', 'Komputer Stacjonarny'),
        ('Monitop', 'Monitor'),
        ('inne urządzenie', 'Inne Urządzenie'),
    )
    CHOICES2 = (
        ('PŁATNE', 'PŁATNE'),
        ('GWARANCJA', 'GWARANCJA'),
        ('REKLAMACJA', 'REKLAMACJA')
    )

    serial_gadget = forms.CharField(max_length=32, required=False)
    model_gadget = forms.CharField(max_length=32)
    brand_gadget = forms.CharField(max_length=32)
    password_gadget = forms.CharField(max_length=64, required=False)
    opis_problem = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), required=False)
    zestaw = forms.CharField(max_length=64, required=False)
    type_gadget = forms.ChoiceField(choices=CHOICES)
    type_service = forms.ChoiceField(choices=CHOICES2)
    klient = forms.CharField(max_length=64, required=False)
    opis_naprawy = forms.CharField(max_length=512, required=False)

    serial_gadget.widget.attrs.update({'class': 'form-control'})
    model_gadget.widget.attrs.update({'class': 'form-control'})
    brand_gadget.widget.attrs.update({'class': 'form-control'})
    password_gadget.widget.attrs.update({'class': 'form-control'})
    zestaw.widget.attrs.update({'class': 'form-control'})
    type_gadget.widget.attrs.update({'class': 'form-control'})
    type_service.widget.attrs.update({'class': 'form-control'})
    opis_naprawy.widget.attrs.update({'class': 'form-control'})

    def save(self):
        new_gadget = Gadget.objects.create(
            serial_gadget=self.cleaned_data['serial_gadget'],
            model_gadget=self.cleaned_data['model_gadget'],
            brand_gadget=self.cleaned_data['brand_gadget'],
            password_gadget=self.cleaned_data['password_gadget'],
            opis_problem=self.cleaned_data['opis_problem'],
            zestaw=self.cleaned_data['zestaw'],
            type_gadget=self.cleaned_data['type_gadget'],
            type_service=self.cleaned_data['type_service'],
            opis_naprawy=self.cleaned_data['opis_naprawy']
        )
        return new_gadget


class OpisNaprawyForm(forms.Form):

    opis_naprawy = forms.CharField(max_length=512)
    opis_naprawy.widget.attrs.update({'class': 'form-control'})

    def save(self):
        new_opis_naprawy = Gadget.objects.create(
            opis_naprawy=self.cleaned_data['opis_naprawy'],
        )
        return new_opis_naprawy


