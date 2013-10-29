# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import ugettext as _

from exams.models import Examination, Test, Assignment, File, Order, Candidate, CandidateUpload, ExamRegistration
#from exams.forms import CandidateFormset
from exams.forms import OrderForm, CandidateForm, OrderFormset, ExamRegistrationFormset, CandidateUploadForm
from django.http import HttpResponseRedirect


from exams.context_processors import current_examination

from education.models import School
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin
from extra_views.generic import GenericInlineFormSet

class DownloadView(View):
    '''
    Generic class view to abstract out the task of serving up files from within Django.
    Recommended usage is to combine it with SingleObjectMixin and extend certain methods based on your particular use case.
    
    Example usage::
    
        class Snippet(models.Model):
            name = models.CharField(max_length = 100)
            slug = SlugField()
            code = models.TextField()
        
        from django.views.generic.detail import SingleObjectMixin
    
        class DownloadSnippetView(SingleObjectMixin, DownloadView):
            model = Snippet
            use_xsendfile = False
            mimetype = 'application/python'
        
           def get_contents(self):
                return self.get_object().code
        
            def get_filename(self):
                return self.get_object().slug + '.py'
    '''
    
    mimetype = None
    extension = None
    filename = None
    use_xsendfile = True
    
    def get_filename(self):
        return self.filename
    
    def get_extension(self):
        return self.extension
    
    def get_mimetype(self):
        return self.mimetype
    
    def get_location(self):
        ''' Returns the path the file is currently located at. Used only if use_xsendfile is True '''
        pass
    
    def get_contents(self):
        ''' Returns the contents of the file download.  Used only if use_xsendfile is False '''
        pass
    
    def get(self, request, *args, **kwargs):
        response = HttpResponse(mimetype=self.get_mimetype())
        response['Content-Disposition'] = 'filename=' + self.get_filename()
        
        if self.use_xsendfile is True:
            response['X-Sendfile'] = self.get_location()
        else:
            response.write(self.get_contents())

        return response

class ExaminationsView(ListView):
    model = Examination
examinations = ExaminationsView.as_view()

class ExaminationView(DetailView):
    model = Examination
examination = ExaminationView.as_view()

class TestView(DetailView):
    model = Test

    def get_object(self):
        return get_object_or_404(Test, uuid=self.request.resolver_match.kwargs['uuid'])
test = TestView.as_view()

class TestsView(ListView):
    model = Test
tests = TestsView.as_view()

class AssignmentView(DetailView):
    model = Assignment

    def get_object(self):
        return get_object_or_404(Assignment, uuid=self.request.resolver_match.kwargs['uuid'])
assignment = AssignmentView.as_view()

class AssignmentsView(ListView):
    model = Assignment
assignments = AssignmentsView.as_view()

class FileDownloadView(SingleObjectMixin, DownloadView):
    model = File
    use_xsendfile = False
    mimetype = 'application/octet-stream'

    def get_object(self):
        return get_object_or_404(File, uuid=self.request.resolver_match.kwargs['uuid'])

    def get_contents(self):
        return self.get_object().file.read()

    def get_filename(self):
        obj = self.get_object()
        return "dl_%(uuid)s_%(filename)s" % {
            'uuid': obj.uuid,
            'filename': obj.file.path,
        }
download = FileDownloadView.as_view()



class OrdersView(ListView):
    model = Order
orders = OrdersView.as_view()

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        if self.request.POST:
            context['order_form'] = OrderFormset(self.request.POST)
        else:
            context['order_form'] = OrderFormset()
        return context    

    def get_initial(self):
        initial = super(OrderCreateView, self).get_initial()
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        initial['examination'] = current_examination(request=self.request)['current_examination']
        initial['created_by'] = self.request.user
        return initial

    def is_valid(self, form):
        form.cleaned_data['created_by'] = self.request.user

        return super(OrderCreateView, self).is_valid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        order_form = context['order_form']
        if order_form.is_valid():
            self.object = form.save()
            order_form.instance = self.object
            order_form.save()
            return super(OrderCreateView, self).form_valid(form)
        else:
            return super(OrderCreateView, self).form_valid(form)

    # TODO: Verify, that user is allowed to modify orders for this school
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderCreateView, self).dispatch(*args, **kwargs)
ordercreate = OrderCreateView.as_view()

class OrderEditView(UpdateView):
    model = Order
    form_class = OrderForm
    def get_context_data(self, **kwargs):
        context = super(OrderEditView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        if self.request.POST:
            context['order_form'] = OrderFormset(self.request.POST, instance=self.get_object())
        else:
            context['order_form'] = OrderFormset()
        return context    

    # def get_initial(self):
    #     initial = super(OrderEditView, self).get_initial()
    #     school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
    #     initial['examination'] = current_examination(request=self.request)['current_examination']
    #     initial['created_by'] = self.request.user
    #     return initial

    def form_valid(self, form):
        context = self.get_context_data()
        order_form = context['order_form']
        if order_form.is_valid():
            self.object = form.save()
            order_form.instance = self.object
            order_form.save()
            return super(OrderEditView, self).form_valid(form)
        else:
            return super(OrderEditView, self).form_valid(form)

    def is_valid(self, form):
        form.cleaned_data['created_by'] = self.request.user

        return super(OrderEditView, self).is_valid(form)

    # TODO: Verify, that user is allowed to modify orders for this school
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        order = Order.objects.get(uuid=self.request.resolver_match.kwargs['order_uuid'])
        return order
orderedit = OrderEditView.as_view()

class CandidatesView(ListView):
    model = Candidate

    def get_queryset(self):
        examination = current_examination(self.request)['current_examination']
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        candidates = Candidate.objects.filter(school=school, examination=examination)
        return candidates

    def get_context_data(self, **kwargs):
        context = super(CandidatesView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        return context

    # TODO: Require management rights
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CandidatesView, self).dispatch(*args, **kwargs)
candidates = CandidatesView.as_view()

class CandidateView(DetailView):
    model = Candidate

    def get_object(self):
        candidate = Candidate.objects.get(uuid=self.request.resolver_match.kwargs['candidate_uuid'])
        return candidate        

    def get_context_data(self, **kwargs):
        context = super(CandidateView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        return context

    # TODO: Require management rights
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CandidateView, self).dispatch(*args, **kwargs)
candidate = CandidateView.as_view()



class ExamRegistrationInline(InlineFormSet):
    model = ExamRegistration

class CandidateCreateView(CreateWithInlinesView):
    model = Candidate
    inlines = [ExamRegistrationInline]
    fields = ['last_name', 'first_names', 'identity_number', 'candidate_number', 'candidate_type', 'retrying', 'site',]
    #inlines_names = ['exam_form']
    #form_class = CandidateForm

    def get_context_data(self, **kwargs):
        context = super(CandidateCreateView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        return context

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        form.instance.school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        form.instance.examination = Examination.objects.get_latest()
        self.object = form.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    # TODO: Require management rights
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CandidateCreateView, self).dispatch(*args, **kwargs)
candidatecreate = CandidateCreateView.as_view()

class CandidateEditView(UpdateWithInlinesView):
    model = Candidate
    inlines = [ExamRegistrationInline]
    fields = ['last_name', 'first_names', 'identity_number', 'candidate_number', 'candidate_type', 'retrying', 'site',]

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        form.instance.school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        form.instance.examination = Examination.objects.get_latest()
        self.object = form.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CandidateEditView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        return context        
    
    def get_object(self):
        candidate = Candidate.objects.get(uuid=self.request.resolver_match.kwargs['candidate_uuid'])
        return candidate

    # TODO: Require management rights
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CandidateEditView, self).dispatch(*args, **kwargs)
candidateedit = CandidateEditView.as_view()        

orders = OrdersView.as_view()

ordercreate = OrderCreateView.as_view()
orderedit = OrderEditView.as_view()

class CandidateUploadView(CreateView):
    model = CandidateUpload
    form_class = CandidateUploadForm
    fields = ['file',]

    def get_context_data(self, **kwargs):
        context = super(CandidateUploadView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        return context   

    def get_initial(self):
        from exams.context_processors import current_examination
        initial = super(CandidateUploadView, self).get_initial()
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        #initial['id_school'] = school.pk
        initial['school'] = school
        initial['examination'] = current_examination(self.request)['current_examination']
        initial['by_user'] = self.request.user
        return initial

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     formset = ExamRegistrationFormset(self.request.POST)
        
    #     if (form.is_valid() and formset.is_valid()):
    #         return self.form_valid(form, formset)
    #     else:
    #         return self.form_invalid(form, formset)
    
    # TODO: Show feedback/message, based on importer results
    def form_valid(self, form):
        form.instance.by_user = self.request.user
        form.instance.school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        form.instance.examination = current_examination(self.request)['current_examination']
        return super(CandidateUploadView, self).form_valid(form)

    # TODO: Require management rights
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CandidateUploadView, self).dispatch(*args, **kwargs)
candidateupload = CandidateUploadView.as_view()