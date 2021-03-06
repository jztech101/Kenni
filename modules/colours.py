#!/usr/bin/env python3
import tools
colours = {
    "00": "white",
    "01": "black",
    "02": "blue",
    "03": "green",
    "04": "light red",
    "05": "red",
    "06": "magenta (purple)",
    "07": "orange",
    "08": "yellow",
    "09": "light green",
    "10": "cyan",
    "11": "light cyan",
    "12": "light blue",
    "13": "light magenta (pink)",
    "14": "gray",
    "15": "light grey",
    "16": "unk",
    "17": "unk",
    "18": "unk",
    "19": "unk",
    "20": "unk",
    "21": "unk",
    "22": "unk",
    "23": "unk",
    "24": "unk",
}


def test_colours(kenni, input):
    if not input.admin and tools.isChan(input.sender, False):
        return
    output = str()

    keys = list(colours.keys())
    keys.sort()
    bold_output = str()
    for colour in keys:
        output += "\x03{0}{1} ({0})\x03, ".format(colour, colours[colour])
        bold_output += "\x02\x03{0}{1} ({0})\x03\x02, ".format(colour,
                                                               colours[colour])

    output = output[:-2]
    bold_output = bold_output[:-2]

    kenni.say(output)
    kenni.say(bold_output)
test_colours.commands = ['color', 'colour', 'colors', 'colours']
test_colours.priority = 'high'


if __name__ == '__main__':
    print(__doc__.strip())
