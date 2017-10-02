
# -*- coding: utf-8 -*-

import requests
import click

"""Main module."""

BASE_URL = 'http://reisapi.ruter.no'
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


def trip_proposals(from_id, to_id):

    payload = {'fromPlace': from_id,
               'toPlace': to_id,
               'time': '01102017190000',
               'isafter': 'True',
               'proposals': '5'
              }

    request = requests.get(GET_TRAVELS_URL, params=payload)

    return request.json().get('TravelProposals')

 
def trip(from_place, to_place):

    from_id = place_id(from_place)

    to_id = place_id(to_place)

    proposals = trip_proposals(from_id, to_id)

    for position, proposal in enumerate(proposals, start=1):

        if proposal.get('Remarks'):
            print('Remarks! Check app or ruter.no.')

        print('Forslag #{0} (Travel time: {1})'.format(position, proposal.get('TotalTravelTime')))

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

            print(text) 

        print()

