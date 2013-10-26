# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset
from django.utils.translation import ugettext as _

from exams.models import Order, OrderItem, Candidate, ExamRegistration
from django.forms.models import inlineformset_factory

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.add_input(Reset('reset', _('Reset')))

    class Meta:
        model = Order
        exclude = ['status', 'date', 'parent',]

OrderFormset = inlineformset_factory(Order, OrderItem, extra=3)


class CandidateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.add_input(Reset('reset', _('Reset')))

    class Meta:
        model = Candidate
        exclude = ['merge_with', 'gender', 'first_name', 'birthday',]

#CandidateFormSet = formset_factory(CandidateForm)
CandidateRegistrationFormset = inlineformset_factory(Candidate, ExamRegistration, extra=5)
