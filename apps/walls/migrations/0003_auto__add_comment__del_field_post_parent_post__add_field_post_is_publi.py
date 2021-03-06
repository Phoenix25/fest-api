# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table(u'walls_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comment_created', to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'walls', ['Comment'])

        # Adding M2M table for field notification_users on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_notification_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'user_id'])

        # Adding M2M table for field visible_to on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_visible_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'user_id'])

        # Deleting field 'Post.parent_post'
        db.delete_column(u'walls_post', 'parent_post_id')

        # Adding field 'Post.is_public'
        db.add_column(u'walls_post', 'is_public',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Post.comments_count'
        db.add_column(u'walls_post', 'comments_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Removing M2M table for field childs on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_childs'))

        # Adding M2M table for field notification_users on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_notification_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])

        # Adding M2M table for field visible_to on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_visible_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])

        # Adding M2M table for field comments on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('comment', models.ForeignKey(orm[u'walls.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'comment_id'])


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table(u'walls_comment')

        # Removing M2M table for field notification_users on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_notification_users'))

        # Removing M2M table for field visible_to on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_visible_to'))

        # Adding field 'Post.parent_post'
        db.add_column(u'walls_post', 'parent_post',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_posts', null=True, to=orm['walls.Post'], blank=True),
                      keep_default=False)

        # Deleting field 'Post.is_public'
        db.delete_column(u'walls_post', 'is_public')

        # Deleting field 'Post.comments_count'
        db.delete_column(u'walls_post', 'comments_count')

        # Adding M2M table for field childs on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_childs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('to_post', models.ForeignKey(orm[u'walls.post'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_post_id', 'to_post_id'])

        # Removing M2M table for field notification_users on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_notification_users'))

        # Removing M2M table for field visible_to on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_visible_to'))

        # Removing M2M table for field comments on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_comments'))


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
        u'walls.comment': {
            'Meta': {'ordering': "['time_created']", 'object_name': 'Comment'},
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_created'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'walls.post': {
            'Meta': {'ordering': "['time_created']", 'object_name': 'Post'},
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_created'", 'to': u"orm['auth.User']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['walls.Comment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notification_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visible_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'visible_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'wall': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'walls.wall': {
            'Meta': {'object_name': 'Wall'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'notification_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'walls'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'visible_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'visible_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['walls']