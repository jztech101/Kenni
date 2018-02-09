#!/usr/bin/env python2
"""
search.py - kenni Web Search Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2013, Edward Powell (embolalia.net)
Copyright 2008-2013 Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
"""

import json
import re
import urllib
import web
from modules import proxy
from modules.url import find_title
r_tag = re.compile(r'<(?!!)[^>]+>')
r_bing = re.compile(r'<h2><a href="([^"]+)"')


def remove_spaces(x):
    if '  ' in x:
        x = x.replace('  ', ' ')
        return remove_spaces(x)
    else:
        return x


def bing_search(query, lang='en-GB'):
    query = web.urllib.quote(query)
    base = 'https://www.bing.com/search?mkt=%s&q=' % lang
    page = proxy.get(base + query)
    m = r_bing.search(page)
    if m: return m.group(1)


def bing(kenni, input):
    """Queries Bing for the specified input."""
    query = input.group(2)
    if query.startswith(':'):
        lang, query = query.split(' ', 1)
        lang = lang[1:]
    else: lang = 'en-GB'
    if not query:
        return kenni.reply('.bing what?')

    query = query.encode('utf-8')
    uri = bing_search(query, lang)
    if uri:
        passs, title = find_title(uri)
        if passs:
            kenni.say("[" + title +"] " + uri)
        else:
            kenni.say(uri)
        if not hasattr(kenni, 'last_seen_uri'):
            kenni.last_seen_uri = {}
        kenni.last_seen_uri[input.sender] = uri
    else: kenni.reply("No results found for '%s'." % query)
bing.commands = ['bing']
bing.example = '.bing swhack'


def duck_sanitize(incoming):
    return web.decode((incoming).decode('utf-8'))

def duck_search(query):
    '''Do a DuckDuckGo Search'''

    ## grab results from the API for the query
    duck_api_results = duck_api(query)

    ## output is a string of the URL result

    ## try to find the first result
    if 'Results' in duck_api_results and min_size('Results', duck_api_results):
        ## 'Results' is the most common place to look for the first result
        output = duck_api_results['Results'][0]['FirstURL']
    elif 'AbstractURL' in duck_api_results and min_size('AbstractURL', duck_api_results):
        ## if there is no 'result', let's try AbstractURL
        ## this is usually a wikipedia article
        output = duck_api_results['AbstractURL']
    elif 'RelatedTopics' in duck_api_results and min_size('RelatedTopics', duck_api_results):
        ## if we still can't find a search result, let's grab a topic URL
        ## this is usually vaguely related to the search query
        ## many times this is a wikipedia result
        for topic in duck_api_results['RelatedTopics']:
            output = '%s - %s' % (topic['Name'], topic['Topics'][0]['FirstURL'])
            if 'duckduckgo.com' in output:
                ## as a last resort, DuckDuckGo will provide links to the query on its site
                ## it doesn't appear to ever return a https URL
                output = output.replace('http://', 'https://')
            break
    else:
        ## if we still can't find a search result via the API
        ## let's try scraping the html page
        uri = 'https://duckduckgo.com/html/?q=%s&kl=us-en&kp=-1' % web.urllib.quote(query)
        page = proxy.get(uri)

        r_duck = re.compile(r'nofollow" class="[^"]+" href="(.*?)">')

        bad_results = ['/y.js?', '//ad.ddg.gg/', '.msn.com/', 'r.search.yahoo.com/',]
        m = r_duck.findall(page)
        output = str()
        if m:
            for result in m:
                valid_result = True
                for each in bad_results:
                    if each in result:
                        valid_result = False
                if valid_result:
                    output = result
                    break
        else:
            return None
    return duck_sanitize(output)

def min_size(key, dictt):
    ## I am lazy
    return len(dictt[key]) > 0


def duck_api(query):
    '''Send 'query' to DDG's API and return results as a dictionary'''
    #query = web.urllib.quote(query)
    uri = 'https://api.duckduckgo.com/?q=%s&format=json&no_html=1&no_redirect=1&kp=-1' % query
    results = proxy.get(uri)
    results = json.loads(results)
    return results

def duck(kenni, input):
    '''Perform a DuckDuckGo Search and Zero-Click lookup'''
    query = input.group(2)
    if not query:
        return kenni.reply('.ddg what?')

    #query = query.encode('utf-8')
    #kenni.say('query: ' + query)

    ## try to find a search result via the API
    uri = duck_search(query)
    if uri:
        passs, title = find_title(uri)
        if passs:
            kenni.say("[" + title +"] " + uri)
        else:
            kenni.say(uri)
    else:
        return kenni.reply("No results found for '%s'." % query)
duck.commands = ['duck', 'ddg', 'g', 'search']

if __name__ == '__main__':
    print __doc__.strip()
