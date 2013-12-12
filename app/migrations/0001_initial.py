# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Campaign'
        db.create_table(u'app_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'app', ['Campaign'])

        # Adding model 'CampaignRound'
        db.create_table(u'app_campaignround', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rounds', to=orm['app.Campaign'])),
            ('round_ordinal', self.gf('django.db.models.fields.IntegerField')()),
            ('round_name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'app', ['CampaignRound'])

        # Adding model 'Opponent'
        db.create_table(u'app_opponent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=1024)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('wiki', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('blurbl', self.gf('django.db.models.fields.TextField')(null=True)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True)),
        ))
        db.send_create_signal(u'app', ['Opponent'])

        # Adding model 'Matchup'
        db.create_table(u'app_matchup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matchups', to=orm['app.CampaignRound'])),
            ('opponent_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matchup_1s', to=orm['app.Opponent'])),
            ('opponent_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matchup_2s', to=orm['app.Opponent'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Opponent'], null=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'app', ['Matchup'])

        # Adding model 'MatchupVote'
        db.create_table(u'app_matchupvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matchup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['app.Matchup'])),
            ('for_opponent_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('for_opponent_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'app', ['MatchupVote'])


    def backwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table(u'app_campaign')

        # Deleting model 'CampaignRound'
        db.delete_table(u'app_campaignround')

        # Deleting model 'Opponent'
        db.delete_table(u'app_opponent')

        # Deleting model 'Matchup'
        db.delete_table(u'app_matchup')

        # Deleting model 'MatchupVote'
        db.delete_table(u'app_matchupvote')


    models = {
        u'app.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'app.campaignround': {
            'Meta': {'object_name': 'CampaignRound'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': u"orm['app.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'round_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'round_ordinal': ('django.db.models.fields.IntegerField', [], {})
        },
        u'app.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'opponent_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchup_1s'", 'to': u"orm['app.Opponent']"}),
            'opponent_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchup_2s'", 'to': u"orm['app.Opponent']"}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchups'", 'to': u"orm['app.CampaignRound']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Opponent']", 'null': 'True'})
        },
        u'app.matchupvote': {
            'Meta': {'object_name': 'MatchupVote'},
            'for_opponent_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_opponent_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matchup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['app.Matchup']"})
        },
        u'app.opponent': {
            'Meta': {'object_name': 'Opponent'},
            'blurbl': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '1024'}),
            'wiki': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['app']