# -*- coding: utf-8 -*-
import datetime
from django.utils.timezone import utc
from django.db.models import Q

from exams.models import Examination

def current_examination(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    current = Examination.objects.filter(Q(registration_begin__lte=now, registration_end__gte=now) | Q(registration_status='E')).order_by('-registration_end')

    if len(current) > 0:
        current = current[0]
    else:
        current = None

    return {
        'current_examination': current,
    }