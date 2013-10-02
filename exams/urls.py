# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('exams.views',
    url(r'^$', 'examinations', name='examinations'),
    #url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', 'examination', name='examination'),
    
    url(r'^(?P<slug>[A-Za-z0-9-_]{1,})/$', 'examination', name='examination'),

    url(r'^(?P<examination_slug>[A-Za-z0-9-_]{1,})/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', 'test', name='test'),
    url(r'^(?P<examination_slug>[A-Za-z0-9-_]{1,})/(?P<test_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', 'assignment', name='assignment'),

    url(r'^file/(?P<uuid>\w+)/$', 'download', name='download'),
)
