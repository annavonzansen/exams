# -*- coding: utf-8 -*-

from exams.models import Examination

def current_examination(request):
    try:
        current = Examination.objects.get_latest()
    except Examination.DoesNotExist:
        current = None

    return {
        'current_examination': current,
    }