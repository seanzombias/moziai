# -*- coding:utf-8 -*-

"""
地理信息库
"""
import math

PI = 3.1415926535897932
degree2radian = PI / 180.0
NM2KM = 1.852  # 海里转千米
EARTH_RADIUS = 6371137  # 地球平均半径


def get_horizontal_distance(geopoint1, geopoint2):
    """
     求地面两点的水平距离   Haversine公式
    :param geopoint1: tuple, (lat, lon), 例：(40.9, 140.0)
    :param geopoint2: tuple, (lat, lon), 例：(40.9, 142.0)
    :return: float, KM
    """
    lat1 = geopoint1[0] * degree2radian
    lon1 = geopoint1[1] * degree2radian
    lat2 = geopoint2[0] * degree2radian
    lon2 = geopoint2[1] * degree2radian

    difference = lat1 - lat2
    mdifference = lon1 - lon2
    distance = 2 * math.asin(math.sqrt(math.pow(math.sin(difference / 2), 2)
                                       + math.cos(lat1) * math.cos(lat2)
                                       * math.pow(math.sin(mdifference / 2), 2)))
    distance = distance * EARTH_RADIUS / 1000
    return distance


def get_slant_distance(geopoint1, geopoint2):
    """
    获取三维直线距离, 点高需为海拔高度
    :param geopoint1: tuple, (lat, lon, alt), 例：(40.9, 140.0, 560.8)
    :param geopoint2: tuple, (lat, lon, alt), 例：(40.9, 142.0, 4560.8)
    :return: float, KM
    """
    hd = get_horizontal_distance(geopoint1, geopoint2)
    delta_alt = geopoint1[2] - geopoint2[2]
    return get_range(hd, delta_alt)


def get_range(range_km, delta_alt):
    """
    获取直线距离
    :param range_km: float, 水平距离，KM
    :param delta_alt: float, 垂直距离，m
    :return: float, KM
    """
    range_km *= 1000.0
    return math.sqrt((range_km * range_km + delta_alt * delta_alt)) / 1000.0


def normal_angle(angle):
    """
    角度调整为0-360度以内
    :param angle: float, 角度
    :return: float
    """
    if 0 <= angle < 360:
        return angle
    else:
        return angle % 360


def get_azimuth(geopoint1, geopoint2):
    """
    获取point1 指向 point2 的方位角
    :param geopoint1: tuple, (lat, lon), 例：(40.9, 140.0)
    :param geopoint2: tuple, (lat, lon), 例：(40.9, 142.0)
    :return: 角度 0-360, 正北：0， 正东:90, 顺时针旋转，正西：270
    """
    lat1 = geopoint1[0] * degree2radian
    lon1 = geopoint1[1] * degree2radian
    lat2 = geopoint2[0] * degree2radian
    lon2 = geopoint2[1] * degree2radian
    azimuth = 180 * math.atan2(math.sin(lon2 - lon1), math.tan(lat2) * math.cos(lat1) - math.sin(lat1) * math.cos(lon2 - lon1)) / PI
    return normal_angle(azimuth)


