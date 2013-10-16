# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

from django_extensions.db.fields import AutoSlugField, CreationDateTimeField, ModificationDateTimeField, UUIDField

from django.utils import timezone

import os
import re

CONTENT_TYPE_CHOICES = (
    ('M', _('Markdown')),
    ('H', _('HTML')),
    ('P', _('Plaintext')),
)

CONTENT_STATUS_FINAL = 'F'
CONTENT_STATUS_DRAFT = 'D'
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_DRAFT, _('Draft')),
    (CONTENT_STATUS_FINAL, _('Final')),
)

ASSIGNMENT_TYPE_SELECT_ONE = 's'
ASSIGNMENT_TYPE_CHOICES = (
    ('t', _('Text field')),
    ('T', _('Textarea')),
    ('S', _('Select multiple')),
    (ASSIGNMENT_TYPE_SELECT_ONE, _('Select one')),
)
ASSIGNMENT_SELECT_SEPARATOR = '|'

LANGUAGE_TEST_LEVELS = (
    ('A', _('Long')),
    ('B', _('Semi')),
    ('C', _('Short')),
    ('L7', _('Latin, 7th grade')),
    ('L1', _('Latin, high school')),
)

REGISTRATION_STATUS_CHOICES = (
    ('E', _('Enabled')),
    ('D', _('Disabled')),
)

def get_unique_filename(instance, filename):
    new_filename = 'uploads/%(date)s/%(uuid)s/%(filename)s' % {
        'filename': filename,
        'uuid': instance.uuid,
        'date': timezone.now().strftime('%Y%m%d%H%M%S'),
    }
    return new_filename

class Subject(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    short = models.CharField(max_length=3, unique=True, verbose_name=_('Short'))

    #subject_type = models.CharField(max_length=1, choices=SUBJECT_TYPE_CHOICES, verbose_name=_('Subject Type'))

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    def __str__(self):
        return "%(name)s (%(short)s)" % {
            'name': self.name,
            'short': self.short,
        }

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

class Examination(models.Model):
    """Examination

    Examination round (YOS2013)
    """
    uuid = UUIDField(verbose_name='UUID')
    title = models.CharField(max_length=255, unique=True, verbose_name=_('Title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    slug = AutoSlugField(populate_from=['title',])

    registration_begin = models.DateTimeField(blank=True, null=True)
    registration_end = models.DateTimeField(blank=True, null=True)
    registration_status = models.CharField(max_length=1, choices=REGISTRATION_STATUS_CHOICES, default='D')

    def get_tests(self):
        return Test.objects.filter(exam=self)

    @property
    def begin(self):
        tests = self.get_tests()
        smallest = None

        for t in tests:
            if smallest is None or t.begin < smallest:
                smallest = t.begin
        return smallest

    @property
    def end(self):
        tests = self.get_tests()
        largest = None

        for t in tests:
            if largest is None or t.end > largest:
                largest = t.end
        return largest

    def is_now(self):
        if self.begin < timezone.now() and self.end > timezone.now():
            return True
        return False

    def __unicode__(self):
        return _('Examination %s') % (self.title)
    
    class Meta:
        verbose_name = _('Examination')
        verbose_name_plural = _('Examinations')

class Test(models.Model):
    """Test

    Single test (math, physics, chemistry, languages, ...)
    """
    uuid = UUIDField(verbose_name='UUID')
    examination = models.ForeignKey(Examination)
    subject = models.ForeignKey('education.Subject', verbose_name=_('Subject'))

    level = models.CharField(max_length=2, choices=LANGUAGE_TEST_LEVELS, blank=True, null=True, verbose_name=_('Level'))

    #title = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from=['title',])

    assignments = models.ManyToManyField('Assignment', blank=True, null=True, verbose_name=_('Assignments'))

    begin = models.DateTimeField(verbose_name=_('Begin'))
    end = models.DateTimeField(verbose_name=_('End'))

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def is_now(self):
        if self.begin < timezone.now() and self.end > timezone.now():
            return True
        return False

    @property
    def assignment_count(self):
        return self.assignments.count()

    def __unicode__(self):
        return 'Test %(subject)s (%(level)s) / %(examination)s, %(assignment_count)d assignments' % {
            'subject': self.subject,
            'level': self.level,
            'assignment_count': self.assignment_count,
            'examination': self.examination.title,
        }

    class Meta:
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')

class AnswerOption(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    key = models.CharField(max_length=255)
    value = models.TextField(max_length=255)

    def __unicode__(self):
        return _('AnswerOption %(key)s: %(value)s (%(uuid)s)') % {
            'key': self.key,
            'value': self.value,
            'uuid': uuid,
        }

    class Meta:
        verbose_name = _('Answer Option')
        verbose_name_plural = _('Answer Options')

class Assignment(models.Model):
    """Assignment"""
    uuid = UUIDField(verbose_name='UUID')

    title = models.CharField(max_length=255)

    assignment_type = models.CharField(max_length=3, choices=ASSIGNMENT_TYPE_CHOICES)
    instructions = models.TextField(blank=True, null=True)

    content = models.TextField()
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPE_CHOICES)
    slug = AutoSlugField(populate_from=['title',])

    attached_files = models.ManyToManyField('File', blank=True, null=True)

    answer_options = models.ForeignKey(AnswerOption, blank=True, null=True)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def attached_files_count(self):
        return self.attached_files.count()

    def format_assignment_select(self):
        def expand_choices(matchobj):
            opts = matchobj.group(1).split(ASSIGNMENT_SELECT_SEPARATOR)
            num = opts[0].split(' ')[0]
            opts[0] = ' '.join(opts[0].split(' ')[1:])
            code = '<select name="assignment-%(uuid)s-%(num)s"><option>%(select)s</option>' % {
                'select': _("-- Select --"),
                'uuid': '%%UUID%%',
                'num': num,
                } + ''.join(['<option>%s</option>' % x.strip() for x in opts]) + '</select>'
            return code
        regexp = r'\[(.*?)\]'
        assignment = re.sub(regexp, expand_choices, self.content)
        return assignment

    def format_assignment(self):
        if self.assignment_type == ASSIGNMENT_TYPE_SELECT_ONE:
            return self.format_assignment_select()
        else:
            return self.content

    def get_settings(self):
        # TODO: Get settings: default, global, group, user
        pass

    def __unicode__(self):
        return _('Assignment %(title)s (%(uuid)s)') % {
            'title': self.title,
            'uuid': self.uuid,
        }
    
    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

class Answer(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    test = models.ForeignKey(Test)
    assignment = models.ForeignKey(Assignment)
    content = models.TextField()

    status = models.CharField(max_length=1, choices=CONTENT_STATUS_CHOICES)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return 'Answer %s to assignment %s by %s' % (self.uuid, self.assignment.title, self.user)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

class File(models.Model):
    uuid = UUIDField()

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title'))
    file = models.FileField(upload_to=get_unique_filename, verbose_name=_('File'))


    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return _('File: %(title)s, %(filename)s (%(size)d bytes) (%(uuid)s)') % {
                    'title': self.title,
                    'filename': os.path.basename(self.file.path),
                    'uuid': self.uuid,
                    'size': self.file.size,
                 }

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')