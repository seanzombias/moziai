#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : geo.py
# Create date : 2019-10-21 15:40
# Modified date : 2020-01-09 05:38
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from math import radians, cos, sin, asin, sqrt, degrees, atan2, degrees
from . import pylog

def get_point_with_point_bearing_distance(lat, lon, bearing, distance):
    '''
    一直一点求沿某一方向一段距离的点
    '''
    #pylog.info("lat:%s lon:%s bearing:%s distance:%s" % (lat, lon, bearing, distance))
    radiusEarthKilometres = 3440
    initialBearingRadians = radians(bearing)
    disRatio = distance / radiusEarthKilometres
    distRatioSine = sin(disRatio)
    distRatioCosine = cos(disRatio)
    startLatRad = radians(lat)
    startLonRad = radians(lon)
    startLatCos = cos(startLatRad)
    startLatSin = sin(startLatRad)
    endLatRads = asin((startLatSin * distRatioCosine) + (startLatCos * distRatioSine * cos(initialBearingRadians)))
    endLonRads = startLonRad + atan2(sin(initialBearingRadians) *distRatioSine * startLatCos, distRatioCosine - startLatSin * sin(endLatRads))
    my_lat = degrees(endLatRads)
    my_lon = degrees(endLonRads)
    dic = {"latitude" : my_lat, "longitude" : my_lon}
    return dic

def get_two_point_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c*r*1000

def get_degree(latA, lonA, latB, lonB):

    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y,x))
    brng = (brng + 360) % 360
    return brng
