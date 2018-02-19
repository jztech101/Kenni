#!/usr/bin/env python3
import json
import re
import urlib2request, urlib2parse, urlib2error
import time

user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'


class Grab(urlib2request.URLopener):
    def __init__(self, *args):
        self.version = user_agent
        urlib2request.URLopener.__init__(self, *args)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        return urlib2addinfourl(fp, [headers, errcode], "http:" + url)
urlib2request._urlopener = Grab()


def remote_call(uri, size=0, info=False):
    pyurl = 'https://tumbolia-two.appspot.com/py/'
    code = 'import json;'
    #code += "req=urllib2.Request(%s,headers={'Accept':'*/*'});"
    #code += "req.add_header('User-Agent','%s');" % (user_agent)
    #code += "u=urllib2.urlopen(req);"

    code += 'opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(),'
    code += 'urllib2.BaseHandler(), urllib2.HTTPHandler(),'
    code += 'urllib2.HTTPRedirectHandler(), urllib2.HTTPErrorProcessor(),'
    code += 'urllib2.UnknownHandler());'
    code += 'urllib2.install_opener(opener);'
    code += "req=urllib2.Request(%s, headers={'Accept':'*/*'});"
    code += "req.add_header('User-Agent', '%s');" % (user_agent)
    code += "u=urllib2.urlopen(req);"

    code += "rtn=dict();"
    if info:
        code += "rtn['info']=u.info();"
    else:
        code += "rtn['headers']=u.headers.dict;"
        if size:
            code += "contents=u.read("
            code += str(size)
            code += ");"
        else:
            code += "contents=u.read();"

        code += "con=str();"
        code += r'''exec "try: con=(contents).decode('utf-8')\n'''
        code += '''except: con=(contents).decode('iso-8859-1')";'''
        code += "rtn['read']=con;"
        code += "rtn['url']=u.url;"
        code += "rtn['geturl']=u.geturl();"
        code += "rtn['code']=u.code;"
    code += "print json.dumps(rtn)"
    query = code % repr(uri)
    temp = urlib2parse.quote(query)
    u = urlib2request.urlopen(pyurl + temp)
    results = u.read()
    u.close()

    try:
        useful = json.loads(results)
        return True, useful
    except Exception as error:
        return False, str(results)


def get(uri):
    if not uri.startswith('http'):
        return
    status, u = remote_call(uri)
    if status:
        page = u['read']
    else:
        page = str()
    return page


def get_more(uri, size=0):
    if not uri.startswith('http'):
        uri = 'http://' + uri

    if size:
        status, response = remote_call(uri, size=size)
    else:
        status, response = remote_call(uri)
    return status, response


def head(uri):
    if not uri.startswith('http'):
        uri = 'http://' + uri
    status, response = remote_call(uri, info=True)
    if status:
        page = response['info']
    else:
        page = str()
    return page


if __name__ == "__main__":
    print(__doctype__.strip())
