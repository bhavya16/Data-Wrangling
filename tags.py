"""
Your task is to explore the data a bit more.

Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.



We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}

So, we have to see if we have such tags, and if we have any tags with 
problematic characters.



Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:

  "lower", for tags that contain only lowercase letters and are valid,

  "lower_colon", for otherwise valid tags with a colon in their names,

  "problemchars", for tags with problematic characters, and

  "other", for other tags that do not fall into the other three categories.

See the 'process_map' and 'test' functions for examples of the expected format.

"""

import xml.etree.ElementTree as ET
import pprint
import re

#create the three regular expressions we are checking for
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):

    if element.tag == "tag":

        key = element.get('k')

        if re.search(lower, key):

            keys['lower'] += 1

        elif re.search(lower_colon, key):

            keys['lower_colon'] += 1

        elif re.search(problemchars, key):

            keys['problemchars'] += 1

        else:

            keys['other'] += 1

    return keys

def process_map(filename):
    #initialize dictionary
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        # discard the element is needed to clear from memory and speed up processing
        element.clear()
    return keys

keys = process_map('sample.osm')
pprint.pprint(keys)

#RESULT
#{'lower': 111168, 'lower_colon': 134890, 'other': 5899, 'problemchars': 1}