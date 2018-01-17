#1/usr/bin/env/python
"""
food.py - Jenni Food Module
by afuhrtrumpet

More info:
 * jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/
"""

from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import random
import requests
import json
import pprint
import sys
import urllib
import argparse

def request(host, path, api_key, url_params=None):

    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def food(jenni, input):
    if not hasattr(jenni.config, 'yelp_apikey'):
        return jenni.say('Please sign up for a Yelp API key to use this function.')
    key = jenni.config.yelp_apikey
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

    location = input.group(2)
    if not location:
        jenni.say("Please enter a location.")
        return
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': 3
    }

    response = request(API_HOST, SEARCH_PATH, key, url_params=url_params)

    businesses = response.get('businesses')

    if not businesses:
        jenni.say('No businesses in ' + location + ' found.')
        return
    finalresponse=""
    for x in range(3):
        if x >= len(businesses):
            break
        else:
            if not finalresponse:
                finalresponse = request(API_HOST, BUSINESS_PATH + businesses[x]['id'], key)
            else:
                finalresponse = finalresponse + ", " +request(API_HOST, BUSINESS_PATH + businesses[x]['id'], key)
    if len(businesses) <= 3:
        jenni.say(len(businesses)+ " found: " + finalresponse)
    else:
        jenni.say(len(businesses)+ " found, showing first 3: " + finalresponse)

food.commands = ["food"]
food.priority = 'medium'
food.example = '.food <location> <thing>'

if __name__ == '__main__':
    print __doc__.strip()
