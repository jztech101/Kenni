#!/usr/bin/env python3
import re, unicodedata
from itertools import islice
import web
import random

cp_names = dict()
cp_ranges = dict()
data_loaded = False


def load_data():
    all_code = web.get('http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt')
    all_code = all_code.decode('utf-8')
    for line in all_code.split('\n'):
        parts = line.split(';')
        if len(parts) >= 10:
            name = parts[1]
            name_parts = name.split(',')
            name_part_tmp = name_parts[0].replace('<', '')

            ## look for codepoint ranges
            if 'First>' in name:
                if name_part_tmp not in cp_ranges:
                    cp_ranges[name_part_tmp] = list()
                cp_ranges[name_part_tmp].append(parts[0])
            elif 'Last>' in name:
                if name_part_tmp not in cp_ranges:
                    cp_ranges[name_part_tmp] = list()
                cp_ranges[name_part_tmp].append(parts[0])

            if parts[10]:
                name += ' ' + str(parts[10])

            ## remove '<' and '>' from names (usually only on ranges)
            name = name.replace('<', '')
            name = name.replace('>', '')
            cp_names[parts[0]] = name

    ## generate codepoints for ranges founded above
    for cp_range in cp_ranges:
        cps = cp_ranges[cp_range]
        start = cps[0]
        end = cps[1]

        for number in range(int(start, 16), int(end, 16)):
            cp_names['%04X' % (number)] = cp_range


def about(u, cp=None, name=None):
    global data_loaded

    ## load UnicodeData
    if not data_loaded:
        load_data()
        data_loaded = True

    if cp is None:
        ## cp is not provided, we can safely grab the codepoint
        cp = ord(u)
    else:
        ## codepoint is provided but is in hexadeciaml
        cp = int(cp, 16)

    if name is None:
        name = 'No Name Found'
        ## we need the U+XXXX numbers
        ## which are hex numbers
        ## it is how the numbers are formatted in the UnicodeData file
        search_cp = '%04X' % (cp)
        if search_cp in cp_names:
            name = cp_names[search_cp]

    ## TODO: Replace this...
    if not unicodedata.combining(u):
        template = 'U+%04X %s (%s)'
    else:
        template = 'U+%04X %s (\xe2\x97\x8c%s)'

    return template % (cp, name, u)


def codepoint_simple(arg):
    global data_loaded

    ## load UnicodeData
    if not data_loaded:
        load_data()
        data_loaded = True

    arg = arg.upper()

    r_label = re.compile('\\b' + arg.replace(' ', '.*\\b') + '\\b')

    results = list()

    ## loop over all codepoints that we have
    for cp in cp_names:
        u = chr(int(cp, 16))
        name = cp_names[cp]
        if r_label.search(name):
            results.append((len(name), u, cp, name))

    if not results:
        r_label = re.compile('\\b' + arg.replace(' ', '.*\\b'))

        for cp in cp_names:
            u = chr(int(cp, 16))
            name = cp_names[cp]
            if r_label.search(name):
                results.append((len(name), u, cp, name))

    if not results:
        return None

    length, u, cp, name = sorted(results)[0]
    return about(u, cp, name)


def codepoint_extended(arg):
    global data_loaded

    ## load UnicodeData
    if not data_loaded:
        load_data()
        data_loaded = True

    arg = arg.upper()
    try: r_search = re.compile(arg)
    except: raise ValueError('Broken regexp: %r' % arg)

    ## loop over all codepoints that we have
    for cp in cp_names:
        u = chr(int(cp, 16))
        name = '-'
        name = cp_names[cp]
        if r_search.search(name):
            yield about(u, cp, name)


def u(kenni, input):
    '''Look up unicode information.'''
    arg = input.bytes[3:]
    # kenni.msg('#inamidst', '%r' % arg)
    if not arg:
        return kenni.say('You gave me zero length input.')
    elif not arg.strip(b' '):
        if len(arg) > 1: return kenni.say('%s SPACEs (U+0020)' % len(arg))
        return kenni.say('1 SPACE (U+0020)')

    # @@ space
    if set(arg.upper()) - set(
        'ABCDEFGHIJKLMNOPQRSTUVWYXYZ0123456789- .?+*{}[]\\/^$'):
        printable = False
    elif len(arg) > 1:
        printable = True
    else: printable = False

    if printable:
        extended = False
        for c in '.?+*{}[]\\/^$':
            if c in arg:
                extended = True
                break

        ## allow for codepoints as short as 4 and up to 6
        ## since the official spec as of Unicode 7.0 only has
        ## hexadeciaml numbers with a length no greater than 6
        if 4 <= len(arg) <= 6:
            try: u = chr(int(arg, 16))
            except ValueError: pass
            else: return kenni.say(about(u))

        if extended:
            # look up a codepoint with regexp
            results = list(islice(codepoint_extended(arg), 4))
            for i, result in enumerate(results):
                if (i < 2) or ((i == 2) and (len(results) < 4)):
                    kenni.say(result)
                elif (i == 2) and (len(results) > 3):
                    kenni.say(result + ' [...]')
            if not results:
                kenni.say('Sorry, no results')
        else:
            # look up a codepoint freely
            result = codepoint_simple(arg)
            if result is not None:
                kenni.say(result)
            else: kenni.say('Sorry, no results for %r.' % arg)
    else:
        text = arg.decode('utf-8')
        if len(text) <= 3:
            ## look up less than three podecoints
            for u in text:
                kenni.say(about(u))
        elif len(text) <= 10:
            ## look up more than three podecoints
            kenni.say(' '.join('U+%04X' % ord(c) for c in text))
        else:
            ## oh baby
            kenni.say('Sorry, your input is too long!')
u.commands = ['u', 'unicode']
u.example = '.u 203D'

if __name__ == '__main__':
    print(__doc__.strip())
