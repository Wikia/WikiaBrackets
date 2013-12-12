# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Opponent.blurbl'
        db.delete_column(u'app_opponent', 'blurbl')

        # Adding field 'Opponent.blurb'
        db.add_column(u'app_opponent', 'blurb',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Opponent.blurbl'
        db.add_column(u'app_opponent', 'blurbl',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Deleting field 'Opponent.blurb'
        db.delete_column(u'app_opponent', 'blurb')


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
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '1024'}),
            'wiki': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['app']