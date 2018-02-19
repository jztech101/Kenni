#!/usr/bin/env python3
import proxy
import locale
import json
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
        page = proxy.get("https://files.coinmarketcap.com/generated/search/quick_search.json")
    except:
        return kenni.say('[CryptoCoin] Connection to API did not succeed.')
    try:
        data = json.loads(page)
    except:
        return kenni.say("[CryptoCoin] Couldn't make sense of information from API")
    currency = None
    text = input.group(2)
    if not text:
        return kenni.say("You must enter a currency to proceed")
    for x in data:
        if x["name"].lower() == text.lower():
            currency = x["slug"]
            break
        #elif x["symbol"].lower() == text.lower():
        #   currency = x["slug"]
        #    break
        else:
            for y in x["tokens"]:
                if y.lower() == text.lower():
                    currency = x["slug"]
                    break
    if currency is None:
        kenni.say("Currency not found")
    else:
        try:
            page = proxy.get("https://api.coinmarketcap.com/v1/ticker/" + currency +"/")
        except:
            return kenni.say('[CryptoCoin] Connection to API did not succeed.')
        try:
            data = json.loads(page)
        except:
            return kenni.say("[CryptoCoin] Couldn't make sense of information from API")
        data=data[0]
        sevdchange = data['percent_change_7d']
        if not sevdchange:
            sevdchange = "Data Not Found"
        else:
            sevdchange = sevdchange + "%"
        kenni.say(data["name"] + " (" + data["symbol"] + ") - Price (USD): " + nicecurrency(data['price_usd']) + " - Price (BTC): " + nicedeci(data['price_btc']) + " - Market Cap (USD): " + nicecurrency(data['market_cap_usd']) + " - In Circulation: " + nicenum(data["available_supply"]) + " - Volume (24 hours - USD): " + nicecurrency(data['24h_volume_usd']) + " - 1 hour: " + data['percent_change_1h'] + "% - 24 hours: " + data['percent_change_24h'] + "% - 7 days: " + sevdchange)
cryptocoin.commands = ['cryptocoin', 'cc']
cryptocoin.example = '.cryptocoin'
cryptocoin.rate = 20

