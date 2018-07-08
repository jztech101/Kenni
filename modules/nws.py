#!/usr/bin/env python3
import copy
import datetime
import feedparser
import re
import sqlite3
import string
import textwrap
import time
import urllib.request, urllib.parse, urllib.error
import web
import tools

states = {
        'alabama': 'al',
        'alaska': 'ak',
        'arizona': 'az',
        'arkansas': 'ar',
        'california': 'ca',
        'colorado': 'co',
        'connecticut': 'ct',
        'delaware': 'de',
        'florida': 'fl',
        'georgia': 'ga',
        'hawaii': 'hi',
        'idaho': 'id',
        'illinois': 'il',
        'indiana': 'in',
        'iowa': 'ia',
        'kansas': 'ks',
        'kentucky': 'ky',
        'louisiana': 'la',
        'maine': 'me',
        'maryland': 'md',
        'massachusetts': 'ma',
        'michigan': 'mi',
        'minnesota': 'mn',
        'mississippi': 'ms',
        'missouri': 'mo',
        'montana': 'mt',
        'nebraska': 'ne',
        'nevada': 'nv',
        'new hampshire': 'nh',
        'new jersey': 'nj',
        'new mexico': 'nm',
        'new york': 'ny',
        'north carolina': 'nc',
        'north dakota': 'nd',
        'ohio': 'oh',
        'oklahoma': 'ok',
        'oregon': 'or',
        'pennsylvania': 'pa',
        'rhode island': 'ri',
        'south carolina': 'sc',
        'south dakota': 'sd',
        'tennessee': 'tn',
        'texas': 'tx',
        'utah': 'ut',
        'vermont': 'vt',
        'virginia': 'va',
        'washington': 'wa',
        'west virginia': 'wv',
        'wisconsin': 'wi',
        'wyoming': 'wy',
}

months = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
}

conditions = {
    'Heat': '\x02\x0304Heat\x03\x02',
    'Flood': '\x02\x0303Flood\x03\x02',
    'Statement': '\x02\x0313\x1FStatement\x1F\x03\x02',
    'Surf': '\x02\x0311Surf\x03\x02',
    'Thunderstorm': '\x02\x0307Thunderstorm\x03\x02',
    'Red Flag': '\x02\x0304Red Flag\x03\x02',
    'Lake': '\x02\x0311Lake\x03\x02',
    'Effect': '\x02\x0311Effect\x03\x02',
    'Air': '\x02\x0305Air\x03\x02',
    'Tornado': '\x02\x0304!!!TORNADO!!!\x03\x02',
    'Watch': '\x02\x0308\x1F*WATCH*\x1F\x03\x02',
    'Warning': '\x02\x0304!WARNING!\x03\x02',
    'Severe': '\x02\x0305Severe\x03\x02',
    'Special': '\x02\x0306\x1FSpecial\x1F\x03\x02',
    'Fire': '\x02\x0304Fire\x03\x02',
    'Seas': '\x02\x0311Seas\x03\x02',
    'Danger': '\x02\x0304DANGER\x03\x02',
    'Small Craft': '\x02\x0311Small Craft\x03\x02',
    'Advisory': '\x0306Advisory\x03',
    'Hurricane': '\x02\x0313HURRICANE\x03\x02',
    'Wind': '\x02\x0311Wind\x03\x02',
    'Flash': '\x0311Flash\x03',
    'Rip Current': '\x02\x0311Rip Current\x03\x02',
    'Beach Hazards': '\x0308Beach Hazards\x03',
    'Frost': '\x02\x0311Frost\x03\x02',
    'Quality': '\x0313Quality\x03',
    'Hydrologic': '\x0311Hydrologic\x03',
    'Weather': '\x02Weather\x02',
    'High': '\x02\x0304HIGH\x03\x02',
    'Dense Fog': '\x0303Dense Fog\x03',
    'Winter': '\x02\x0311Winter\x03\x02',
    'Rain': '\x0311Rain\x03',
    'Freezing': '\x02\x0311FREEZING\x03\x02',
    'Stagnation': '\x02Stagnation\x02',
    'Freeze': '\x02\x0311FREEZE\x03\x02',
    'Chill': '\x0311Chill\x03',
    'Coastal': '\x02Coastal\x02',
    'Storm': '\x02*Storm*\x02',
    'Blizzard': '\x0311Blizzard\x03',
    'Snow': '\x0311Snow\x03',
}

county_list = 'https://alerts.weather.gov/cap/{0}.php?x=3'
alerts = 'https://alerts.weather.gov/cap/wwaatmget.php?x={0}'
zip_code_lookup = 'https://www.zip-codes.com/zip-code/{0}/zip-code-{0}.asp'
nomsg = 'There are no active watches, warnings or advisories for {0}.'
re_fips = re.compile(r'County FIPS:</.*?>(\S+)</td></tr>')
re_state = re.compile(r'State:</span></td><td class="info"><a href="/state/\S\S.asp">\S\S \[([A-Za-z ]+)\]</a></td></tr>')
re_city = re.compile(r'City:</span></td><td class="info"><a href="/city/\S+.asp">(.*)</a></td></tr>')
re_zip = re.compile(r'^(\d{5})\-?(\d{4})?$')
more_info = 'Complete weather watches, warnings, and advisories for {0}, available here: {1} -- You may also PM the bot to get more details.'
warning_list = 'https://alerts.weather.gov/cap/us.php?x=1'
stop = False
CHANNEL = '##weather'

def colourize(text):
    for condition in conditions:
        if condition in text:
            text = text.replace(condition, conditions[condition])
    return text


def nws_lookup(kenni, input):
    ''' Look up weather watches, warnings, and advisories. '''
    text = input.group(2)
    if not text:
        return kenni.say('You need to provide some input.')
    bits = text.split(',')
    master_url = False
    if len(bits) == 2:
        ## county given
        county = bits[0]
        state = bits[1]
        url_part1 = 'https://alerts.weather.gov'
        state = (state).strip().lower()
        county = (county).strip().lower()
        reverse_lookup = list()
        if len(state) == 2:
            reverse_lookup = [k for k, v in states.items() if v == state]
            if reverse_lookup:
                state = reverse_lookup[0]
        if state not in states and len(reverse_lookup) < 1:
            kenni.say('State not found.')
            return
        url1 = county_list.format(states[state])
        page1 = web.get(url1).split('\n')
        prev1 = str()
        prev2 = str()
        url_part2 = str()
        for line in page1:
            mystr = '>' + str(county) + '<'
            if mystr in line.lower():
                url_part2 = prev2[9:40]
                break
            prev2 = prev1
            prev1 = line
        if not url_part2:
            return kenni.say('Could not find county.')
        master_url = 'https://alerts.weather.gov/cap/' + url_part2
        location = text
    elif len(bits) == 1:
        ## zip code
        if bits[0]:
            zip_code = bits[0]
            zips = re_zip.findall(zip_code)
            if not zips:
                return kenni.say('ZIP is invalid.')
            else:
                try:
                    zip_code = zips[0][0]
                except:
                    return kenni.say('ZIP could not be validated.')
            urlz = zip_code_lookup.format(zip_code)
            pagez = web.get(urlz)
            fips = re_fips.findall(pagez.decode('utf-8',"ignore"))
            if fips:
                state = re_state.findall(pagez.decode('utf-8', "ignore"))
                city = re_city.findall(pagez.decode('utf-8', "ignore"))
                if not state and not city:
                    return kenni.say('Could not match ZIP code to a state')
                try:
                    state = state[0].lower()
                    state = states[state].upper()
                    location = city[0] + ', ' + state
                    fips_combo = str(state) + 'C' + str(fips[0])
                    master_url = alerts.format(fips_combo)
                except:
                    return kenni.say('Could not parse state or city from database.')
            else:
                return kenni.say('ZIP code does not exist.')

    if not master_url:
        return kenni.say('Invalid input. Please enter a ZIP code or a county and state pairing, such as \'Franklin, Ohio\'')

    feed = feedparser.parse(master_url)
    warnings_dict = dict()
    for item in feed.entries:
        if nomsg[:51] == colourize(item['title']):
            return kenni.say(nomsg.format(location))
        else:
            warnings_dict[colourize(str(item['title']))] = str(item['summary'])

    if len(warnings_dict) > 0:
        ## if we have any alerts...
        ## let us sort it so the most recent thing is first, then second, etc...
        warn_keys = list(warnings_dict.keys())
        find_issue = re.compile('issued (\S+) (\S+) at (\S+):(\S+)(\S)M')
        warn_keys_dt = dict()
        for warn in warn_keys:
            warn_dt = find_issue.findall(warn)
            if len(warn_dt) > 0:
                warn_dt = warn_dt[0]
                month = months[warn_dt[0]]
                day = int(warn_dt[1])
                hour = int(warn_dt[2])
                minute = int(warn_dt[3])
                if warn_dt[-1] == 'P':
                    if hour < 12:
                        hour += 12
                year = datetime.datetime.now().year

                hour -= 1
                warn_keys_dt[warn] = datetime.datetime(year, month, day, hour, minute)

        warn_list_dt = sorted(warn_keys_dt, key=warn_keys_dt.get, reverse=True)
        #print 'warn_list_dt', warn_list_dt

        if tools.isChan(input.sender, False) and not (input.group(1)).startswith('nws-more'):
            ## if queried in channel
            for key in warn_list_dt:
                kenni.say(key)
            kenni.say(more_info.format(location, master_url))
        else:
            ## if queried in private message
            for key in warn_list_dt:
                kenni.say(key)
                kenni.say(warnings_dict[key])
            kenni.say(more_info.format(location, master_url))
nws_lookup.commands = ['nws', 'nws-more']
nws_lookup.priority = 'high'
nws_lookup.thread = True
nws_lookup.rate = 10


if __name__ == '__main__':
    print(__doc__.strip())
