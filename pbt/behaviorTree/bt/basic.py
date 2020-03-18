#!/usr/bin/python
# -*- coding: utf-8 -*-
# by aie

import math

def InternationalDecimalConverter(value):
    if type(value) == int:
        value = float(value)
    if type(value) == float:
        return value
    else:
        convert = str.replace(value, ",", ".")
        return float(convert)


'''
    aa=InternationalDecimalConverter('3,123')
print(aa)
aa=InternationalDecimalConverter('3.123')
print(aa)
aa=InternationalDecimalConverter(3.123)
print(aa)
'''


# aa=InternationalDecimalConverter(3,123)
# print(aa)

def MakeLatLong(latitude, longitude):
    instance = {}
    instance['latitude'] = InternationalDecimalConverter(latitude)
    instance['longitude'] = InternationalDecimalConverter(longitude)
    return instance


# aa=MakeLatLong(32.13,4.234)
# print(aa)

def MidPointCoordinate(lat1, lon1, lat2, lon2):
    # initialize
    lat1 = InternationalDecimalConverter(lat1)
    lon1 = InternationalDecimalConverter(lon1)
    lat2 = InternationalDecimalConverter(lat2)
    lon2 = InternationalDecimalConverter(lon2)
    dLon = math.radians(lon2 - lon1)
    # convert to radians
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)

    Bx = math.cos(lat2) * math.cos(dLon)
    By = math.cos(lat2) * math.sin(dLon)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
                      math.sqrt((math.cos(lat1) + Bx) * (math.cos(lat1) + Bx) + By * By))
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)

    return MakeLatLong(math.degrees(lat3), math.degrees(lon3))


'''
aa=MidPointCoordinate(0,0,0,40)
print(aa)
aa=MidPointCoordinate(0,0,30,40)
print(aa)
aa=MidPointCoordinate(10,20,30,40)
print(aa)
'''


def ProjectLatLong(origin, bearing, range):
    radiusEarthKilometres = 3440
    initialBearingRadians = math.radians(bearing)
    distRatio = range / radiusEarthKilometres
    distRatioSine = math.sin(distRatio)
    distRatioCosine = math.cos(distRatio)
    startLatRad = math.radians(origin['latitude'])
    startLonRad = math.radians(origin['longitude'])
    startLatCos = math.cos(startLatRad)
    startLatSin = math.sin(startLatRad)
    endLatRads = math.asin(
        (startLatSin * distRatioCosine) + (startLatCos * distRatioSine * math.cos(initialBearingRadians)))
    endLonRads = startLonRad + math.atan2(math.sin(initialBearingRadians) * distRatioSine * startLatCos,
                                          distRatioCosine - startLatSin * math.sin(endLatRads))
    return MakeLatLong(math.degrees(endLatRads), math.degrees(endLonRads))


'''
aa=MakeLatLong(0,0)
bb=ProjectLatLong(aa,30,10)
print(bb)
'''


def FindBoundingBoxForGivenLocations(coordinates, padding):
    west = 0.0
    east = 0.0
    north = 0.0
    south = 0.0

    # Condiation Check
    if coordinates == None or len(coordinates) == 0:
        padding = 0

    # Assign Up to numberOfReconToAssign
    for lc in range(0, len(coordinates)):
        loc = coordinates[lc]
        if lc == 0:
            north = loc['latitude']
            south = loc['latitude']
            west = loc['longitude']
            east = loc['longitude']
        else:
            if loc['latitude'] > north:
                north = loc['latitude']
            elif loc['latitude'] < south:
                south = loc['latitude']

            if loc['longitude'] < west:
                west = loc['longitude']
            elif (loc['longitude'] > east):
                east = loc['longitude']

    # Adding Padding
    north = north + padding
    south = south - padding
    west = west - padding
    east = east + padding

    # Return In Format
    return [MakeLatLong(north, west), MakeLatLong(north, east), MakeLatLong(south, east), MakeLatLong(south, west)]


'''
aa=MakeLatLong(32.13,4.234)
bb=FindBoundingBoxForGivenLocations([aa],10)
print(bb)
'''

def CombineTablesNew(table1, table2):
    combinedTable = {}
    for k, v in table1.items():
        combinedTable[len(combinedTable)] = v

    for k, v in table2.items():
        combinedTable[len(combinedTable)] = v

    return combinedTable

'''
aa={'a':1,'b':2,'c':3}
bb={'d':4,'e':5,'f':6}
cc=CombineTablesNew(aa,bb)
print(cc)
'''

def CombineTables(table1,table2):
    for k, v in table2.items():
        table1[len(table1)] = v
    return table1


'''
aa={'a':1,'b':2,'c':3}
bb={'d':4,'e':5,'f':6}
cc=CombineTables(aa,bb)
print(cc)
{'c': 3, 3: 5, 4: 6, 'b': 2, 'a': 1, 5: 4}
'''


'''
# 在Python中直截就可以使用split
def Split(s, sep):
     fields = {}
     sep = sep or " "
     pattern = str.format("([^%s]+)", sep)
     str.replace(s, pattern, lambda c: fields[len(fields)] == c)
     return fields
'''

