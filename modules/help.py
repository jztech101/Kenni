def doc(kenni, input):
    """Shows a command's documentation, and possibly an example."""
    if input.group(2):
        name = input.group(2)
        if name and name in kenni.doc:
            kenni.say(kenni.doc[name][0])
            if kenni.doc[name][1]:
                kenni.say('e.g. ' + kenni.doc[name][1])
        else:
            kenni.say('No help found')
    else:
        kenni.say('help: Returns possibly helpful information')
doc.commands = ['help']
doc.example = 'help'
doc.priority = 'low'
