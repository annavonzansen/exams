# -*- coding: utf-8 -*-
from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from django.utils.translation import ugettext as _

from exams.models import Examination, Test, Assignment, AnswerOption, Answer, File, Subject, Order, OrderItem, ExamRegistration, Candidate, SpecialArrangement, CandidateUpload, MaterialType

import csv
from django.http import HttpResponse
from simple_history.admin import SimpleHistoryAdmin

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(SimpleHistoryAdmin):
    list_display = ('uuid', 'site', 'examination', 'get_order_text', 'date', 'status', 'created_by')
    list_filter = ('examination', 'status',)
    inlines = [
        OrderItemInline,
    ]
    actions = [export_as_csv_action('CSV Export',)]

admin.site.register(Order, OrderAdmin)

class AssignmentInline(admin.TabularInline):
    model = Assignment

class TestInline(admin.TabularInline):
    model = Test

class TestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'examination', 'begin', 'end', 'assignment_count',)
    inlines = [
        AssignmentInline,
    ]

class ExaminationAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'registration_begin', 'registration_end', 'registration_status',)
    inlines = [
        TestInline,
    ]

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'subject_type', 'get_material_types',)

class ExamRegistrationInline(admin.TabularInline):
    model = ExamRegistration

# class SpecialArrangementFilter(admin.SimpleListFilter):
#     title = _('Special Arrangement')
#     parameter_name = 'special_arrangement'

#     def lookups(self, request, model_admin):
#         sas = SpecialArrangement.objects.all()

#         opts = []
#         for special in sas:
#             opts.append((special.short, special.title))
#         return opts

#     def queryset(self, request, queryset):
#         sas = SpecialArrangement.objects.get(short=self.value())
#         regs = ExamRegistration.objects.filter(special_arrangement=sas)
#         objs = queryset.filter()

# TODO: Allow filtering by school, show as dropdown <https://docs.djangoproject.com/en/1.4/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter>
#class FilterWithCustomTemplate(SimpleListFilter):
#    template = "custom_template.html"

class CandidateAdmin(SimpleHistoryAdmin):
    list_display = ('identity_number', 'gender', 'candidate_type', 'get_examination', 'get_exams_names', 'get_school_id', 'get_last_updated',)
    list_filter = ('examination', 'gender', 'candidate_type', 'school',)

    ordering = ('examination', 'school', 'candidate_number',)
    search_fields = ('identity_number', 'candidate_number',)

    actions = [export_as_csv_action('CSV Export',)]

    inlines = [
        ExamRegistrationInline,
    ]

    # def changelist_view(self, request, extra_context=None):
    #     if not request.GET.has_key('examination__id__exact'):
    #         q = request.GET.copy()
    #         q['examination__id__exact'] = Examination.objects.get_active().pk
    #         request.GET = q
    #         request.META['QUERY_STRING'] = request.GET.urlencode()
    #     return super(CandidateAdmin, self).changelist_view(request, extra_context=extra_context)

class SpecialArrangementAdmin(admin.ModelAdmin):
    list_display = ('title', 'short',)

admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Test, TestAdmin)
#admin.site.register(Assignment)
admin.site.register(AnswerOption)
admin.site.register(Answer)
admin.site.register(File)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(SpecialArrangement, SpecialArrangementAdmin)
#admin.site.register(CandidateUpload)
admin.site.register(MaterialType)