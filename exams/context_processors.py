# -*- coding: utf-8 -*-
import datetime
from django.utils.timezone import utc

from exams.models import Examination

def current_examination(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    current = Examination.objects.filter(registration_begin__lte=now, registration_end__gte=now).order_by('-registration_end')

    if len(current) > 0:
        current = current[0]
    else:
        return None

    return {
        'current_examination': current,
    }