
# -*- coding: utf-8 -*-

import requests
import click
import blindspin
import time
import logging
from datetime import datetime, date, time

"""Main module."""

logging.basicConfig(level=logging.DEBUG)

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

    with blindspin.spinner():
        request = requests.get(GET_TRAVELS_URL, params=payload)

    return request.json().get('TravelProposals')

 
def trip(from_place, to_place):

    from_id = place_id(from_place)

    to_id = place_id(to_place)

    proposals = trip_proposals(from_id, to_id)

    for position, proposal in enumerate(proposals, start=1):

        if proposal.get('Remarks'):
            print('Remarks! Check app or ruter.no.')

        print('Forslag #{0} (Travel time: {1})\n'.format(position, proposal.get('TotalTravelTime')))

        for pos, stage in enumerate(proposal.get('Stages')):

            if stage.get('Transportation') == 0:
                text = '{0} Walk {1}'.format(pos, stage.get('WalkingTime'))
            else:
                departure_name = stage.get('DepartureStop').get('Name')
                departure = stage.get('DepartureTime')
                line_name = stage.get('LineName')
                arrival_name = stage.get('ArrivalStop').get('Name')
                arrival = stage.get('ArrivalTime')
                transportation = TRANSPORTATIONS.get(stage.get('Transportation'))

                text = '{0} {1} {2} {3} {4} -> {5} {6}'.format(pos, departure_name, departure, line_name, transportation, arrival_name, arrival)

            click.echo(text) 

        click.echo()
