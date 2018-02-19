#!/usr/bin/env python3
import json
import re
from html.entities import name2codepoint
uc = str
from modules import proxy
import time
import urllib.request, urllib.error, urllib.parse
import web
import sys

BAD_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.pdf',
                  '.doc', '.docx', '.deb', '.rpm', '.exe', '.zip', '.7z', '.gz',
                  '.tar', '.webm', '.mp4', '.mp3', '.avi', '.mpeg', '.mpg',
                  '.ogv', '.ogg', '.java')
url_finder = re.compile(r'(?iu)(%s?(http|https)(://\S+\.?\S+/?\S+?))' )
r_entity = re.compile(r'&[A-Za-z0-9#]+;')
INVALID_WEBSITE = 0x01
HTML_ENTITIES = { 'apos': "'" }


def noteuri(kenni, input):
    uri = input.group(1).encode('utf-8')
    if not hasattr(kenni, 'last_seen_uri'):
        kenni.last_seen_uri = {}
    kenni.last_seen_uri[input.sender] = uri
noteuri.rule = r'(?u).*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'


def get_page_backup(url):
    req = urllib.request.Request(url, headers={'Accept':'*/*'})
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0')
    u = urllib.request.urlopen(req)
    contents = u.read(262144)
    out = dict()
    try:
        con = (contents).decode('utf-8')
    except:
        con = (contents).decode('iso-8859-1')
    out['code'] = u.code
    out['read'] = con
    out['geturl'] = u.geturl()
    out['headers'] = u.headers.dict
    out['url'] = u.url
    return out['code'], out


def find_title(url):
    """
    This finds the title when provided with a string of a URL.
    """
    if not url.startswith("http"):
        url = 'http://' + url
    if '/#!' in url:
        url = url.replace('/#!', '/?_escaped_fragment_=')

    if 'i.imgur' in url:
        a = url.split('.')
        url = a[0][:-1] + '.'.join(a[1:-1])

    if 'zerobin.net' in url:
        return True, 'ZeroBin'

    url = uc.decode(url)

    msg = str()
    k = 0
    status = False

    while not status:
        if 'i.imgur' not in url:
            real_parts = url.split('?')
            if real_parts and real_parts[0].endswith(BAD_EXTENSIONS):
                break

        k += 1
        if k > 3:
            break

        msg = dict()

        try:
            ## 256 kilobytes
            status, msg = proxy.get_more(url, 1024 * 256)
        except:
            try:
                status, msg = get_page_backup(url)
                print("[url] Proxy isn't working!")
            except:
                print('[url] Proxy and "get_page_backup" have both failed!')
                continue

        if type(msg) == type(dict()) and 'code' in msg:
            status = msg['code']
        else:
            continue

        time.sleep(0.5)


    if not status:
        return False, msg

    useful = msg

    info = useful['headers']
    page = useful['read']

    try:
        mtype = info['content-type']
    except:
        print('failed mtype:', str(info))
        return False, 'mtype failed'
    if not (('/html' in mtype) or ('/xhtml' in mtype)):
        return False, str(mtype)

    content = page


    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.text

    except:
        regex = re.compile('<(/?)title( [^>]+)?>', re.IGNORECASE)
        content = regex.sub(r'<\1title>', content)
        regex = re.compile('[\'"]<title>[\'"]', re.IGNORECASE)
        content = regex.sub('', content)
        start = content.find('<title>')
        if start == -1:
            return False, 'NO <title> found'
        end = content.find('</title>', start)
        if end == -1:
            return False, 'NO </title> found'
        content = content[start + 7:end]
        content = content.strip('\n').rstrip().lstrip()
        title = content


    def e(m):
        entity = m.group()
        if entity.startswith('&#x'):
            cp = int(entity[3:-1], 16)
            meep = chr(cp)
        elif entity.startswith('&#'):
            cp = int(entity[2:-1])
            meep = chr(cp)
        else:
            entity_stripped = entity[1:-1]
            try:
                char = name2codepoint[entity_stripped]
                meep = chr(char)
            except:
                if entity_stripped in HTML_ENTITIES:
                    meep = HTML_ENTITIES[entity_stripped]
                else:
                    meep = str()
        try:
            return uc.decode(meep)
        except:
            return uc.decode(uc.encode(meep))

    title = r_entity.sub(e, title)

    title = title.replace('\n', ' ')
    title = title.replace('\r', ' ')
    title = title.replace('\t', ' ')

    def remove_spaces(x):
        if '  ' in x:
            x = x.replace('  ', ' ')
            return remove_spaces(x)
        else:
            return x


    new_title = str()
    for char in title:
        unichar = uc.encode(char)
        if len(list(uc.encode(char))) <= 3:
            new_title += uc.encode(char)
    title = new_title

    title = re.sub(r'(?i)dcc\ssend', '', title)

    title = remove_spaces(title)
    title = (title).strip()

    title += '\x0F'

    if len(title) > 350:
        title = title[:350] + '\x0F[...]'


    if title:
        return True, title
    else:
        return False, 'No Title'

def remove_nonprint(text):
    new = str()
    for char in text:
        x = ord(char)
        if x > 32 and x <= 126:
            new += char
    return new

def show_title_demand(kenni, input):
    '''.title http://google.com/ -- forcibly show titles for a given URL'''
    uri = input.group(2)

    if uri and 'http' not in uri:
        uri = 'http://' + uri
    if not uri:
        channel = input.sender
        if not hasattr(kenni, 'last_seen_uri'):
            kenni.last_seen_uri = dict()
        if channel in kenni.last_seen_uri:
            uri = kenni.last_seen_uri[channel]
        else:
            return kenni.say('No recent links seen in this channel.')
    passs, page_title = find_title(uri)
    if passs:
        response = page_title
    else:
        response = "No Title Found"
    kenni.say(response)
show_title_demand.commands = ['title']
show_title_demand.priority = 'high'


def collect_links(kenni, input):
    link = input.groups()
    channel = input.sender
    link = link[0]
    if not hasattr(kenni, 'last_seen_uri'):
        kenni.last_seen_uri = dict()
    kenni.last_seen_uri[channel] = link
collect_links.rule = '(?iu).*(%s?(http|https)(://\S+)).*'
collect_links.priority = 'low'

re_meta = re.compile('(?i)content="\S+;\s*?url=(\S+)"\s*?>')


def unbitly(kenni, input):
    '''.longurl <link> -- obtain the final destination URL short URL'''
    url = input.group(2)
    if not url:
        if hasattr(kenni, 'last_seen_uri') and input.sender in kenni.last_seen_uri:
            url = kenni.last_seen_uri[input.sender]
        else:
            return kenni.say('No URL provided')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    status, useful = proxy.get_more(url)
    try:
        new_url = re_meta.findall(useful['read'])
    except:
        return kenni.say(str(useful))

    if new_url:
        new_url = new_url[0]
    else:
        url = url.replace("'", r"\'")
        try:
            status, results = proxy.get_more(url)
            new_url = results['geturl']
        except:
            return kenni.say('Failed to grab URL: %s' % (url))

    channel = input.sender
    if not hasattr(kenni, 'last_seen_uri'):
        kenni.last_seen_uri = dict()
    kenni.last_seen_uri[channel] = new_url

    if new_url.startswith(('http://', 'https://')):
        kenni.say(new_url)
    else:
        kenni.say('Failed to obtain final destination.')
unbitly.commands = ['unbitly', 'untiny', 'longurl', 'st', 'short']
unbitly.priority = 'low'
unbitly.example = '.unbitly http://git.io/6fY4OQ'


def puny(kenni, input):
    '''.puny -- convert to xn-- code for URLs'''
    text = input.group(2)
    if not text:
        return kenni.say('No input provided.')

    if text.startswith('xn--'):
        text = text[4:]
        text_ascii = (text).encode('utf-8')
        try:
            text_unpuny = (text_ascii).decode('punycode')
        except:
            return kenni.say('Stop being a twat.')
        output = (text_unpuny).encode('utf-8')
        output = (output).decode('utf-8')
    else:
        text = (text).encode('utf-8')
        text_utf = (text).decode('utf-8')

        text_puny = (text_utf).encode('punycode')

        output = 'xn--' + text_puny

    return kenni.say(output)
puny.commands = ['puny', 'idn', 'idna']


if __name__ == '__main__':
    print(__doc__.strip())
