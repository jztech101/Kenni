#!/usr/bin/env python
'''
dinner.py - Dinner Module
Copyright 2014 Sujeet Akula (sujeet@freeboson.org)
Copyright 2013 Michael Yanovich (yanovich.net)
Copyright 2013 Unknown
Licensed under the Eiffel Forum License 2.

More info:
 * kenni-misc: https://github.com/freeboson/kenni-misc/
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/
'''

import re
import web
re_mark = re.compile('<dt><a href="(.*?)" target="_blank">(.*?)</a></dt>')

def food(kenni, input):
    '''.fd -- provide suggestions for dinner'''
    txt = input.group(2)
    url = 'http://www.whatthefuckshouldimakefordinner.com'
    if txt == '-v':
        url = 'http://whatthefuckshouldimakefordinner.com/veg.php'
    page = web.get(url)

    results = re_mark.findall(page)

    if results:

        dish = results[0][1].upper()
        long_url = results[0][0]

        kenni.say("WHY DON'T YOU EAT SOME FUCKING " + dish +
                  ", HERE IS THE RECIPE: " + long_url)

    else:
        kenni.say("I DON'T FUCKING KNOW, EAT PIZZA.")

food.commands = ['food','breakfast','lunch', 'brunch','fucking_dinner', 'fuckingdinner', 'dinner', 'fd', 'wtfsimfd']
food.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
