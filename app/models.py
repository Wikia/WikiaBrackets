from django.db import models
from dirtyfields import DirtyFieldsMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver
import requests


class Campaign(models.Model):
    name = models.CharField(max_length=1024,
                            help_text="The name of the campaign, like 'The Beard-Off'")
    start_date = models.DateTimeField(null=True,
                                      help_text="For record-keeping purposes, start date of the campaign")
    end_date = models.DateTimeField(null=True,
                                    help_text="For record-keeping purposes, end date of the campaign")
    is_active = models.BooleanField(default=False,
                                    help_text="For listing active campaigns on the Wikia app")
    is_complete = models.BooleanField(default=False,
                                      help_text="A complete campaign will have a winner")

    def __unicode__(self):
        return self.name

    @property
    def active_round(self):
        ar = self.rounds.filter(is_complete=False).order_by('round_ordinal').last()
        if ar:
            return ar.round_ordinal
        return -1

    @property
    def num_rounds(self):
        return self.rounds.count()

    @property
    def num_opponents(self):
        first_round = self.rounds.first()
        if first_round is None:
            return 0
        matchups = first_round.matchups.all()
        return len(
            filter(lambda x: x.opponent_1, matchups)
            + filter(lambda x: x.opponent_2, matchups)
        )

    @property
    def num_opponents_required(self):
        return (self.rounds.count()) + 1 ** 2

    @property
    def winner(self):
        last_round_winners = self.rounds.last().winners
        if len(last_round_winners) == 1:
            return last_round_winners[0]


class CampaignRound(DirtyFieldsMixin, models.Model):
    campaign = models.ForeignKey(Campaign, related_name="rounds",
                                 help_text="The campaign this round applies to.")
    round_ordinal = models.IntegerField(help_text="The order that this round occurs in. Start at 1, and go up.")
    round_name = models.CharField(max_length=1024,
                                  help_text="""e.g. "The Sweet Sixteen".""")
    is_complete = models.BooleanField(default=False,
                                      help_text="Helps us identify the active round")

    @property
    def is_active(self):
        return self.campaign.active_round == self.round_ordinal

    @property
    def campaign_name(self):
        return self.campaign.name

    @property
    def winners(self):
        return filter(lambda x: x, [matchup.winner for matchup in self.matchups.all()])

    def __unicode__(self):
        return self.round_name


@receiver(pre_save, sender=CampaignRound)
def tally_matchups_when_campaign_round_is_completed(sender, instance, *args, **kwargs):
    if instance.is_complete and len(instance.winners) == 0:
        map(lambda x: x.assign_winner, instance.matchups.objects.all())


class Opponent(models.Model):
    url = models.URLField(max_length=1024, unique=True,
                          help_text="This is the URL of the article we're matching up")
    title = models.CharField(max_length=1024, blank=True,
                             help_text="The article title we're referring to (editable)")
    wiki = models.CharField(max_length=1024,
                            blank=True,
                            help_text="The name of the wiki the article is from.")
    blurb = models.TextField(null=True, blank=True, help_text="Add a blurb for this opponent here")
    thumbnail = models.URLField(max_length=1024,
                                null=True,
                                blank=True,
                                help_text="Automatically generated on creation, but editable")

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.wiki)

    @property
    def matchups(self):
        return list(self.matchup_1s.all()) + list(self.matchup_2s.all())

    @property
    def json(self):
        return {
            'name': self.title,
            'wiki': self.wiki,
            'blurb': self.blurb,
            'thumbnail': self.thumbnail,
            'matchups': dict([(matchup.id, matchup.json) for matchup in self.matchups])
        }

    def get_metadata_from_url(self):
        baseurl, title = self.url.split('/wiki/')
        response = requests.get(baseurl+'/api/v1/Articles/Details', params=dict(titles=title))
        if response.status_code is not 200:
            raise Exception("Couldn't get data from API")
        items = response.json().get('items', [])
        if len(items) == 0:
            raise Exception("Couldn't get data from API")
        #hack required due to PLA-1043
        article_id = items.values()[0]['id']
        response = requests.get(baseurl+'/api/v1/Articles/Details', params=dict(ids=article_id))
        if response.status_code is not 200:
            raise Exception("Couldn't get data from API")
        article_response = response.json()
        items = article_response.get('items', [])
        if len(items) == 0:
            raise Exception("Couldn't get data from API")
        data = items.get(str(article_id))
        if not data:
            raise Exception("Couldn't get data from API")
        if not self.title:
            self.title = data['title']
        if not self.thumbnail:
            self.thumbnail = data.get('thumbnail')
        params = dict(expand=1, string=article_response['basepath'], limit=1, batch=1, includeDomain='true')
        wiki_response = requests.get('http://www.wikia.com/api/v1/Wikis/ByString',
                                     params=params)
        if wiki_response.status_code is not 200:
            raise Exception("Couldn't get data from API")
        wiki_items = wiki_response.json().get('items', [])
        if len(wiki_items) == 0:
            raise Exception("Couldn't get data from API")
        wiki_result = wiki_items[0]
        if not self.wiki:
            self.wiki = wiki_result['name']


@receiver(pre_save, sender=Opponent)
def get_data_from_api_on_create(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.get_metadata_from_url()


class Matchup(models.Model):
    name = models.CharField(max_length=1024, null=True, help_text="Useful for marketing a given matchup")
    slug = models.SlugField(null=True, unique=True, help_text="Use a slug for marketing a matchup URL")
    round = models.ForeignKey(CampaignRound, related_name='matchups',
                              help_text="The round of the campaign this matchup is happening")
    opponent_1 = models.ForeignKey(Opponent, related_name="matchup_1s", help_text="The first \"opponent\"")
    opponent_2 = models.ForeignKey(Opponent, related_name="matchup_2s", help_text="The second \"opponent\"")
    winner = models.ForeignKey(Opponent, null=True, blank=True, help_text="Who won the matchup")
    blurb = models.TextField(null=True, help_text="A place for you put a writeup on this matchup")

    @property
    def json(self):
        return {
            'name': self.name,
            'blurb': self.blurb,
            'campaign_id': self.campaign.id,
            'campaign_name': self.campaign.name,
            'opponents': {
                self.opponent_1_id: {
                    'name': unicode(self.opponent_1),
                    'votes': self.opponent_1_votes
                },
                self.opponent_2_id: {
                    'name': unicode(self.opponent_2),
                    'votes': self.opponent_2_votes
                }
            }
        }

    @property
    def campaign(self):
        return self.round.campaign

    def assign_winner(self):
        opponent_1_votes = self.votes.filter(for_opponent_1=True).count()
        opponent_2_votes = self.votes.filter(for_opponent_2=True).count()
        if opponent_1_votes > opponent_2_votes:
            self.winner = self.opponent_1
        else:
            self.winner = self.opponent_2
        self.save()

    @property
    def opponent_1_votes(self):
        return self.votes.filter(for_opponent_1=True).count()

    @property
    def opponent_2_votes(self):
        return self.votes.filter(for_opponent_2=True).count()

    def __unicode__(self):
        return "%s round %d -- %s: %s vs. %s" % (self.round.campaign.name, self.round.round_ordinal,
                                                 self.name, self.opponent_1, self.opponent_2)


class MatchupVote(models.Model):
    matchup = models.ForeignKey(Matchup, related_name='votes')
    for_opponent_1 = models.BooleanField(default=False)
    for_opponent_2 = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.for_opponent_1 and self.for_opponent_2) or not (self.for_opponent_1 or self.for_opponent_2):
            raise Exception("There must be a vote for a single opponent")
        super(MatchupVote, self).save()

    def __unicode__(self):
        opp = self.matchup.opponent_1 if self.for_opponent_1 else self.matchup.opponent_2
        return "%s round %d -- %s: Vote for %s" % (self.matchup.round.campaign.name,
                                                self.matchup.round.round_ordinal,
                                                self.matchup.name,
                                                opp)