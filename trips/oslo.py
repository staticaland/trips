
# -*- coding: utf-8 -*-

import requests
import click
import udatetime
import time
import logging
from datetime import datetime, date, time
import dotmap
import crayons

"""Main module."""

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
        _after_time = datetime.now()
        # 01102017190000
        after_time = _after_time.strftime('%d%m%Y%H%M%S')

    payload = {'fromPlace': from_id,
               'toPlace': to_id,
               'time': after_time,
               'isafter': 'True',
               'proposals': '5'
              }

    request = requests.get(GET_TRAVELS_URL, params=payload)

    return request.json().get('TravelProposals')


def pretty_time(da_time=''):
    # 2017-10-07T16:41:00+02:00
    time = udatetime.from_string(da_time)
    return datetime.strftime(time, '%H:%M')

 
def trip(from_place, to_place):

    from_id = place_id(from_place)

    to_id = place_id(to_place)

    proposals = trip_proposals(from_id, to_id)

    for position, proposal in enumerate(proposals, start=1):

        click.echo(crayons.yellow('------------ Suggestion #{0} ({1})-------------\n'.format(position, proposal.get('TotalTravelTime'), bold=True)))

        if proposal.get('Remarks'):
            print('Remarks! Check app or ruter.no.')

        for pos, stage in enumerate(proposal.get('Stages'), start=1):

            stage = dotmap.DotMap(stage)

            if stage.Transportation == 0:
                text = '[{0}] Walk ({1})'.format(pos, stage.WalkingTime)
            else:
                step_params = dict(pos=crayons.cyan(pos, bold=True),
                                   departure_name=stage.DepartureStop.Name,
                                   departure_time=pretty_time(stage.DepartureTime),
                                   line_name=stage.LineName,
                                   arrival_name=stage.ArrivalStop.Name,
                                   arrival_time=pretty_time(stage.ArrivalTime),
                                   transportation=TRANSPORTATIONS[stage.Transportation],
                                   )

                text = '[{pos}] From {departure_name} at {departure_time} [{line_name}] -> {arrival_name} at {arrival_time} [{transportation}]'.format(**step_params)

            click.echo(text) 

        click.echo()
