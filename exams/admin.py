# -*- coding: utf-8 -*-
from django.contrib import admin

from exams.models import Examination, Test, Assignment, AnswerOption, Answer, File
from django_markdown.admin import MarkdownModelAdmin

class AssignmentInline(admin.TabularInline):
    model = Assignment

class TestInline(admin.TabularInline):
    model = Test

class TestAdmin(admin.ModelAdmin):
    inlines = [
        #AssignmentInline,
    ]

class ExaminationAdmin(MarkdownModelAdmin):
    inlines = [
        TestInline,
    ]

admin.site.register(Examination)
admin.site.register(Test, TestAdmin)
admin.site.register(Assignment)
admin.site.register(AnswerOption)
admin.site.register(Answer)
admin.site.register(File)