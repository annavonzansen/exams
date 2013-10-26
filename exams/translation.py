# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from exams.models import Subject

class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)
#translator.register(Subject, SubjectTranslationOptions)