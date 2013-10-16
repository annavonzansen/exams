# -*- coding: utf-8 -*-

from exams.models import Examination

def current_examination(request):
    return {
        'current_examination': 'xx',
    }
    #current_examination = Examination.objects.filter()