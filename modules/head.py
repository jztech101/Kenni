#!/usr/bin/env python3
import http.client, time
from html.entities import name2codepoint
import web


def head(kenni, input):
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '')
    if ' ' in uri:
        uri, header = uri.rsplit(' ', 1)
    else: uri, header = uri, None

    if not uri and hasattr(kenni, 'last_seen_uri'):
        try: uri = kenni.last_seen_uri[input.sender]
        except KeyError: return kenni.say('?')

    if not uri.startswith('htt'):
        uri = 'http://' + uri

    if '/#!' in uri:
        uri = uri.replace('/#!', '/?_escaped_fragment_=')

    try: info = web.head(uri)
    except IOError: return kenni.say("Can't connect to %s" % uri)
    except http.client.InvalidURL: return kenni.say("Not a valid URI, sorry.")

    if not isinstance(info, list):
        try: info = dict(info)
        except TypeError:
            return kenni.say('Try .head http://example.org/ [optional header]')
        info['Status'] = '200'
    else:
        newInfo = dict(info[0])
        newInfo['Status'] = str(info[1])
        info = newInfo

    if header is None:
        data = []
        if 'Status' in info:
            data.append(info['Status'])
        if 'Content-Type' in info:
            data.append(info['Content-Type'].replace('; charset=', ', '))
        if 'Last-Modified' in info:
            modified = info['Last-Modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if 'Content-Length' in info:
            data.append(info['Content-Length'] + ' bytes')
        kenni.say(', '.join(data))
    else:
        if header in info:
            kenni.say(header + ': ' + info.get(header))
        else:
            msg = 'There was no %s header in the response.' % header
            kenni.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'

if __name__ == '__main__':
    print(__doc__.strip())
