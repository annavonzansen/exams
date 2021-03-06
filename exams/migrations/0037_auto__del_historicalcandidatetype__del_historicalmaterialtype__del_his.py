# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HistoricalCandidateType'
        db.delete_table(u'exams_historicalcandidatetype')

        # Deleting model 'HistoricalMaterialType'
        db.delete_table(u'exams_historicalmaterialtype')

        # Deleting model 'HistoricalSubject'
        db.delete_table(u'exams_historicalsubject')

        # Deleting model 'HistoricalExamination'
        db.delete_table(u'exams_historicalexamination')

        # Deleting model 'HistoricalTest'
        db.delete_table(u'exams_historicaltest')

        # Deleting model 'HistoricalSubjectGroup'
        db.delete_table(u'exams_historicalsubjectgroup')

        # Deleting model 'HistoricalOrder'
        db.delete_table(u'exams_historicalorder')

        # Deleting model 'HistoricalSpecialArrangement'
        db.delete_table(u'exams_historicalspecialarrangement')

        # Deleting model 'HistoricalCandidateUpload'
        db.delete_table(u'exams_historicalcandidateupload')

        # Deleting model 'HistoricalExamRegistration'
        db.delete_table(u'exams_historicalexamregistration')

        # Deleting model 'HistoricalOrderItem'
        db.delete_table(u'exams_historicalorderitem')

        # Deleting model 'HistoricalCandidate'
        db.delete_table(u'exams_historicalcandidate')


    def backwards(self, orm):
        # Adding model 'HistoricalCandidateType'
        db.create_table(u'exams_historicalcandidatetype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalCandidateType'])

        # Adding model 'HistoricalMaterialType'
        db.create_table(u'exams_historicalmaterialtype', (
            ('one_for_x', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('max_amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalMaterialType'])

        # Adding model 'HistoricalSubject'
        db.create_table(u'exams_historicalsubject', (
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'group_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalSubject'])

        # Adding model 'HistoricalExamination'
        db.create_table(u'exams_historicalexamination', (
            ('season', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2013, max_length=4)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(populate_from=['year', 'season'], allow_duplicates=False, max_length=50, separator=u'-', blank=True, overwrite=False)),
            ('registration_status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            ('registration_begin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('registration_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalExamination'])

        # Adding model 'HistoricalTest'
        db.create_table(u'exams_historicaltest', (
            ('begin', self.gf('django.db.models.fields.DateTimeField')()),
            (u'examination_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'subject_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalTest'])

        # Adding model 'HistoricalSubjectGroup'
        db.create_table(u'exams_historicalsubjectgroup', (
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalSubjectGroup'])

        # Adding model 'HistoricalOrder'
        db.create_table(u'exams_historicalorder', (
            ('status', self.gf('django.db.models.fields.CharField')(default='c', max_length=2)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'examination_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'site_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'parent_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('additional_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'created_by_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalOrder'])

        # Adding model 'HistoricalSpecialArrangement'
        db.create_table(u'exams_historicalspecialarrangement', (
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalSpecialArrangement'])

        # Adding model 'HistoricalCandidateUpload'
        db.create_table(u'exams_historicalcandidateupload', (
            ('status', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            (u'examination_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'order_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'by_user_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('file', self.gf('django.db.models.fields.TextField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'school_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalCandidateUpload'])

        # Adding model 'HistoricalExamRegistration'
        db.create_table(u'exams_historicalexamregistration', (
            ('status', self.gf('django.db.models.fields.CharField')(default='R', max_length=1)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'subject_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'candidate_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('additional_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalExamRegistration'])

        # Adding model 'HistoricalOrderItem'
        db.create_table(u'exams_historicalorderitem', (
            (u'order_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            (u'material_type_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'subject_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalOrderItem'])

        # Adding model 'HistoricalCandidate'
        db.create_table(u'exams_historicalcandidate', (
            ('first_names', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'examination_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'site_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'candidate_type_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'merge_with_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(blank=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'school_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='c', max_length=1)),
            ('candidate_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'person_ptr_id', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, db_index=True)),
            ('retrying', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('identity_number', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
        ))
        db.send_create_signal(u'exams', ['HistoricalCandidate'])


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'language': ('django.db.models.fields.CharField', [], {'default': "'fi'", 'max_length': '2'}),
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
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['name']", 'overwrite': 'False'}),
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
            'candidate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.CandidateType']", 'null': 'True', 'blank': 'True'}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['people.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'retrying': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.School']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.SchoolSite']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '1'})
        },
        u'exams.candidatetype': {
            'Meta': {'object_name': 'CandidateType'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.candidateupload': {
            'Meta': {'object_name': 'CandidateUpload'},
            'by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Order']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.School']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.examination': {
            'Meta': {'unique_together': "(('year', 'season'),)", 'object_name': 'Examination'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'season': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['year', 'season']", 'overwrite': 'False'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2013', 'max_length': '4'})
        },
        u'exams.examregistration': {
            'Meta': {'unique_together': "(('subject', 'candidate'),)", 'object_name': 'ExamRegistration'},
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
        u'exams.materialtype': {
            'Meta': {'object_name': 'MaterialType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'one_for_x': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.order': {
            'Meta': {'ordering': "('-date', 'site', 'examination')", 'object_name': 'Order'},
            'additional_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'examination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Examination']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.Order']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['education.SchoolSite']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '2'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.orderitem': {
            'Meta': {'ordering': "('order', 'subject', 'material_type')", 'unique_together': "(('order', 'subject', 'material_type'),)", 'object_name': 'OrderItem'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.MaterialType']"}),
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
            'Meta': {'ordering': "('group', 'subject_type', 'name', 'short')", 'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exams.SubjectGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['exams.MaterialType']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'exams.subjectgroup': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'SubjectGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
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
            'first_names': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_number': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'merge_with': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['exams']