# -*- coding: utf-8 -*-
from django.contrib import admin

from exams.models import Examination, Test, Assignment, AnswerOption, Answer, File, Subject
from django_markdown.admin import MarkdownModelAdmin

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
    list_display = ('title', 'registration_begin', 'registration_end', 'registration_status',)
    inlines = [
        TestInline,
    ]

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'subject_type', 'material_writing', 'material_listening',)

admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Test, TestAdmin)
#admin.site.register(Assignment)
admin.site.register(AnswerOption)
admin.site.register(Answer)
admin.site.register(File)
admin.site.register(Subject, SubjectAdmin)
