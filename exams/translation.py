# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from exams.models import Subject, MaterialType, SubjectGroup, SpecialArrangement

class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(Subject, SubjectTranslationOptions)

class SubjectGroupTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(SubjectGroup, SubjectGroupTranslationOptions)

class MaterialTypeTranslationOptions(TranslationOptions):
    fields = ('title',)
translator.register(MaterialType, MaterialTypeTranslationOptions)

class SpecialArrangementTranslationOptions(TranslationOptions):
    fields = ('title',)
translator.register(SpecialArrangement, SpecialArrangementTranslationOptions)