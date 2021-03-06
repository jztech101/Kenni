#!/usr/bin/env python3
import re
import web


def excuse(kenni, input):
    a = re.compile('<a [\s\S]+>(.*)</a>')

    try:
        page = web.get('http://programmingexcuses.com/')
    except:
        return kenni.say("I'm all out of excuses!")

    results = a.findall(page.decode('utf-8'))

    if results:
        result = results[0]
        result = result.strip()
        if result[-1] not in ['.', '?', '!']:
            result += '.'
        kenni.say(result)
    else:
        kenni.say("I'm too lazy to find an excuse.")
excuse.commands = ['why', 'excuse', 'excuses']


if __name__ == '__main__':
    print(__doc__.strip())
