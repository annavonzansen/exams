# -*- coding: utf-8 -*-

from django import template
from exams.models import Order, Subject, SubjectGroup, MaterialType

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
    else:
        return None

@register.simple_tag
def order_sg_total(order, subject_group, material_type):
    if isinstance(order, Order) and isinstance(subject_group, SubjectGroup) and isinstance(material_type, MaterialType):
        return order.get_subjectgroup_material_total(subject_group=subject_group, material_type=material_type)
    else:
        return None
