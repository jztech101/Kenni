#!/usr/bin/env python3
import web

def val(kenni, input):
    """Check a webpage using the W3C Markup Validator."""
    if not input.group(2):
        return kenni.say("Nothing to validate.")
    uri = input.group(2)
    if not uri.startswith('http://'):
        uri = 'http://' + uri

    path = '/check?uri=%s;output=xml' % web.urlib2.quote(uri)
    info = web.head('http://validator.w3.org' + path)

    result = uri + ' is '

    if isinstance(info, list):
        return kenni.say('Got HTTP response %s' % info[1])

    if 'X-W3C-Validator-Status' in info:
        result += str(info['X-W3C-Validator-Status'])
        if info['X-W3C-Validator-Status'] != 'Valid':
            if 'X-W3C-Validator-Errors' in info:
                n = int(info['X-W3C-Validator-Errors'].split(' ')[0])
                if n != 1:
                    result += ' (%s errors)' % n
                else: result += ' (%s error)' % n
    else: result += 'Unvalidatable: no X-W3C-Validator-Status'

    kenni.say(result)
val.rule = (['val'], r'(?i)(\S+)')
val.example = '.val http://www.w3.org/'

if __name__ == '__main__':
    print(__doc__.strip())
