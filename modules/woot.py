#!/usr/bin/env python3
import feedparser

api = "https://api.woot.com/1/sales/current.rss/www.woot.com"


def woot(kenni, input):
    """ .woot -- pulls the latest information from woot.com """
    output = str()
    parsed = feedparser.parse(api)
    if not parsed['entries']:
        kenni.say("No item currently available.")
        return
    item = parsed['entries'][0]['woot_products']
    link = parsed['entries'][0]['link']
    price = parsed['entries'][0]['woot_price']
    s = parsed['entries'][0]['woot_soldoutpercentage']
    if len(s) == 1:
        soldout = 0
    else:
        soldout = int(s.split('.')[1]) * 10
    condition = parsed['entries'][0]['woot_condition']
    quantity = parsed['entries'][0]['woot_product']['quantity']
    woot_off = parsed['entries'][0]['woot_wootoff']

    base1 = "{0} -- \x02Price:\x02 {1}, \x02Soldout:\x02 {2}% \x02Condition:"
    base2 = "\x02 {3}, \x02Quantity:\x02 {4}, \x02Woot-Off:\x02 {5} -- {6}"
    base = base1 + base2

    link = link.split('?')[0]

    output = base.format(item, price, soldout, condition, quantity,
            woot_off, link.replace("http:", "https:"))
    kenni.say(output)
woot.commands = ['woot']
woot.priority = 'low'
woot.rate = 30

if __name__ == '__main__':
    print(__doc__.strip())
