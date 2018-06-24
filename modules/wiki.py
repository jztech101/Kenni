#!/usr/bin/env python3
import re
import web
import tools
import wikipedia
def wiki(kenni, input):
    query = input.group(2)
    if not query:
        kenni.say("Please enter a query")
    else:
        results = wikipedia.search(query)
        if not results:
            kenni.say("No results found")
        else:
            try:
               page = wikipedia.page(results[0])
            except wikipedia.DisambiguationError as err:
               page = wikipedia.page(err.options[0])
            wikiTitle = page.title
            wikiUrl = page.url
            wikiSummary = page.summary[:tools.charlimit-len(wikiUrl)-15] + " [...]"
        kenni.say(wikiTitle + " : " + wikiSummary + " - " + wikiUrl)
wiki.commands = ['wikipedia', 'wiki']

if __name__ == '__main__':
    print(__doc__.strip())
