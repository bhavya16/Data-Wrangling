"""
Your task is to explore the data a bit more.

The first task is a fun one - find out how many unique users 
have contributed to the map in this particular area!


The function process_map should return a set of unique user IDs ("uid")

"""


import xml.etree.cElementTree as ET

import pprint

import re




def get_user(element):

    if element.get("uid"):

        uid = element.attrib["uid"]

        return uid

    else:

        # you want this function to return None if the key doesn't exist

        return None




def process_map(filename):

    users = set()

    for _, element in ET.iterparse(filename):

        if element.get("uid"):

           users.add(element.attrib["uid"])


    return users


users = process_map('sample.osm')
pprint.pprint(users)


"""
RESULT 
set(['86504',
     '866388',
     '867',
     '86769',
     '8699',
     '8703',
     '870861',
     '870879',
     '8764',
     '88337',
     '88961',
     '8909',
     '898696',
     '89943',
     '901014',
     '904963',
     '90516',
     '9065',
     '906532',
     '906974',
     '908687',
     '91056',
     '911135',
     '9112',
     '912025',
     '915044',
     '91568',
     '92074',
     '920804',
     '92274',
     '92286',
     '923250',
     '92387',
     '933797',
     '93524',
     '93549',
     '93679',
     '93788',
     '95488',
     '957',
     '97148',
     '97198',
     '97411',
     '974505',
     '979332',
     '981939',
     '982168',
     '98704',
     '987788',
     '98876',
     '992134',
     '99367',
     '99476',
     '99571',
     '999',
     '999881'])
"""