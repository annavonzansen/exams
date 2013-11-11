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

from exams.models import Examination, Test, Assignment, File, Order, Candidate, CandidateUpload, ExamRegistration, OrderItem, MaterialType, ORDER_STATUS_INITIALIZED, ORDER_STATUS_CREATED, ORDER_STATUS_UPDATED
#from exams.forms import CandidateFormset
from exams.forms import OrderForm, CandidateForm, OrderFormset, ExamRegistrationFormset, CandidateUploadForm, ExamRegistrationForm, ExamRegistrationHelper, OrderItemHelper
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from exams.context_processors import current_examination

from education.models import School, SchoolSite
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

class OrderView(DetailView):
    model = Order

    def get_object(self):
        order = Order.objects.get(uuid=self.request.resolver_match.kwargs['order_uuid'])
        return order        

    def get_context_data(self, **kwargs):
        from exams.models import Subject
        context = super(OrderView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        subjects = Subject.objects.all()
        materials = MaterialType.objects.all()
        context['school'] = school
        context['materials'] = materials
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(OrderView, self).dispatch(*args, **kwargs)     
order = OrderView.as_view()

class OrdersView(ListView):
    model = Order
    def get_context_data(self, **kwargs):
        from exams.models import Subject
        context = super(OrdersView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        subjects = Subject.objects.all()
        materials = MaterialType.objects.all()

        current = []
        sites = school.get_sites()
        for s in sites:
            try:
                current.append(s.get_latest_order())
            except Order.DoesNotExist:
                pass

        context['school'] = school
        context['materials'] = materials
        context['current_orders'] = current
        return context

    def get_queryset(self):
        from education.models import SchoolSite
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        sites = SchoolSite.objects.filter(school=school)
        examination = Examination.objects.get_latest()
        orders = Order.objects.filter(site__in=sites, examination=examination)
        return orders

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(OrdersView, self).dispatch(*args, **kwargs)
orders = OrdersView.as_view()

class OrderItemInline(InlineFormSet):
    model = OrderItem
    extra = 0

class OrderCreateView(UpdateWithInlinesView):
    model = Order
    inlines = [OrderItemInline]
    form_class = OrderForm
    fields = ['site', 'email', 'additional_details',]
    extra = 0

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        context['form'].fields['site'].queryset = SchoolSite.objects.filter(school=school)
        context['helper'] = OrderItemHelper()
        return context

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        
        form.instance.examination = Examination.objects.get_latest()
        form.instance.created_by = self.request.user

        self.object = form.save()

        for formset in inlines:
            formset.save()
        messages.info(self.request, _('Order created successfully!'))
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        examination = current_examination(self.request)['current_examination']
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        site = school.get_default_site()
        new = Order(created_by=self.request.user, examination=examination, status=ORDER_STATUS_INITIALIZED, site=site)
        new.save()
        new.append_missing_subjects()
        return new

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(OrderCreateView, self).dispatch(*args, **kwargs)
ordercreate = OrderCreateView.as_view()

class OrderEditView(UpdateWithInlinesView):
    model = Order
    inlines = [OrderItemInline]
    form_class = OrderForm
    fields = ['site', 'email', 'additional_details',]

    def get_context_data(self, **kwargs):
        context = super(OrderEditView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        context['form'].fields['site'].queryset = SchoolSite.objects.filter(school=school)
        context['helper'] = OrderItemHelper()
        return context    

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        
        form.instance.examination = Examination.objects.get_latest()
        form.instance.created_by = self.request.user
        #form.instance.status = 'c'

        self.object = form.save()
        for formset in inlines:
            formset.save()

        # TODO: Send e-mail confirmation
        messages.info(self.request, _('Order updated successfully!'))
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        old = Order.objects.get(uuid=self.request.resolver_match.kwargs['order_uuid'])
        if old.status == ORDER_STATUS_INITIALIZED:
            old.status = ORDER_STATUS_CREATED
            if old.parent:
                old.parent.status = ORDER_STATUS_UPDATED
                old.parent.save()
            return old
        new = old.clone()
        return new
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(UpdateWithInlinesView, self).dispatch(*args, **kwargs)
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(CandidateView, self).dispatch(*args, **kwargs)
candidate = CandidateView.as_view()



class ExamRegistrationInline(InlineFormSet):
    model = ExamRegistration
    form_class = ExamRegistrationForm
    extra = 0

# TODO: Convert to UpdateWithInlinesView
class CandidateCreateView(CreateWithInlinesView):
    model = Candidate
    inlines = [ExamRegistrationInline]
    fields = ['last_name', 'first_names', 'candidate_number', 'site',]
    form_class = CandidateForm
    extra = 0

    def get_initial(self):
        initial = super(CandidateCreateView, self).get_initial()
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        site = SchoolSite.objects.filter(school=school)
        if len(site) > 0:
            initial['site'] = site[0]
        return initial

    def get_context_data(self, **kwargs):
        context = super(CandidateCreateView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        context['form'].fields['site'].queryset = SchoolSite.objects.filter(school=school)
        context['helper'] = ExamRegistrationHelper()
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
        messages.success(self.request, _('Candidate added!'))
        return HttpResponseRedirect(self.get_success_url())

    # TODO: Create new candidate, create registration template
    # def get_object(self):
    #     examination = current_examination(self.request)['current_examination']
    #     school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
    #     candidate = Candidate(examination=examination, school=school)
    #     candidate.save()
    #     candidate.append_missing_registrations()
    #     #candidate = Candidate.objects.get(uuid=self.request.resolver_match.kwargs['candidate_uuid'])
    #     return candidate

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(CandidateCreateView, self).dispatch(*args, **kwargs)
candidatecreate = CandidateCreateView.as_view()

class CandidateEditView(UpdateWithInlinesView):
    model = Candidate
    inlines = [ExamRegistrationInline]
    fields = ['last_name', 'first_names', 'identity_number', 'candidate_number', 'candidate_type', 'retrying', 'site',]
    form_class = CandidateForm

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        form.instance.school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        form.instance.examination = Examination.objects.get_latest()
        self.object = form.save()
        for formset in inlines:
            formset.save()
        messages.success(self.request, _('Candidate updated!'))
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CandidateEditView, self).get_context_data(**kwargs)
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        context['school'] = school
        context['form'].fields['site'].queryset = SchoolSite.objects.filter(school=school)
        context['helper'] = ExamRegistrationHelper()
        return context        
    
    def get_object(self):
        candidate = Candidate.objects.get(uuid=self.request.resolver_match.kwargs['candidate_uuid'])
        return candidate

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(CandidateEditView, self).dispatch(*args, **kwargs)
candidateedit = CandidateEditView.as_view()        



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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        school = School.objects.get(uuid=self.request.resolver_match.kwargs['uuid'])
        if not school.is_manager(self.request.user):
            raise PermissionDenied
        return super(CandidateUploadView, self).dispatch(*args, **kwargs)
candidateupload = CandidateUploadView.as_view()