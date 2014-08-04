

from django import forms
from django.forms.formsets import formset_factory


class VoteForm(forms.Form):
    summary = forms.CharField()
    descr   = forms.CharField()
    q1      = forms.CharField()
    q2      = forms.CharField()
    q3      = forms.CharField()

VoteFormSet = formset_factory(VoteForm, extra=1)

