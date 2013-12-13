from django.contrib import admin
import models


class MatchupAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'slug', 'round', 'opponent_1',
                    'opponent_1_votes', 'opponent_2', 'opponent_2_votes', 'winner')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'is_complete',
                    'num_rounds', 'num_opponents', 'num_opponents_required', 'active_round', 'winner')


class CampaignRoundAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'round_ordinal', 'round_name', 'is_active', 'is_complete')


admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Opponent)
admin.site.register(models.CampaignRound, CampaignRoundAdmin)
admin.site.register(models.Matchup, MatchupAdmin)
admin.site.register(models.MatchupVote)