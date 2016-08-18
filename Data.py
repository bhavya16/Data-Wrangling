#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import sys
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.
In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:
<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>
  should be turned into:
{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}
- for "way" specifically:
  <nd ref="305896090"/>
  <nd ref="1719825889"/>
should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

mapping = {"Ave": "Avenue",

           "NW": "North West",
           "NE": "North East",
           "E": "East",
           "E.":"East",
           "E ": "East",
           "W.":"West",
           "W ":"West",
           "N.":"North",
           "N": "North",
           "N ":"North",
           "S.":"South",
           "S ":"South",
           "West":"West",
           "Northeast":"North East",
           "SE" :"South East",
           "Blvd": "Boulevard",
           "Blvd.":"Boulevard",
           "CIrcle":"Circle",
           "Hwy": "Highway",
           "Rd.": "Road",
           "Rd ":"Road",
           "St.":"Street",
           "St":"Street",
           "St ":"Street",
           "ST": "Street",
           "Rdt" :"Road",
           "Ln": "Lane",
           "SW": "South West",
           "Ct": "Court",
           "Cir": "Circle",
           "AVE": "Avenue",
          }

def is_street_name(k):
    return (k == "addr:street")

def update_name(name, mapping):
    name = name.strip()
    print 'BEFORE'
    print name
    pattern = re.compile(r'\b(' + '|'.join(mapping.keys()) + r')\b')
    if pattern:
        name = pattern.sub(lambda x: mapping[x.group()], name)
        print 'AFTER'
        print name.strip('.')
    return name.strip('.')

def fix_postcode(v):

    postcode = ''
    for char in v:
        if char.isdigit():
            postcode += char
        if len(postcode) == 5:
            break
    return postcode

def node_update_k(node, value, tag):
    """Adds 'k' and 'v' values from tag as new key:value pair to node."""
    k = value
    v = tag.attrib['v']                       
    if k.startswith('addr:'):
        # Ignore 'addr:street:' keys with 2 colons
        if k.count(':') == 1:
            if 'address' not in node:
                node['address'] = {}
            if k == 'addr:postcode' and len(v) > 5:
                v = fix_postcode(v)
            # Fix all substrings of street names using a
            # more generalized update method from audit.py
            elif k == 'addr:street':
                v = audit.update(v, audit.mapping)
            node['address'][k[5:]] = v


def shape_element(element):

    node = {}

    address = {}

    pos = []

    if element.tag == "node" or element.tag == "way" :

        # YOUR CODE HERE

        node["id"] = element.attrib["id"]

        node["type"] =  element.tag

        node[ "visible"] = element.get("visible")

        created = {}

        created["version"] = element.attrib["version"]

        created["changeset"] = element.attrib["changeset"]

        created["timestamp"] = element.attrib["timestamp"]

        created["user"] = element.attrib["user"]

        created["uid"] = element.attrib["uid"]

        node["created"] = created

        if "lat" in element.keys() and "lon" in element.keys():

           pos = [element.attrib["lat"], element.attrib["lon"]]
        
           node["pos"] = [float(string) for string in pos]

        else:

           node["pos"] = None

        for tag in element.iter('tag'):

           if re.search('addr:', tag.attrib['k']):

                if len(tag.attrib['k'].split(":")) < 3:

                    addr_add = tag.attrib['k'].split(":")[1]

                    #address[addr_add] = tag.attrib['v']
                    address[addr_add] = update_name(tag.attrib['v'],mapping)
                     
        if address:

            node['address'] = address
        for nd in element.iter("nd"):
            if not "node_refs" in node.keys():
                node["node_refs"] = []
            node_refs = node["node_refs"]
            node_refs.append(nd.attrib["ref"])
            node["node_refs"] = node_refs
        return node


    else:

        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():

    data = process_map('sample.osm', False)

if __name__ == '__main__':
    test()