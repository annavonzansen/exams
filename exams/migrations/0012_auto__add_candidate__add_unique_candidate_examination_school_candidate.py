# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Candidate'
        db.create_table(u'exams_candidate', (
            (u'person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.Person'], unique=True, primary_key=True)),
            ('examination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Examination'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.School'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.SchoolSite'], null=True, blank=True)),
            ('candidate_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('candidate_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.CandidateType'])),
        ))
        db.send_create_signal(u'exams', ['Candidate'])

        # Adding unique constraint on 'Candidate', fields ['examination', 'school', 'candidate_number']
        db.create_unique(u'exams_candidate', ['examination_id', 'school_id', 'candidate_number'])

        # Adding model 'OrderItem'
        db.create_table(u'exams_orderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Order'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Subject'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'exams', ['OrderItem'])

        # Adding model 'ExamRegistration'
        db.create_table(u'exams_examregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Subject'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Candidate'])),
            ('additional_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='R', max_length=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'exams', ['ExamRegistration'])

        # Adding M2M table for field special_arrangements on 'ExamRegistration'
        m2m_table_name = db.shorten_name(u'exams_examregistration_special_arrangements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('examregistration', models.ForeignKey(orm[u'exams.examregistration'], null=False)),
            ('specialarrangement', models.ForeignKey(orm[u'exams.specialarrangement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['examregistration_id', 'specialarrangement_id'])

        # Adding model 'CandidateType'
        db.create_table(u'exams_candidatetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal(u'exams', ['CandidateType'])

        # Adding model 'SpecialArrangement'
        db.create_table(u'exams_specialarrangement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('short', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'exams', ['SpecialArrangement'])

        # Adding model 'Order'
        db.create_table(u'exams_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['education.SchoolSite'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('examination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Examination'])),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='c', max_length=2)),
            ('additional_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exams.Order'], null=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['Order'])


    def backwards(self, orm):
        # Removing unique constraint on 'Candidate', fields ['examination', 'school', 'candidate_number']
        db.delete_unique(u'exams_candidate', ['examination_id', 'school_id', 'candidate_number'])

        # Deleting model 'Candidate'
        db.delete_table(u'exams_candidate')

        # Deleting model 'OrderItem'
        db.delete_table(u'exams_orderitem')

        # Deleting model 'ExamRegistration'
        db.delete_table(u'exams_examregistration')

        # Removing M2M table for field special_arrangements on 'ExamRegistration'
        db.delete_table(db.shorten_name(u'exams_examregistration_special_arrangements'))

        # Deleting model 'CandidateType'
        db.delete_table(u'exams_candidatetype')

        # Deleting model 'SpecialArrangement'
        db.delete_table(u'exams_specialarrangement')

        # Deleting model 'Order'
        db.delete_table(u'exams_order')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'education.school': {
            'Meta': {'ordering': "('name', 'school_id')", 'object_name': 'School'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'school_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['name']", 'overwrite': 'False'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'education.schoolsite': {
            'Meta': {'unique_together': "(('school', 'name'),)", 'object_name': 'SchoolSite'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'Finland'", 'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postal_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'postal_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.School']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.answer': {
            'Meta': {'object_name': 'Answer'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Assignment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Test']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.answeroption': {
            'Meta': {'object_name': 'AnswerOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '255'})
        },
        u'exams.assignment': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Assignment'},
            'answer_options': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.AnswerOption']", 'null': 'True', 'blank': 'True'}),
            'assignment_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'attached_files': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exams.File']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Test']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.candidate': {
            'Meta': {'unique_together': "(('examination', 'school', 'candidate_number'),)", 'object_name': 'Candidate', '_ormbases': [u'people.Person']},
            'candidate_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'candidate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.CandidateType']"}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['people.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.School']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.SchoolSite']", 'null': 'True', 'blank': 'True'})
        },
        u'exams.candidatetype': {
            'Meta': {'object_name': 'CandidateType'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.examination': {
            'Meta': {'object_name': 'Examination'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['title']", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.examregistration': {
            'Meta': {'object_name': 'ExamRegistration'},
            'additional_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Candidate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'special_arrangements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exams.SpecialArrangement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Subject']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.order': {
            'Meta': {'object_name': 'Order'},
            'additional_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Order']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.SchoolSite']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '2'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Order']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Subject']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.specialarrangement': {
            'Meta': {'object_name': 'SpecialArrangement'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.subject': {
            'Meta': {'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_listening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'material_writing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.test': {
            'Meta': {'object_name': 'Test'},
            'begin': ('django.db.models.fields.DateTimeField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Subject']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'people.person': {
            'Meta': {'object_name': 'Person'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_number': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'merge_with': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['exams']