from django.db import models
from dirtyfields import DirtyFieldsMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
        return self.rounds.filter(is_complete=False).order_by('round_ordinal')[0]

    @property
    def winner(self):
        last_round_winners = self.rounds[-1].winners
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
        return self.campaign.active_round.id == self.id

    @property
    def winners(self):
        return filter(lambda x: x, [matchup.winner for matchup in self.matchups])

    def __unicode__(self):
        return self.round_name


@receiver(pre_save, sender=CampaignRound)
def tally_matchups_when_campaign_round_is_completed(sender, instance, *args, **kwargs):
    map(lambda x: x.assign_winner, instance.matchups)


class Opponent(models.Model):
    url = models.URLField(max_length=1024, unique=True,
                          help_text="This is the URL of the article we're matching up")
    title = models.CharField(max_length=1024, help_text="The article title we're referring to (editable)")
    wiki = models.CharField(max_length=1024, help_text="The name of the wiki the article is from.")
    blurbl = models.TextField(null=True, help_text="Add a blurb for this opponent here")
    thumbnail = models.URLField(max_length=1024,
                                null=True,
                                help_text="Automatically generated on creation, but editable")

    def __unicode__(self):
        return u"(%s) %s" % (self.title, self.wiki)

    @property
    def matchups(self):
        return self.matchup_1s + self.matchup_2s


class Matchup(models.Model):
    name = models.CharField(max_length=1024, null=True, help_text="Useful for marketing a given matchup")
    slug = models.SlugField(null=True, unique=True, help_text="Use a slug for marketing a matchup URL")
    round = models.ForeignKey(CampaignRound, related_name='matchups',
                              help_text="The round of the campaign this matchup is happening")
    opponent_1 = models.ForeignKey(Opponent, related_name="matchup_1s", help_text="The first \"opponent\"")
    opponent_2 = models.ForeignKey(Opponent, related_name="matchup_2s", help_text="The second \"opponent\"")
    winner = models.ForeignKey(Opponent, null=True, help_text="Who won the matchup")
    blurb = models.TextField(null=True, help_text="A place for you put a writeup on this matchup")

    def assign_winner(self):
        opponent_1_votes = self.votes.filter(for_opponent_1=True).count()
        opponent_2_votes = self.votes.filter(for_opponent_2=True).count()
        if opponent_1_votes > opponent_2_votes:
            self.winner = self.opponent_1
        else:
            self.winner = self.opponent_2
        self.save()


class MatchupVote(models.Model):
    matchup = models.ForeignKey(Matchup, related_name='votes')
    for_opponent_1 = models.BooleanField(default=False)
    for_opponent_2 = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.for_opponent_1 and self.for_opponent_2) or not (self.for_opponent_1 or self.for_opponent_2):
            raise Exception("There must be a vote for a single opponent")
        super(MatchupVote, self).save()
