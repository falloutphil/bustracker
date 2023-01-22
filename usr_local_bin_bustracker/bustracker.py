#!/usr/bin/env python

# python2 - remember!

from Adafruit_8x8 import EightByEight
from time import sleep
from urllib import urlopen
from json import loads
from sys import stderr
from itertools import izip_longest, cycle

font = {

' ':[
 [0,0,0],
 [0,0,0],
 [0,0,0],
 [0,0,0],
 [0,0,0]
],
'1':[
 [0,1,0],
 [1,1,0],
 [0,1,0],
 [0,1,0],
 [1,1,1]
],
'2':[
 [0,1,0],
 [1,0,1],
 [0,0,1],
 [0,1,0],
 [1,1,1]
],
'3':[
 [1,1,1],
 [0,0,1],
 [0,1,1],
 [0,0,1],
 [1,1,1]
],
'4':[
 [1,0,1],
 [1,0,1],
 [1,1,1],
 [0,0,1],
 [0,0,1]
],
'5':[
 [1,1,1],
 [1,0,0],
 [1,1,1],
 [0,0,1],
 [1,1,1]
],
'6':[
 [1,1,1],
 [1,0,0],
 [1,1,1],
 [1,0,1],
 [1,1,1]
],
'7':[
 [1,1,1],
 [0,0,1],
 [0,1,0],
 [1,0,0],
 [1,0,0]
],
'8':[
 [1,1,1],
 [1,0,1],
 [1,1,1],
 [1,0,1],
 [1,1,1]
],
'9':[
 [1,1,1],
 [1,0,1],
 [1,1,1],
 [0,0,1],
 [1,1,1]
],
'0':[
 [1,1,1],
 [1,0,1],
 [1,0,1],
 [1,0,1],
 [1,1,1]
],
'E':[
 [1,1,1],
 [1,0,0],
 [1,1,0],
 [1,0,0],
 [1,1,1]
],
'?':[
 [0,0,0],
 [0,0,0],
 [0,1,0],
 [0,0,0],
 [0,0,0]
],
'*' : [
 [1,1,1,1,1,1,1,1],
 [1,0,0,0,0,0,1,1],
 [1,0,0,0,0,0,0,1],
 [0,1,1,1,1,1,1,1],
 [0,1,1,0,0,1,1,0]
]

}

def handleDue(estimatedTime):
    if estimatedTime == '0':
        estimatedTime = '*'
    return estimatedTime

def printToMatrix(grid, stringInList, starty = 0, startx = 0):
    for letter, char in enumerate(handleDue(stringInList)):
        for ypos, bitRow in enumerate(font[char], starty):
            for xpos, bit in enumerate(bitRow, startx + letter * len(bitRow) + letter):
                grid.setPixel(ypos, xpos, bit) 

# Take the json and iterate through filter for the bus in question and
# return "count" nearest results in minutes
# Inputs are strings so convert to ints for sort
def get_bus_times(*rest_urls, **kwargs):
    count = kwargs.get('count', 2)
    json_data_list = [loads(response.read()) for response in [urlopen(url) for url in rest_urls]]
    return [sorted([str(buses['timeToStation']/60) for buses in data], key=int)[:count] for data in json_data_list]

# Dot Matrix grid is split into two vertical columns
lhs = EightByEight(address=0x70)
rhs = EightByEight(address=0x71)

# Use this to find a bus stop of interest
# https://tfl.gov.uk/tfl/syndication/feeds/bus-stops.csv
# Petersfield Road
url_e3_pr = 'https://api.tfl.gov.uk/line/e3/arrivals/490010968V?direction=outbound&app_id=XXXX&app_key=XXXX'
# Meon Road
url_440_mr = 'https://api.tfl.gov.uk/line/440/arrivals/490010968W?direction=outbound&app_id=XXXX&app_key=XXXX'
# 490003083G ACTON OLD TOWN HALL (westbound)
url_266_th_west = 'https://api.tfl.gov.uk/line/266/arrivals/490003083G?direction=outbound&app_id=XXXX&app_key=XXXX'


while True:
    try:
        next_buses_by_route = get_bus_times(url_e3_pr, url_440_mr, url_266_th_west)
        lhs.clear()
        rhs.clear()
        ypos=0
        # split buses into vertical columns, where each row represents a route.
        # if any route has less than 3 buses due, add a '?' to keep each row earmarked for
        # a specific route.
        buses = izip_longest(*next_buses_by_route, fillvalue='??')
        # iterator that flips between left and right hand grid objects
        sides = cycle([lhs, rhs])
        # enumerate to get a y-axis coordinate reference
        for bus_column, get_side in zip([enumerate(bus) for bus in buses], sides):
            for ymod, wait in bus_column:
               printToMatrix(get_side, wait, ypos)
               ypos += 6 - ymod
            ypos = 0
    except:
        print >> stderr, 'Ooops Python Threw-up, handling and restarting loop...'
    
    sleep(20)





