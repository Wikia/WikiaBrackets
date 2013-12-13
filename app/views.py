from django.http import HttpResponse
import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateformat import format
import json


def active_campaigns(request):
    data = dict([(campaign.id, campaign.name) for campaign in models.Campaign.objects.filter(is_active=True)])
    return HttpResponse(json.dumps({'campaigns': data}), content_type="application/json")


def campaign_data(request, campaign_id):
    try:
        campaign = models.Campaign.objects.get(id=campaign_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'message': 'Campaign %d does not exist!' % campaign_id}),
                            content_type="application/json", status=404)
    data = {
        'campaign': {
            'id': campaign.id,
            'name': campaign.name,
            'start_date': format(campaign.start_date, 'U'),
            'end_date': format(campaign.end_date, 'U'),
            'is_active': campaign.is_active,
            'is_complete': campaign.is_complete,
            'active_round': campaign.active_round,
            'num_rounds': campaign.num_rounds,
            'num_opponents': campaign.num_opponents,
            'winner_id': campaign.winner.id if campaign.winner else None,
            'winner_name': campaign.winner.title if campaign.winner else None,
            'active_round': campaign.active_round,
            'rounds': dict([
                (campaign_round.round_ordinal,
                 {
                     'name': campaign_round.round_name,
                     'ordinal': campaign_round.round_ordinal,
                     'is_complete': campaign_round.is_complete,
                     'winners': dict([(opponent.id, opponent.title) for opponent in campaign_round.winners])
                 })
                for campaign_round in campaign.rounds.all()]),
            'matchups_by_round': dict([
                (campaign_round.id,
                 dict([
                     (matchup.id, matchup.json)
                     for matchup in campaign_round.matchups.all()
                 ]))
                for campaign_round in campaign.rounds.all()
            ])
        }
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def opponents(request):
    ids = request.GET.get('ids')
    if ids is None:
        return HttpResponse(json.dumps({'message': 'Include IDs in ids param'}),
                            content_type="application/json", status=404)
    data = dict([(opponent.id, opponent.json) for opponent in models.Opponent.objects.filter(id__in=ids.split(','))])
    return HttpResponse(json.dumps(data), content_type="application/json")

