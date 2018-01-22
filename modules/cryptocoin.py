#!/usr/bin/env python
'''
units.py - jenni Units Module
Copyright 2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/
'''

from modules import proxy
import locale
import json
def nicecurrency(c):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(float(c), grouping=True)

def nicenum(c):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.format("%d", float(c), grouping=True)

def cryptocoin(jenni, input):
    try:
        page = proxy.get("https://api.coinmarketcap.com/v1/ticker/")
    except:
        return jenni.say('[CryptoCoin] Connection to API did not succeed.')

    try:
        data = json.loads(page)
    except:
        return jenni.say("[CryptoCoin] Couldn't make sense of information from API")
    currency = None
    text = input.group(2)
    for x in data:
        if x["name"].lower() == text.lower():
            currency = x
            break
        elif x["id"].lower() == text.lower():
            currency = x
            break
        elif x["symbol"].lower() == text.lower():
            currency = x
            break
    if currency is None:
        jenni.say("Currency not found")
    else:
        jenni.say(currency["name"] + " (" + currency["symbol"] + ") - Price (USD): " + nicecurrency(currency['price_usd']) + " - Market Cap (USD): " + nicecurrency(currency['market_cap_usd']) + " - In Circulation: " + nicenum(currency["available_supply"]) + " - Volume (24 hours - USD): " + nicecurrency(currency['24h_volume_usd']) + " - 1 hour: " + currency['percent_change_1h'] + "% - 24 hours: " + currency['percent_change_24h'] + "% - 7 days: " + currency['percent_change_7d'] + "%")
cryptocoin.commands = ['cryptocoin', 'cc']
cryptocoin.example = '.cryptocoin'
cryptocoin.rate = 20

