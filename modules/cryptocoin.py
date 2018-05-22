#!/usr/bin/env python3
import locale
import json
import web
def nicecurrency(c):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    if not c:
        return "Data Not Found"
    else:
        return locale.currency(float(c), grouping=True)

def nicenum(c):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    if not c:
        return "Data Not Found"
    else:
        return locale.format("%d", float(c), grouping=True)
def nicedeci(c):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    if not c:
        return "Data Not Found"
    else:
        return locale.format("%.5f", float(c))

def cryptocoin(kenni, input): 
    try:
        page = web.get("https://api.coinmarketcap.com/v2/listings/")
    except:
        return kenni.say('[CryptoCoin] Connection to API Listings did not succeed.')
    try:
        data = json.loads(page.decode('utf-8'))["data"]
    except:
        return kenni.say("[CryptoCoin] Couldn't make sense of information from API")
    currency = None
    text = input.group(2)
    if not text:
        return kenni.say("You must enter a currency to proceed")
    for x in data:
        if x["name"].lower() == text.lower():
            currency = x["id"]
            break
        elif x["symbol"].lower() == text.lower():
            currency = x["id"]
            break
    if currency is None:
        kenni.say("Currency not found")
    else:
        currency = str(currency)
        try:
            page = web.get("https://api.coinmarketcap.com/v2/ticker/" + currency +"/")
        except:
            return kenni.say('[CryptoCoin] Connection to API Ticker did not succeed.')
        try:
            data = json.loads(page.decode('utf-8'))["data"]
        except:
            return kenni.say("[CryptoCoin] Couldn't make sense of information from API")
        quotes = data["quotes"]["USD"]
        sevdchange = quotes['percent_change_7d']
        if not sevdchange:
            sevdchange = "Data Not Found"
        else:
            sevdchange = str(sevdchange) + "%"
        kenni.say(data["name"] + " (" + data["symbol"] + ") - Price (USD): " + nicecurrency(quotes["price"]) + " - Market Cap (USD): " + nicecurrency(quotes['market_cap']) + " - In Circulation: " + nicenum(data["circulating_supply"]) + " - Max: " 
+ nicenum(data['max_supply']) +  " - Volume (24 hours - USD): " + nicecurrency(quotes['volume_24h']) + " - 1 hour: " + str(quotes['percent_change_1h']) + "% - 24 hours: " + str(quotes['percent_change_24h']) + "% - 7 days: " + sevdchange)
cryptocoin.commands = ['cryptocoin', 'cc']
cryptocoin.example = '.cryptocoin'
cryptocoin.rate = 20

