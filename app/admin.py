from django.contrib import admin
import models


admin.site.register(models.Campaign)
admin.site.register(models.Opponent)
admin.site.register(models.CampaignRound)
admin.site.register(models.Matchup)
admin.site.register(models.MatchupVote)