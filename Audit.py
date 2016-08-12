"""
Your task in this exercise has two steps:


- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
 
    the unexpected street types to the appropriate ones in the expected list.

    You have to add mappings only for the actual problems you find in this OSMFILE,

    not a generalized solution, since that may and will depend on the particular area you are auditing.

- write the update_name function, to actually fix the street name.

    The function takes a string with street name as an argument and should return the fixed name
 
   We have provided a simple test so that you see what exactly is expected

"""


import xml.etree.cElementTree as ET

from collections import defaultdict

import re

import pprint



OSMFILE = "sample.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)




expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
 
            "Trail", "Parkway", "Commons"]



# UPDATE THIS VARIABLE


mapping = {

           "Ave": "Avenue",

           "NW": "North West",
           "E": "East",
           "E.":"East",
           "W.":"West",
           "N.":"North",
           "S.":"South",
           "West":"West",
           "Northeast":"North East",
           "SE" :"South East",
           "Blvd": "Boulevard",
           "Blvd.":"Boulevard",
           "CIrcle":"Circle",
           "Hwy": "Highway",
           "Rd.": "Road",
           "St.":"Street",
           "St" :"Street",
           "ST": "Street",
           "Rdt" :"Road",
           "Ln" : "Lane",
           "SW" : "South West",
           "Ct": "Court",
           "Cir": "Circle",
           "AVE": "Avenue"
            }



def audit_street_type(street_types, street_name):

    m = street_type_re.search(street_name)

    if m:

        street_type = m.group()

        if street_type not in expected:

            street_types[street_type].add(street_name)



def is_street_name(elem):

    return (elem.attrib['k'] == "addr:street")





def audit(osmfile):

    osm_file = open(osmfile, "r")

    street_types = defaultdict(set)

    for event, elem in ET.iterparse(osm_file, events=("start",)):


        if elem.tag == "node" or elem.tag == "way":

            for tag in elem.iter("tag"):

               if is_street_name(tag):

                    audit_street_type(street_types, tag.attrib['v'])

    osm_file.close()

    return street_types




def update_name(name, mapping):

    m = street_type_re.search(name)

    better_name = name
    if m:

       try:
           better_street_type = mapping[m.group()]
           better_name = street_type_re.sub(better_street_type, name)
       except KeyError:
           print(m.group())
    return better_name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
       for name in ways:
          better_name = update_name(name, mapping)
          print name, "=>", better_name
          if name == "Cape Anne Ct":

              assert better_name == "Cape Anne Court"
          if name == "Half Street SE":

              assert better_name == "Half Street South East"



if __name__ == '__main__':

    test()
