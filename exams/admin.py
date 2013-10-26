# -*- coding: utf-8 -*-
from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin

from exams.models import Examination, Test, Assignment, AnswerOption, Answer, File, Subject, Order, OrderItem, ExamRegistration, Candidate, SpecialArrangement

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]

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

class ExaminationAdmin(MarkdownModelAdmin):
    list_display = ('__str__', 'registration_begin', 'registration_end', 'registration_status',)
    inlines = [
        TestInline,
    ]

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'subject_type', 'material_writing', 'material_listening',)



class ExamRegistrationInline(admin.TabularInline):
    model = ExamRegistration

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('identity_number', 'gender', 'candidate_type', 'get_examination', 'get_exams_names', 'get_school_id', 'get_last_updated',)
    list_filter = ('examination',)

    inlines = [
        ExamRegistrationInline,
    ]

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