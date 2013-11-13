# -*- coding: utf-8 -*-

from django import template
from exams.models import Order, Subject, SubjectGroup, MaterialType, SpecialArrangement, ExamRegistration

register = template.Library()

# @register.filter(name='is_manager')
# def is_manager(value, arg):
#     """Returns True if user is manager for school"""
#     print value
#     print arg
#     if arg in value.managers:
#         return True
#     return False

# @register.filter(name='count')
# def count(value):
#     return len(value)

@register.simple_tag
def order_subject_count(order, subject, material_type):
    if isinstance(order, Order) and isinstance(subject, Subject) and isinstance(material_type, MaterialType):
        return order.get_subject_material_amount(subject=subject, material_type=material_type)
    return None

@register.simple_tag
def order_sg_total(order, subject_group, material_type):
    if isinstance(order, Order) and isinstance(subject_group, SubjectGroup) and isinstance(material_type, MaterialType):
        return order.get_subjectgroup_material_total(subject_group=subject_group, material_type=material_type)
    return None

@register.simple_tag
def order_mt_total(order, material_type):
    if isinstance(order, Order) and isinstance(material_type, MaterialType):
        return order.get_materialtype_total(material_type=material_type)
    return None

@register.filter
def sg_has_material(subject_group, material_type):
    if isinstance(subject_group, SubjectGroup) and isinstance(material_type, MaterialType):
        return subject_group.has_material(material_type)
    return False

@register.filter
def subject_has_material(subject, material_type):
    if isinstance(subject, Subject) and isinstance(material_type, MaterialType):
        return subject.has_material(material_type)
    return False

@register.simple_tag
def order_field_for(order, subject, material_type):

    return '<input type="number" size="4" name="%(name)s" value="%(value)d"/>'

@register.filter
def er_has_sa(er, sa):
    if isinstance(er, ExamRegistration) and isinstance(sa, SpecialArrangement):
        if sa in er.special_arrangements.all():
            return True
    return False