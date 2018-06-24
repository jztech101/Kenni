#!/usr/bin/env python3
import re
import web
import tools
uri = 'https://en.wiktionary.org/w/index.php?title=%s&printable=yes'
r_tag = re.compile(r'<[^>]+>')
r_ul = re.compile(r'(?ims)<ul>.*?</ul>')

def text(html):
    text = r_tag.sub('', html).strip()
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('(intransitive', '(intr.')
    text = text.replace('(transitive', '(trans.')
    return text

def wiktionary(word):
    bytes = web.get(uri % web.quote(word)).decode('utf-8')
    bytes = r_ul.sub('', bytes)

    mode = None
    etymology = None
    definitions = {}
    for line in bytes.splitlines():
        if 'id="Etymology"' in line:
            mode = 'etymology'
        elif 'id="Noun"' in line:
            mode = 'noun'
        elif 'id="Verb"' in line:
            mode = 'verb'
        elif 'id="Adjective"' in line:
            mode = 'adjective'
        elif 'id="Adverb"' in line:
            mode = 'adverb'
        elif 'id="Interjection"' in line:
            mode = 'interjection'
        elif 'id="Particle"' in line:
            mode = 'particle'
        elif 'id="Preposition"' in line:
            mode = 'preposition'
        elif 'id="' in line:
            mode = None

        elif (mode == 'etmyology') and ('<p>' in line):
            etymology = text(line)
        elif (mode is not None) and ('<li>' in line):
            definitions.setdefault(mode, []).append(text(line))

        if '<hr' in line:
            break
    return etymology, definitions

parts = ('preposition', 'particle', 'noun', 'verb',
    'adjective', 'adverb', 'interjection')

def format(word, definitions, number=2):
    result = '%s' % word
    for part in parts:
        if part in definitions:
            defs = definitions[part][:number]
            result += ' \u2014 ' + ('%s: ' % part)
            n = ['%s. %s' % (i + 1, e.strip(' .')) for i, e in enumerate(defs)]
            result += ', '.join(n)
    return result.strip(' .,')

def define(kenni, input):
    word = input.group(2)
    if not word:
        kenni.say("You want the definition for what?")
        return
    word = (word).lower()
    etymology, definitions = wiktionary(word)
    if not definitions:
        kenni.say("Couldn't get any definitions for %s at Wiktionary." % word)
        return

    result = format(word, definitions)
    y=3
    while len(result) < tools.charlimit-20:
        result = format(word, definitions, y)
        y+=1
    if len(result) > tools.charlimit:
        result = result[:tools.charlimit-5] + '[...]'
    kenni.say(result)
define.commands = ['dict', 'define', 'word']
define.example = '.w bailiwick'

if __name__ == '__main__':
    print(__doc__.strip())
