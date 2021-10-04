from django import forms
from django.forms.fields import CharField
class SubscriptionForm(forms.Form):
   name = forms.CharField(label='Nome')
   cpf = forms.CharField(label='CPF')
   email = forms.EmailField(label='Email')
   phone = forms.CharField(label='Telefone')