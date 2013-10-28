# -*- coding: utf-8 -*-

from exams.models import Examination

def current_examination(request):
    current = Examination.objects.get_latest()

    return {
        'current_examination': current,
    }