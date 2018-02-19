#1/usr/bin/env/python

from urlib2.error import HTTPError
from urlib2.parse import quote
from urlib2.parse import urlencode
import random
import requests
import json
import pprint
import sys
import urlib2.request, urlib2.parse, urlib2.error
import argparse

def request(host, path, api_key, url_params=None):

    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(('Querying {0} ...'.format(url)))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def yelp(kenni, input):
    if not hasattr(kenni.config, 'yelp_apikey'):
        return kenni.say('Please sign up for a Yelp API key to use this function.')
    key = kenni.config.yelp_apikey
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

    location = input.group(2)
    if not location:
        kenni.say("Please enter a location.")
        return
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': 3
    }

    response = request(API_HOST, SEARCH_PATH, key, url_params=url_params)

    businesses = response.get('businesses')

    if not businesses:
        kenni.say('No businesses in ' + location + ' found.')
        return
    finalresponse=""
    for x in range(3):
        if x >= len(businesses):
            break
        else:
            if not finalresponse:
                finalresponse = businesses[x]['name']
            else:

                finalresponse = finalresponse + ", " + businesses[x]['name']
    if len(businesses) <= 3:
        kenni.say(str(len(businesses))+ " found: " + finalresponse)
    else:
        kenni.say(str(len(businesses))+ " found, showing first 3: " + finalresponse)

yelp.commands = ["yelp"]
yelp.priority = 'medium'
yelp.example = '.food <location> <thing>'

if __name__ == '__main__':
    print(__doc__.strip())
