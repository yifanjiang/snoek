

from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory


class VoteForm(forms.Form):

#need to set limit of all the fields in the future. TODO
    summary = forms.CharField()
    descr   = forms.CharField()
    q1      = forms.CharField()
    pic1    = forms.ImageField()

VoteFormSet = formset_factory(VoteForm, extra=1)

