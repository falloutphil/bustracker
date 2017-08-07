#!/usr/bin/env python

from Adafruit_8x8 import EightByEight
from time import sleep
from urllib import urlopen
from json import loads
from sys import stderr

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
'*' : [
 [1,1,1,1,1,1,1,1],
 [1,0,0,0,0,0,1,1],
 [1,0,0,0,0,0,0,1],
 [0,1,1,1,1,1,1,1],
 [0,1,1,0,0,1,1,0]
]

}


# https://api.tfl.gov.uk/Line/E3,440,N11/Arrivals/490010968V?direction=outbound&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY
# [{"$type":"Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities","id":"278132595","operationType":1,"vehicleId":"SK07DYC","naptanId":"490010968V","stationName":"Petersfield Road","lineId":"440","lineName":"440","platformName":"V","direction":"outbound","bearing":"158","destinationNaptanId":"","destinationName":"Chiswick Power Road","timestamp":"2016-07-31T13:53:36Z","timeToStation":1115,"currentLocation":"","towards":"Turnham Green","expectedArrival":"2016-07-31T14:12:11.3563248Z","timeToLive":"2016-07-31T14:12:41.3563248Z","modeName":"bus"}]

def handleDue( estimatedTime ):
    if estimatedTime == '0':
        estimatedTime = '*'
    return estimatedTime

def printToMatrix( grid, stringInList, starty=0, startx=0 ):
    for letter,char in enumerate( handleDue(stringInList) ):
        for ypos,bitRow in enumerate(font[char], starty):
            for xpos,bit in enumerate(bitRow,startx+letter*len(bitRow)+letter):
                grid.setPixel(ypos,xpos,bit) 



lhs = EightByEight(address=0x70)
rhs = EightByEight(address=0x71)

url = 'https://api.tfl.gov.uk/line/e3,440,n11/arrivals/490010968V?direction=outbound&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY'

while True:
    try:
        response = urlopen(url);
        data = loads(response.read())
        #print data
        #print '------------------------------------'
	nextThreeE3 = sorted([str(buses['timeToStation']/60) for buses in data if buses['lineId'] == 'e3'],key=int)[:3]
	nextTwo440 = sorted([str(buses['timeToStation']/60) for buses in data if buses['lineId'] == '440'],key=int)[:2]
	nextOneN11 = sorted([str(buses['timeToStation']/60) for buses in data if buses['lineId'] == 'N11'],key=int)[:1]
        lhs.clear()
        rhs.clear()
        ypos=0
        if len(nextThreeE3) > 0:
            for ymod,wait in enumerate(nextThreeE3):
                printToMatrix( lhs, wait, ypos )
                ypos+=(6-ymod)
        ypos=0
        if len(nextTwo440) > 0:
            for ymod,wait in enumerate(nextTwo440):
                printToMatrix( rhs, wait, ypos )
                ypos+=(6-ymod)
        if len(nextOneN11) > 0: printToMatrix( rhs, nextOneN11.pop(), 11, 1 )
    except:
        print >> stderr, 'Ooops Python Threw-up, handling and restarting loop...'
    
    sleep(20)





