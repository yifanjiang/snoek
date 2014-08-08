

from django import forms
from django.forms import ModelForm

class VoteForm(forms.Form):

#need to set limit of all the fields in the future. TODO
    q_count = forms.CharField(widget=forms.HiddenInput())
    summary = forms.CharField()
    descr   = forms.CharField()

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 1)
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['q_count'].initial = extra_fields
        for i in range(int(extra_fields)):
            self.fields['q{0}'.format(i+1)] = forms.CharField()
            self.fields['pic{0}'.format(i+1)] = forms.ImageField()
