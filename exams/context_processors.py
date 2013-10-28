# -*- coding: utf-8 -*-

from exams.models import Examination

def current_examination(request):
    current = Examination.objects.get_active()

    if len(current) > 0:
        current = current[0]
    else:
        current = None

    return {
        'current_examination': current,
    }