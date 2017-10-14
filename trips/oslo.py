# -*- coding: utf-8 -*-

import datetime
import logging
import time

import box
import click
import crayons
import requests
import udatetime

BASE_URL = 'https://reisapi.ruter.no'
GET_PLACES_URL = BASE_URL + '/Place/GetPlaces/'
GET_TRAVELS_URL = BASE_URL + '/Travel/GetTravels'
        
TRANSPORTATIONS = { 0: 'Walk',
                    2: 'Bus',
                    5: 'Boat',
                    6: 'Train',
                    7: 'Tram',
                    8: 'Subway'}

def place_id(place):

    request = requests.get(GET_PLACES_URL, params={'id': place})
    request = request.json()
    id = request[0].get('ID')

    return id


def trip_proposals(from_id, to_id, after_time=None):

    if not after_time:

        _after_time = datetime.datetime.now()

        # Should be like 01102017190000
        after_time = _after_time.strftime('%d%m%Y%H%M%S')

    payload = {'fromPlace': from_id,
               'toPlace': to_id,
               'time': after_time,
               'isafter': 'True',
               'proposals': '5'
              }

    request = requests.get(GET_TRAVELS_URL, params=payload)

    return request.json().get('TravelProposals')


def pretty_time(the_time):
    # 2017-10-07T16:41:00+02:00
    time = udatetime.from_string(the_time)
    return datetime.datetime.strftime(time, '%H:%M')

 
def proposals(from_place, to_place):

    """Return a list of proposal dicts"""

    from_id = place_id(from_place)

    to_id = place_id(to_place)

    return trip_proposals(from_id, to_id)


def print_proposals(proposals):

    click.echo()

    for proposal_position, proposal in enumerate(proposals, start=1):

        # Delightful dict dot notation. Makes the code easier to read. Hi!
        proposal = box.Box(proposal, camel_killer_box=True)

        click.echo(crayons.yellow('------------ Suggestion #{0} ({1}) -------------\n'.format(proposal_position, proposal.total_travel_time, bold=True)))

        if proposal.remarks:
            click.echo('Remarks! Check app or ruter.no.')

        for stage_position, stage in enumerate(proposal.stages, start=1):

            if stage.transportation == 0:
                text = '[{0}] Walk ({1})'.format(stage_position, stage.walking_time)
            else:
                step_params = dict(stage_position=crayons.cyan(stage_position, bold=True),
                                   departure_name=stage.departure_stop.name,
                                   departure_time=pretty_time(stage.departure_time),
                                   line_name=stage.line_name,
                                   arrival_name=stage.arrival_stop.name,
                                   arrival_time=pretty_time(stage.arrival_time),
                                   transportation=TRANSPORTATIONS[stage.transportation],
                                   )

                text = '[{stage_position}] {transportation} from {departure_name} at {departure_time} [{line_name}] -> {arrival_name} at {arrival_time}'.format(**step_params)

            click.echo(text) 

        click.echo()
