# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Div, Fieldset, Layout, ButtonHolder

from exams.models import Order, OrderItem, Candidate, ExamRegistration, CandidateUpload


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.add_input(Reset('reset', _('Reset')))

    class Meta:
        model = Order
        exclude = ['status', 'date', 'parent', 'examination', 'created_by',]

OrderFormset = inlineformset_factory(Order, OrderItem, extra=3)

class OrderItemHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OrderItemHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        #self.add_input(Submit("submit", "Save"))
        self.render_required_fields = True
        self.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'    

class ExamRegistrationHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExamRegistrationHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        #self.add_input(Submit("submit", "Save"))
        self.render_required_fields = True
        self.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'

class ExamRegistrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['special_arrangements'].widget = CheckboxSelectMultiple()

    class Meta:
        model = ExamRegistration

class CandidateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False

        #self.helper.add_input(Submit('submit', _('Save')))
        #self.helper.add_input(Reset('reset', _('Reset')))

    class Meta:
        model = Candidate
        exclude = ['merge_with', 'gender', 'first_name', 'birthday', 'school', 'examination', 'retrying', 'candidate_type',]

class CandidateUploadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CandidateUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = True



        self.helper.add_input(Submit('submit', _('Upload')))
        self.helper.add_input(Reset('reset', _('Reset')))

    class Meta:
        model = CandidateUpload
        exclude = ['by_user', 'status', 'examination', 'school', 'order',]

ExamRegistrationFormset = inlineformset_factory(Candidate, ExamRegistration)
ExamRegistrationFormset.form = ExamRegistrationForm