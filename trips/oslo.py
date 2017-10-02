
# -*- coding: utf-8 -*-

import requests
import click

"""Main module."""

BASE_URL = 'http://reisapi.ruter.no'
GET_PLACES_URL = BASE_URL + '/Place/GetPlaces/'
GET_TRAVELS_URL = BASE_URL + '/Travel/GetTravels'

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

        print('Forslag #{0} (Travel time: {1})'.format(position, proposal.get('TotalTravelTime')))
        
        #click.echo('Avreise:', proposal.get('DepartureTime'))
        
        for pos, stage in enumerate(proposal.get('Stages')):
            print('Steg:', pos)
            print('Linjenavn:', stage.get('LineName'))
            try:
                print(stage.get('DepartureStop').get('Name'))
            except:
                pass
            print('Transporttype', stage.get('Transportation'))
        
        print(proposal.get('ArrivalTime'))
        if proposal.get('Remarks'):
            print('Remarks! Check app or ruter.no.')
