from django import forms
from django.core.validators import RegexValidator

from gadgets.models import *


class KlientForm(forms.ModelForm):
    class Meta:
        model = Klient
        fields = ['name_klient',
                  'telefon_klient',
                  'email_klient'
                  ]

        widgets = {
            'name_klient': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_klient': forms.TextInput(attrs={'class': 'form-control'}),
            'email_klient': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def save(self):
        new_klient = Klient.objects.create(
            name_klient=self.cleaned_data['name_klient'],
            telefon_klient=self.cleaned_data['telefon_klient'],
            email_klient=self.cleaned_data['email_klient'],
        )
        return new_klient


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

    master_gadget = forms.CharField(max_length=64)
    telefon_master_gadget = forms.RegexField(max_length=32, min_length=9, regex=r'^[0-9]*$')
    serial_gadget = forms.CharField(max_length=32, required=False)
    model_gadget = forms.CharField(max_length=32)
    brand_gadget = forms.CharField(max_length=32)
    password_gadget = forms.CharField(max_length=64, required=False)
    opis_problem = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), required=False)
    zestaw = forms.CharField(max_length=64, required=False)
    type_gadget = forms.ChoiceField(choices=CHOICES)
    type_service = forms.ChoiceField(choices=CHOICES2)

    master_gadget.widget.attrs.update({'class': 'form-control'})
    telefon_master_gadget.widget.attrs.update({'class': 'form-control'})
    serial_gadget.widget.attrs.update({'class': 'form-control'})
    model_gadget.widget.attrs.update({'class': 'form-control'})
    brand_gadget.widget.attrs.update({'class': 'form-control'})
    password_gadget.widget.attrs.update({'class': 'form-control'})
    zestaw.widget.attrs.update({'class': 'form-control'})
    type_gadget.widget.attrs.update({'class': 'form-control'})
    type_service.widget.attrs.update({'class': 'form-control'})

    def save(self):
        new_gadget = Gadget.objects.create(
            master_gadget=self.cleaned_data['master_gadget'],
            telefon_master_gadget=self.cleaned_data['telefon_master_gadget'],
            serial_gadget=self.cleaned_data['serial_gadget'],
            model_gadget=self.cleaned_data['model_gadget'],
            brand_gadget=self.cleaned_data['brand_gadget'],
            password_gadget=self.cleaned_data['password_gadget'],
            opis_problem=self.cleaned_data['opis_problem'],
            zestaw=self.cleaned_data['zestaw'],
            type_gadget=self.cleaned_data['type_gadget'],
            type_service=self.cleaned_data['type_service'],
        )
        return new_gadget
