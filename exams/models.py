# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

from django_extensions.db.fields import AutoSlugField, CreationDateTimeField, ModificationDateTimeField, UUIDField
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.timezone import utc
from django.core import serializers
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import PermissionDenied
import os
import re
import datetime
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from people.models import Person

EXAMINATION_SEASON_CHOICES = (
    ('K', _('Spring')),
    ('S', _('Autumn')),
)

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
ASSIGNMENT_TYPE_TEXTAREA = 'T'
ASSIGNMENT_TYPE_CHOICES = (
    ('t', _('Text field')),
    (ASSIGNMENT_TYPE_TEXTAREA, _('Textarea')),
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
    ('S', _('Scheduled')),
)

SUBJECT_TYPE_CHOICES = (
    ('R', _('Real')),
    ('L', _('Language')),
    ('M', _('Math')),
)

def get_unique_filename(instance, filename):
    new_filename = 'uploads/%(date)s/%(uuid)s/%(filename)s' % {
        'filename': filename,
        'uuid': instance.uuid,
        'date': timezone.now().strftime('%Y%m%d%H%M%S'),
    }
    return new_filename


class Subject(models.Model):
    """Test Subject"""
    uuid = UUIDField(verbose_name='UUID')
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    short = models.CharField(max_length=3, unique=True, verbose_name=_('Short'))

    subject_type = models.CharField(max_length=1, choices=SUBJECT_TYPE_CHOICES, verbose_name=_('Subject Type'))

    material_writing = models.BooleanField(default=True, verbose_name=_('Material for written exams'), help_text=_('Does this subject include written assignments'))
    material_listening = models.BooleanField(default=False, verbose_name=_('Material for listening exams'), help_text=_('Does this subject include listening assignments'))

    history = HistoricalRecords()


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

def year_choices(min=None, max=None):
    choices = []
    if not min:
        min = datetime.datetime.now().year - 2
    if not max:
        max = datetime.datetime.now().year + 2

    if min > max:
        tmin = min
        min = max
        max = tmin

    for r in range(min, max):
        choices.append((r, r))
    return choices

# TODO: Django 1.6 supports choices which are functions
YEAR_CHOICES = year_choices(min=2005, max=2020)

class ExaminationManager(models.Manager):
    def get_active(self):
        """Returns currently active examinations"""
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return super(ExaminationManager, self).get_queryset().filter(Q(registration_begin__lte=now, registration_end__gte=now, registration_status='S') | Q(registration_status='E'))

    def get_latest(self):
        """Returns latest examination ("current"), determined by which has latest registration_begin time and is currently active"""
        return self.get_active().latest('registration_begin')

class Examination(models.Model):
    """Examination

    Examination round (YOS2013)
    """
    uuid = UUIDField(verbose_name='UUID')

    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    season = models.CharField(max_length=1, choices=EXAMINATION_SEASON_CHOICES)

    slug = AutoSlugField(populate_from=['year', 'season',])

    # TODO: Allow only one active Examination registration
    registration_begin = models.DateTimeField(blank=True, null=True, verbose_name=_('Registration Begin'), help_text=_('Date + time when registration begins, ie. when schools can register students and order materials'))
    registration_end = models.DateTimeField(blank=True, null=True, verbose_name=_('Registration End'), help_text=_('Date + time when registration begins, ie. when schools can no longer register students and order materials'))
    registration_status = models.CharField(max_length=1, choices=REGISTRATION_STATUS_CHOICES, default='D', verbose_name=_('Registration Status'), help_text=_('Current registration mode. Enabled = schools can register students and order material, disabled = schools can not register students, scheduled = depends on registration begin/end times.'))
    
    history = HistoricalRecords()
    objects = ExaminationManager()
    
    def get_absolute_url(self):
        return reverse('exams:examination', kwargs={
            'slug': self.slug,
        })

    def get_tests(self):
        return Test.objects.filter(examination=self)

    def is_registration_enabled(self):
        # TODO: Deprecated
        if self.registration_status == 'E':
            return True
        elif self.registration_status == 'S':
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            if self.registration_begin <= now and self.registration_end >= now:
                return True
        return False

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

    def __str__(self):
        return "%d%s" % (self.year, self.season)

    def __unicode__(self):
        return self.__str__()
    
    class Meta:
        verbose_name = _('Examination')
        verbose_name_plural = _('Examinations')
        unique_together = (('year', 'season',))

class Test(models.Model):
    """Test

    Single test (math, physics, chemistry, languages, ...)
    """
    uuid = UUIDField(verbose_name='UUID')
    examination = models.ForeignKey(Examination)
    subject = models.ForeignKey('exams.Subject', verbose_name=_('Subject'))

    #level = models.CharField(max_length=2, choices=LANGUAGE_TEST_LEVELS, blank=True, null=True, verbose_name=_('Level'))

    #title = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from=['title',])

    begin = models.DateTimeField(verbose_name=_('Begin'))
    end = models.DateTimeField(verbose_name=_('End'))
    history = HistoricalRecords()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def title(self):
        return "%(subject)s %(level)s" % {
            'subject': self.subject.name.capitalize(),
            'level': self.level or "",
        }
    title.short_description = _('Title')
    title.admin_order_field = 'subject'

    def get_absolute_url(self):
        return reverse('exams:test', kwargs={
            'examination_slug': self.examination.slug,
            'uuid': self.uuid,
        })

    def is_now(self):
        if self.begin < timezone.now() and self.end > timezone.now():
            return True
        return False

    def get_assignments(self):
        assignments = Assignment.objects.filter(test=self, status=CONTENT_STATUS_FINAL)
        return assignments

    @property
    def assignment_count(self):
        return self.get_assignments().count()

    def __unicode__(self):
        return 'Test %(subject)s / %(examination)s, %(assignment_count)d assignments' % {
            'subject': self.subject,
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
    test = models.ForeignKey(Test)

    title = models.CharField(max_length=255)

    assignment_type = models.CharField(max_length=3, choices=ASSIGNMENT_TYPE_CHOICES)
    instructions = models.TextField(blank=True, null=True)

    content = models.TextField()
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPE_CHOICES)

    order = models.IntegerField(default=0)

    attached_files = models.ManyToManyField('File', blank=True, null=True)

    answer_options = models.ForeignKey(AnswerOption, blank=True, null=True)

    status = models.CharField(max_length=1, choices=CONTENT_STATUS_CHOICES)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def get_absolute_url(self):
        return reverse('exams:assignment', kwargs={
            'examination_slug': self.test.examination.slug,
            'test_uuid': self.test.uuid,
            'uuid': self.uuid,
        })

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

    def format_assignment_textarea(self):
        textarea_code = '[textarea]'
        return self.content.replace(textarea_code, '<textarea rows="5" cols="60"></textarea>')

    def format_assignment(self):
        if self.assignment_type == ASSIGNMENT_TYPE_SELECT_ONE:
            return self.format_assignment_select()
        elif self.assignment_type == ASSIGNMENT_TYPE_TEXTAREA:
            return self.format_assignment_textarea()
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
        ordering = ('order',)

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

    def get_absolute_url(self):
        return reverse('exams:download', kwargs={
            'uuid': self.uuid,
        })

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

class CandidateType(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    title = models.CharField(max_length=255, unique=True)
    code = models.IntegerField(unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return "%02d %s" % (self.code, self.title)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Candidate Type')
        verbose_name_plural = _('Candidate Types')


class Candidate(Person):
    #uuid = UUIDField(verbose_name='UUID')
    examination = models.ForeignKey('exams.Examination', verbose_name=_('Examination'))
    history = HistoricalRecords()

    #person = models.ForeignKey('people.Person', verbose_name=_('Person'))


    school = models.ForeignKey('education.School', verbose_name=_('School'))
    site = models.ForeignKey('education.SchoolSite', blank=True, null=True, verbose_name=_('Site'), help_text=_('Site in which this student will attend exams.'))

    candidate_number = models.PositiveIntegerField(verbose_name=_('Candidate Number'), help_text=_('School-specific identification number for candidate (incrementing)'))
    candidate_type = models.ForeignKey(CandidateType, verbose_name=_('Candidate Type'), help_text=_('What sort of candidate this person is?'))

    retrying = models.BooleanField(default=False, verbose_name=_('Candidate is retrying full exam'), help_text=_('Is candidate starting the examination from begin?'))

    # TODO: Validate identity number
    # TODO: Gender from identity number
    # TODO: Age
    #created = CreationDateTimeField()
    #modified = ModificationDateTimeField()

    def add_registration(self, subject):
        er = ExamRegistration.objects.get_or_create(candidate=self, subject=subject)
        return True

    def get_school_id(self):
        return _('%(candidate_number)s / %(school)s') % {
            'candidate_number': self.candidate_number,
            'school': self.school,
        }
    get_school_id.short_description = _('Candidate ID / School')
    get_school_id.admin_order_field = 'candidate_number'

    def get_examination(self):
        return "%s" % self.examination
    get_examination.short_description = _('Examination')
    get_examination.admin_order_field = 'examination'

    def _hide_identity(self):
        if self.identity_number:
            self.identity_number = self.identity_number[:7]
            self.save()
            return True
        return False

    def get_candidate(self):
        return _('%(last_name)s, %(first_names)s (%(identity_number)s)') % {
            'identity_number': self.identity_number,
            'name': self.name,
            'last_name': self.last_name,
            'first_names': self.first_names,
        }
    get_candidate.short_description = _('Candidate')
    get_candidate.admin_order_field = 'candidate_id'

    def get_exams(self):
        exams = ExamRegistration.objects.filter(candidate=self).order_by('subject')
        return exams
    get_exams.short_description = _('Exams')
    

    def get_last_updated(self):
        last_updated = self.modified
        exams = self.get_exams()
        for e in exams:
            if e.modified > last_updated:
                last_updated = e.modified
        return last_updated
    get_last_updated.short_description = _('Last Updated')

    def get_exams_names(self):
        exams = self.get_exams()
        out = []
        for e in exams:
            if e.special_arrangements.count() > 0:
                special_arrangements = "-".join(["<strong>%s</strong>" % x.short for x in e.special_arrangements.all()])
            else:
                special_arrangements = ''
            out.append("<strong>%s</strong> %s %s" % (e.subject.short, e.subject.name, special_arrangements))
        return "<br/>".join(out)
    get_exams_names.short_description = _('Exams')
    get_exams_names.allow_tags = True


    def __str__(self):
        parts = []
        if self.candidate_number:
            parts.append("%s %d," % (_('Candidate'), self.candidate_number))

        if self.gender:
            parts.append(self.get_gender_display().lower())

        if self.last_name:
            parts.append(self.last_name)
        if self.first_names:
            parts.append(self.first_names)
        elif self.first_name:
            parts.append(self.first_name)

        if self.identity_number:
            parts.append("(%s)" % self.identity_number[:7])
        elif self.birthday:
            parts.append("(%s)" % self.birthday)

        return " ".join(parts)


    def __unicode__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('education:school', kwargs={
            'uuid': self.school.uuid,
            #'candidate_uuid': self.uuid,
        })

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')

        unique_together = (('examination', 'school', 'candidate_number',),)

class CandidateUpload(models.Model):
    UPLOADED_FILE_CHOICES = (
        ('U', _('Uploaded')),
        ('P', _('Processed')),
        ('A', _('Archived')),
        ('R', _('Removed')),
        ('I', _('Invalid')),
        ('p', _('Permissions failed')),
    )
    uuid = UUIDField(verbose_name=_('UUID'))
    examination = models.ForeignKey(Examination)
    school = models.ForeignKey('education.School')

    file = models.FileField(upload_to='candidates/%Y%m%d%H%M%S/')

    by_user = models.ForeignKey(settings.AUTH_USER_MODEL)

    status = models.CharField(max_length=1, choices=UPLOADED_FILE_CHOICES, default='U')

    history = HistoricalRecords()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()


    def process_file(self):
        stats = {}
        if self.status == 'U':
            if self.by_user in self.school.managers.all():
                try:
                    stats = import_candidates(self.file.path, allowed_schools=[self.school,])
                    self.status = 'P'
                except PermissionDenied:
                    self.status = 'I'
                self.save()
                return stats
            else:
                self.status = 'p'
                self.save()
                return False
        else:
            return False

    def get_absolute_url(self):
        return reverse('education:candidates', kwargs={
            'uuid': self.school.uuid,
        })

    def __str__(self):
        return "%s, %s, %s, %s" % (self.examination, self.school, self.by_user, self.file.path)

def process_candidateupload(sender, instance, **kwargs):
    instance.process_file()
post_save.connect(process_candidateupload, sender=CandidateUpload, dispatch_uid='process_candidateupload')


class SpecialArrangement(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    title = models.CharField(max_length=255, unique=True, verbose_name=_('Title'))
    short = models.CharField(max_length=5, unique=True, verbose_name=_('Short'))
    history = HistoricalRecords()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __str__(self):
        return "%s (%s)" % (self.title, self.short)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Special Arrangement')
        verbose_name_plural = _('Special Arrangements')

class ExamRegistration(models.Model):
    """Exam registration, attaches candidate to specific exam"""
    uuid = UUIDField(verbose_name='UUID')

    
    subject = models.ForeignKey('exams.Subject', verbose_name=_('Subject'))
    candidate = models.ForeignKey(Candidate)

    special_arrangements = models.ManyToManyField(SpecialArrangement, blank=True, null=True, verbose_name=_('Special Arrangements'))
    additional_details = models.TextField(blank=True, null=True, verbose_name=_('Additional Details'))

    status = models.CharField(max_length=1, choices=REGISTRATION_STATUS_CHOICES, default='R')

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __str__(self):
        return "%(candidate)s > %(subject)s" % {
            'candidate': self.candidate,
            'subject': self.subject,
        }

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Exam Registration')
        verbose_name_plural = _('Exam Registrations')
        unique_together = (('subject', 'candidate',))


ORDER_STATUSES = (
    ('c', _('Order Created')),
    ('P', _('Packaged')),
    ('S', _('Order Shipped')),
)

class Order(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    site = models.ForeignKey('education.SchoolSite')
    history = HistoricalRecords()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'))

    examination = models.ForeignKey('exams.Examination')
    content = models.TextField(blank=True, null=True, editable=False) # order, as JSON. serialized objects [school, schoolsite, students, amounts, who created, ...]

    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Order Date'))
    status = models.CharField(max_length=2, choices=ORDER_STATUSES, default='c', verbose_name=_('Status'))

    additional_details = models.TextField(blank=True, null=True, verbose_name=_('Additional Details'))

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_('Parent Order'), help_text=_('Which order is an older version of this (parent)'))

    def get_order(self):
        items = OrderItem.objects.filter(order=self).order_by('subject')
        return items

    def get_order_json(self):
        items = self.get_order()
        data = serializers.serialize('json', items)
        return data

    def get_order_text(self):
        items = self.get_order()
        return ", ".join([x.__str__() for x in items])

    def get_absolute_url(self):
        return reverse('education:school', kwargs={
            'uuid': self.site.school.uuid,
            #'order_uuid': self.uuid,
        })

    def __str__(self):
        return "Order %(uuid)s, %(school)s %(date)s: %(order)s" % {
            'uuid': self.uuid,
            'school': self.site,
            'date': self.date,
            'order': self.get_order_text(),
        }

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class OrderItem(models.Model):
    uuid = UUIDField(verbose_name='UUID')
    order = models.ForeignKey(Order)
    history = HistoricalRecords()

    subject = models.ForeignKey('exams.Subject')
    amount = models.PositiveIntegerField()


    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __str__(self):
        return "%s:%d" % (self.subject.short, self.amount)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')



def import_candidates(filename, allowed_schools=None):
    # TODO: Django development version has update_or_create()
    stats = {
        'candidates_created': 0,
        'candidates_updated': 0,
        'examregistrations': 0,
        'messages': [],
    }
    _cache = {
        'examinations': {},
        'schools': {},
        'subjects': {},
        'candidate_types': {},
    }

    try:
        from exams.importers import parse_candidate_xml
        from education.models import School

        candidates = parse_candidate_xml(filename)

        for c in candidates:
            if _cache['examinations'].has_key(c.examination):
                examination = _cache['examinations'][c.examination]
            else:
                examination_year = c.examination[0:4]
                examination_season = c.examination[4:5]
            
                examination = Examination.objects.get(year=examination_year, season=examination_season)
                _cache['examinations'][c.examination] = examination

            if _cache['schools'].has_key(c.school):
                school = _cache['schools'][c.school]
            else:
                school = School.objects.get(school_id=c.school)
                _cache['schools'][c.school] = school

            if allowed_schools and school not in allowed_schools:
                raise PermissionDenied
            # TODO: Check that school is in allowed_schools (if defined, else raise PermissionDenied or something like that)

            if _cache['candidate_types'].has_key(c.ctype):
                ctype = _cache['candidate_types'][c.ctype]
            else:
                ctype = CandidateType.objects.get(code=c.ctype)
                _cache['candidate_types'][c.ctype] = ctype

            cand, created = Candidate.objects.get_or_create(candidate_number=c.id, examination=examination, school=school, candidate_type=ctype)
            cand.identity_number = c.identity_number

            cand.gender = c.gender
            cand.retrying = c.retrying

            cand.save()

            if created:
                stats['candidates_created'] += 1
            else:
                stats['candidates_updated'] += 1

            for s in c.subjects:
                if _cache['subjects'].has_key(s):
                    subj = _cache['subjects'][s]
                else:
                    subj = Subject.objects.get(short=s)
                    _cache['subjects'][s] = subj
                cand.add_registration(subj)
                stats['examregistrations'] += 1
    except Examination.DoesNotExist:
        stats['messages'].append(_("Cannot import candidate %(candidate)s, specified examination %(examination)s does not exist!") % {
                    'candidate': c,
                    'examination': c.examination,
                })
    except School.DoesNotExist:
        stats['messages'].append(_("Cannot import candidate %(candidate)s, specified school %(school)s does not exist!") % {
                    'candidate': c,
                    'school': c.school,
                })
    except CandidateType.DoesNotExist:
        stats['messages'].append(_("Cannot import candidate %(candidate)s, specified type %(type)s does not exist!") % {
                    'candidate': c,
                    'type': c.ctype,
                })
    except Subject.DoesNotExist:
        stats['messages'].append(_("Cannot import candidate %(candidate)s, specified subject %(subject)s does not exist!") % {
                    'candidate': c,
                    'subject': c.subjects,
                })      
      
    finally:
        return stats

def export_orders(filename):
    """Exports orders to XLS file"""
    examination = '2013S'
    subject = 'XX'

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('orders')
    sheet.write(0, 0, 'Ylioppilastutkintolautakunta')
    sheet.write(1, 0, _('Examination'))
    sheet.write(1, 1, examination)

    sheet.write(2, 0, _('Subject'))
    sheet.write(2, 1, subject)
    sheet.write(3, 0, _('Date'))
    sheet.write(3, 1, '2013-XX-XX')

    sheet.write(6, 0, _('Packing List'))

    sheet.write(5, 0, 'school_id')
    sheet.write(5, 1, 'amount')
    wbk.save(filename)
