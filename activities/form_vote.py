

from django import forms
from django.forms import ModelForm

class VoteForm(forms.Form):

#need to set limit of all the fields in the future. TODO
    q_count = forms.CharField(widget=forms.HiddenInput())
    summary = forms.CharField(required=False)
    descr   = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 1)
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['q_count'].initial = extra_fields
        for i in range(int(extra_fields)):
            self.fields['q{0}'.format(i+1)] = forms.CharField(required=False)
            self.fields['pic{0}'.format(i+1)] = forms.ImageField(required=False)

class VoteForm1(forms.Form):

#need to set limit of all the fields in the future. TODO
    q_count = forms.CharField(widget=forms.HiddenInput())
    summary = forms.CharField(required=False)
    descr   = forms.CharField(required=False)
    q1 = forms.CharField(required=False)
    pic1 = forms.ImageField(required=False)
    q2 = forms.CharField(required=False)
    pic2 = forms.ImageField(required=False)
    q3 = forms.CharField(required=False)
    pic3 = forms.ImageField(required=False)
