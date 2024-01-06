from django import forms
from django.core.validators import RegexValidator
from django.forms import RadioSelect



# class KlientForm(forms.ModelForm):
#     class Meta:
#         model = Klient
#         fields = ['name_klient',
#                   'telefon_klient',
#                   'email_klient'
#                   ]
#
#         widgets = {
#             'name_klient': forms.TextInput(attrs={'class': 'form-control'}),
#             'telefon_klient': forms.TextInput(attrs={'class': 'form-control'}),
#             'email_klient': forms.EmailInput(attrs={'class': 'form-control'})
#         }
#
#     def save(self):
#         new_klient = Klient.objects.create(
#             name_klient=self.cleaned_data['name_klient'],
#             telefon_klient=self.cleaned_data['telefon_klient'],
#             email_klient=self.cleaned_data['email_klient'],
#         )
#         return new_klient

