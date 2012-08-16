# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Option'
        db.create_table('sentry_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('value', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('sentry', ['Option'])

        # Adding model 'Team'
        db.create_table('sentry_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('sentry', ['Team'])

        # Adding model 'TeamMember'
        db.create_table('sentry_teammember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_set', to=orm['sentry.Team'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sentry_teammember_set', to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('sentry', ['TeamMember'])

        # Adding unique constraint on 'TeamMember', fields ['team', 'user']
        db.create_unique('sentry_teammember', ['team_id', 'user_id'])

        # Adding model 'Project'
        db.create_table('sentry_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sentry_owned_project_set', null=True, to=orm['auth.User'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Team'], null=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal('sentry', ['Project'])

        # Adding model 'ProjectKey'
        db.create_table('sentry_projectkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='key_set', to=orm['sentry.Project'])),
            ('public_key', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True, null=True)),
            ('secret_key', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('sentry', ['ProjectKey'])

        # Adding model 'ProjectOption'
        db.create_table('sentry_projectoptions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('sentry', ['ProjectOption'])

        # Adding unique constraint on 'ProjectOption', fields ['project', 'key']
        db.create_unique('sentry_projectoptions', ['project_id', 'key'])

        # Adding model 'PendingTeamMember'
        db.create_table('sentry_pendingteammember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pending_member_set', to=orm['sentry.Team'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('sentry', ['PendingTeamMember'])

        # Adding unique constraint on 'PendingTeamMember', fields ['team', 'email']
        db.create_unique('sentry_pendingteammember', ['team_id', 'email'])

        # Adding model 'View'
        db.create_table('sentry_view', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('verbose_name_plural', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('sentry', ['View'])

        # Adding model 'Group'
        db.create_table('sentry_groupedmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('logger', self.gf('django.db.models.fields.CharField')(default='root', max_length=64, db_index=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=40, db_index=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('culprit', self.gf('django.db.models.fields.CharField')(max_length=95, null=True, db_column='view', blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('first_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('resolved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('active_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('time_spent_total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('time_spent_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_public', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('sentry', ['Group'])

        # Adding unique constraint on 'Group', fields ['project', 'logger', 'culprit', 'checksum']
        db.create_unique('sentry_groupedmessage', ['project_id', 'logger', 'view', 'checksum'])
        # 

        # Adding M2M table for field views on 'Group'
        db.create_table('sentry_groupedmessage_views', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['sentry.group'], null=False)),
            ('view', models.ForeignKey(orm['sentry.view'], null=False))
        ))
        db.create_unique('sentry_groupedmessage_views', ['group_id', 'view_id'])

        # Adding model 'GroupMeta'
        db.create_table('sentry_groupmeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Group'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sentry', ['GroupMeta'])

        # Adding unique constraint on 'GroupMeta', fields ['group', 'key']
        db.create_unique('sentry_groupmeta', ['group_id', 'key'])

        # Adding model 'Event'
        db.create_table('sentry_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('logger', self.gf('django.db.models.fields.CharField')(default='root', max_length=64, db_index=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=40, db_index=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('culprit', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, db_column='view', blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event_set', null=True, to=orm['sentry.Group'])),
            ('event_id', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, db_column='message_id')),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('time_spent', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('server_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_index=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_index=True)),
        ))
        db.send_create_signal('sentry', ['Event'])

        # Adding unique constraint on 'Event', fields ['project', 'event_id']
        db.create_unique('sentry_message', ['project_id', 'message_id'])

        # Adding model 'GroupBookmark'
        db.create_table('sentry_groupbookmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bookmark_set', to=orm['sentry.Project'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bookmark_set', to=orm['sentry.Group'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sentry_bookmark_set', to=orm['auth.User'])),
        ))
        db.send_create_signal('sentry', ['GroupBookmark'])

        # Adding unique constraint on 'GroupBookmark', fields ['project', 'user', 'group']
        db.create_unique('sentry_groupbookmark', ['project_id', 'user_id', 'group_id'])

        # Adding model 'FilterKey'
        db.create_table('sentry_filterkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('sentry', ['FilterKey'])

        # Adding unique constraint on 'FilterKey', fields ['project', 'key']
        db.create_unique('sentry_filterkey', ['project_id', 'key'])

        # Adding model 'FilterValue'
        db.create_table('sentry_filtervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=159)),
        ))
        db.send_create_signal('sentry', ['FilterValue'])

        # Adding unique constraint on 'FilterValue', fields ['project', 'key', 'value']
        db.create_unique('sentry_filtervalue', ['project_id', 'key', 'value'])

        # Adding model 'MessageFilterValue'
        db.create_table('sentry_messagefiltervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Group'])),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
            ('first_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
        ))
        db.send_create_signal('sentry', ['MessageFilterValue'])

        # Adding unique constraint on 'MessageFilterValue', fields ['project', 'key', 'value', 'group']
        db.create_unique('sentry_messagefiltervalue', ['project_id', 'key', 'value', 'group_id'])

        # Adding model 'MessageCountByMinute'
        db.create_table('sentry_messagecountbyminute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Group'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('time_spent_total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('time_spent_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('sentry', ['MessageCountByMinute'])

        # Adding unique constraint on 'MessageCountByMinute', fields ['project', 'group', 'date']
        db.create_unique('sentry_messagecountbyminute', ['project_id', 'group_id', 'date'])

        # Adding model 'ProjectCountByMinute'
        db.create_table('sentry_projectcountbyminute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('time_spent_total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('time_spent_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('sentry', ['ProjectCountByMinute'])

        # Adding unique constraint on 'ProjectCountByMinute', fields ['project', 'date']
        db.create_unique('sentry_projectcountbyminute', ['project_id', 'date'])

        # Adding model 'SearchDocument'
        db.create_table('sentry_searchdocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Group'])),
            ('total_events', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('sentry', ['SearchDocument'])

        # Adding unique constraint on 'SearchDocument', fields ['project', 'group']
        db.create_unique('sentry_searchdocument', ['project_id', 'group_id'])

        # Adding model 'SearchToken'
        db.create_table('sentry_searchtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='token_set', to=orm['sentry.SearchDocument'])),
            ('field', self.gf('django.db.models.fields.CharField')(default='text', max_length=64)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('sentry', ['SearchToken'])

        # Adding unique constraint on 'SearchToken', fields ['document', 'field', 'token']
        db.create_unique('sentry_searchtoken', ['document_id', 'field', 'token'])

        # Adding model 'UserOption'
        db.create_table('sentry_useroption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sentry.Project'], null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('sentry', ['UserOption'])

        # Adding unique constraint on 'UserOption', fields ['user', 'project', 'key']
        db.create_unique('sentry_useroption', ['user_id', 'project_id', 'key'])

        # Adding model 'MessageIndex'
        db.create_table('sentry_messageindex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('column', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('sentry', ['MessageIndex'])

        # Adding unique constraint on 'MessageIndex', fields ['column', 'value', 'object_id']
        db.create_unique('sentry_messageindex', ['column', 'value', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MessageIndex', fields ['column', 'value', 'object_id']
        db.delete_unique('sentry_messageindex', ['column', 'value', 'object_id'])

        # Removing unique constraint on 'UserOption', fields ['user', 'project', 'key']
        db.delete_unique('sentry_useroption', ['user_id', 'project_id', 'key'])

        # Removing unique constraint on 'SearchToken', fields ['document', 'field', 'token']
        db.delete_unique('sentry_searchtoken', ['document_id', 'field', 'token'])

        # Removing unique constraint on 'SearchDocument', fields ['project', 'group']
        db.delete_unique('sentry_searchdocument', ['project_id', 'group_id'])

        # Removing unique constraint on 'ProjectCountByMinute', fields ['project', 'date']
        db.delete_unique('sentry_projectcountbyminute', ['project_id', 'date'])

        # Removing unique constraint on 'MessageCountByMinute', fields ['project', 'group', 'date']
        db.delete_unique('sentry_messagecountbyminute', ['project_id', 'group_id', 'date'])

        # Removing unique constraint on 'MessageFilterValue', fields ['project', 'key', 'value', 'group']
        db.delete_unique('sentry_messagefiltervalue', ['project_id', 'key', 'value', 'group_id'])

        # Removing unique constraint on 'FilterValue', fields ['project', 'key', 'value']
        db.delete_unique('sentry_filtervalue', ['project_id', 'key', 'value'])

        # Removing unique constraint on 'FilterKey', fields ['project', 'key']
        db.delete_unique('sentry_filterkey', ['project_id', 'key'])

        # Removing unique constraint on 'GroupBookmark', fields ['project', 'user', 'group']
        db.delete_unique('sentry_groupbookmark', ['project_id', 'user_id', 'group_id'])

        # Removing unique constraint on 'Event', fields ['project', 'event_id']
        db.delete_unique('sentry_message', ['project_id', 'message_id'])

        # Removing unique constraint on 'GroupMeta', fields ['group', 'key']
        db.delete_unique('sentry_groupmeta', ['group_id', 'key'])

        # Removing unique constraint on 'Group', fields ['project', 'logger', 'culprit', 'checksum']
        db.delete_unique('sentry_groupedmessage', ['project_id', 'logger', 'view', 'checksum'])

        # Removing unique constraint on 'PendingTeamMember', fields ['team', 'email']
        db.delete_unique('sentry_pendingteammember', ['team_id', 'email'])

        # Removing unique constraint on 'ProjectOption', fields ['project', 'key']
        db.delete_unique('sentry_projectoptions', ['project_id', 'key'])

        # Removing unique constraint on 'TeamMember', fields ['team', 'user']
        db.delete_unique('sentry_teammember', ['team_id', 'user_id'])

        # Deleting model 'Option'
        db.delete_table('sentry_option')

        # Deleting model 'Team'
        db.delete_table('sentry_team')

        # Deleting model 'TeamMember'
        db.delete_table('sentry_teammember')

        # Deleting model 'Project'
        db.delete_table('sentry_project')

        # Deleting model 'ProjectKey'
        db.delete_table('sentry_projectkey')

        # Deleting model 'ProjectOption'
        db.delete_table('sentry_projectoptions')

        # Deleting model 'PendingTeamMember'
        db.delete_table('sentry_pendingteammember')

        # Deleting model 'View'
        db.delete_table('sentry_view')

        # Deleting model 'Group'
        db.delete_table('sentry_groupedmessage')

        # Removing M2M table for field views on 'Group'
        db.delete_table('sentry_groupedmessage_views')

        # Deleting model 'GroupMeta'
        db.delete_table('sentry_groupmeta')

        # Deleting model 'Event'
        db.delete_table('sentry_message')

        # Deleting model 'GroupBookmark'
        db.delete_table('sentry_groupbookmark')

        # Deleting model 'FilterKey'
        db.delete_table('sentry_filterkey')

        # Deleting model 'FilterValue'
        db.delete_table('sentry_filtervalue')

        # Deleting model 'MessageFilterValue'
        db.delete_table('sentry_messagefiltervalue')

        # Deleting model 'MessageCountByMinute'
        db.delete_table('sentry_messagecountbyminute')

        # Deleting model 'ProjectCountByMinute'
        db.delete_table('sentry_projectcountbyminute')

        # Deleting model 'SearchDocument'
        db.delete_table('sentry_searchdocument')

        # Deleting model 'SearchToken'
        db.delete_table('sentry_searchtoken')

        # Deleting model 'UserOption'
        db.delete_table('sentry_useroption')

        # Deleting model 'MessageIndex'
        db.delete_table('sentry_messageindex')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sentry.event': {
            'Meta': {'unique_together': "(('project', 'event_id'),)", 'object_name': 'Event', 'db_table': "'sentry_message'"},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'culprit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'db_column': "'view'", 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'event_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'db_column': "'message_id'"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_set'", 'null': 'True', 'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '40', 'db_index': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '64', 'db_index': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'server_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_index': 'True'}),
            'time_spent': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'sentry.filterkey': {
            'Meta': {'unique_together': "(('project', 'key'),)", 'object_name': 'FilterKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']"})
        },
        'sentry.filtervalue': {
            'Meta': {'unique_together': "(('project', 'key', 'value'),)", 'object_name': 'FilterValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sentry.group': {
            'Meta': {'unique_together': "(('project', 'logger', 'culprit', 'checksum'),)", 'object_name': 'Group', 'db_table': "'sentry_groupedmessage'"},
            'active_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'culprit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'db_column': "'view'", 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '40', 'db_index': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '64', 'db_index': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'resolved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'time_spent_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_spent_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sentry.View']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'sentry.groupbookmark': {
            'Meta': {'unique_together': "(('project', 'user', 'group'),)", 'object_name': 'GroupBookmark'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmark_set'", 'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmark_set'", 'to': "orm['sentry.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sentry_bookmark_set'", 'to': "orm['auth.User']"})
        },
        'sentry.groupmeta': {
            'Meta': {'unique_together': "(('group', 'key'),)", 'object_name': 'GroupMeta'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'sentry.messagecountbyminute': {
            'Meta': {'unique_together': "(('project', 'group', 'date'),)", 'object_name': 'MessageCountByMinute'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'time_spent_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_spent_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'sentry.messagefiltervalue': {
            'Meta': {'unique_together': "(('project', 'key', 'value', 'group'),)", 'object_name': 'MessageFilterValue'},
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sentry.messageindex': {
            'Meta': {'unique_together': "(('column', 'value', 'object_id'),)", 'object_name': 'MessageIndex'},
            'column': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'sentry.option': {
            'Meta': {'object_name': 'Option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        },
        'sentry.pendingteammember': {
            'Meta': {'unique_together': "(('team', 'email'),)", 'object_name': 'PendingTeamMember'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pending_member_set'", 'to': "orm['sentry.Team']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sentry.project': {
            'Meta': {'object_name': 'Project'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sentry_owned_project_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Team']", 'null': 'True'})
        },
        'sentry.projectcountbyminute': {
            'Meta': {'unique_together': "(('project', 'date'),)", 'object_name': 'ProjectCountByMinute'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'time_spent_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_spent_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'sentry.projectkey': {
            'Meta': {'object_name': 'ProjectKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'key_set'", 'to': "orm['sentry.Project']"}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'sentry.projectoption': {
            'Meta': {'unique_together': "(('project', 'key'),)", 'object_name': 'ProjectOption', 'db_table': "'sentry_projectoptions'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']"}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        },
        'sentry.searchdocument': {
            'Meta': {'unique_together': "(('project', 'group'),)", 'object_name': 'SearchDocument'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_events': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'sentry.searchtoken': {
            'Meta': {'unique_together': "(('document', 'field', 'token'),)", 'object_name': 'SearchToken'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'token_set'", 'to': "orm['sentry.SearchDocument']"}),
            'field': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'sentry.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'sentry.teammember': {
            'Meta': {'unique_together': "(('team', 'user'),)", 'object_name': 'TeamMember'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_set'", 'to': "orm['sentry.Team']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sentry_teammember_set'", 'to': "orm['auth.User']"})
        },
        'sentry.useroption': {
            'Meta': {'unique_together': "(('user', 'project', 'key'),)", 'object_name': 'UserOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sentry.Project']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        },
        'sentry.view': {
            'Meta': {'object_name': 'View'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'verbose_name_plural': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['sentry']