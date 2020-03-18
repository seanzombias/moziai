#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : task_reward.py
# Create date : 2019-10-21 16:29
# Modified date : 2020-01-09 18:35
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from math import cos
from math import radians
from . import etc
from . import pylog
from .geo import get_degree
from .geo import get_two_point_distance

def get_target_point():
    lat2 = etc.task_end_point["latitude"]
    lon2 = etc.task_end_point["longitude"]
    return lat2, lon2

def get_target_distance(lat, lon):
    lat2, lon2 = get_target_point()
    distance = get_two_point_distance(lon, lat, lon2, lat2)
    return distance

def get_distance_reward(lat, lon, last_heading, heading_change):
    lat2, lon2 = get_target_point()

    distance = get_two_point_distance(lon, lat, lon2, lat2)
    task_heading = get_degree(lat, lon, lat2, lon2)
    current_heading = last_heading + heading_change
    return _get_reward_value8(task_heading, current_heading, distance)

def _get_reward_value(task_heading, current_heading):
    angel = abs(task_heading - current_heading)
    if angel < 90:
        return 1.0
    return -1.0

def _get_reward_value2(task_heading, current_heading):
    angel = abs(task_heading - current_heading)
    pylog.info("task_heading:%s current_heading:%s angel:%s" % (task_heading, current_heading, angel))
    return cos(radians(angel))

def _get_reward_value3(task_heading, current_heading, distance):
    angel = abs(task_heading - current_heading)
    pylog.info("task_heading:%s current_heading:%s angel:%s distance:%s" % (task_heading, current_heading, angel, distance))
    return (10000 * cos(radians(angel))) / distance

def _get_reward_value4(task_heading, current_heading, distance):
    angel = abs(task_heading - current_heading)
    pylog.info("task_heading:%s current_heading:%s angel:%s distance:%s" % (task_heading, current_heading, angel, distance))
    cos_value = cos(radians(angel))
    if cos_value >= 0:
        return (10000 * cos(radians(angel))) / distance
    else:
        return (-distance / 10000) + (10000 * cos(radians(angel))) / distance

def _get_reward_value5(task_heading, current_heading, distance):
    angel = abs(task_heading - current_heading)
    pylog.info("task_heading:%s current_heading:%s angel:%s distance:%s" % (task_heading, current_heading, angel, distance))
    cos_value = cos(radians(angel))
    if cos_value >= 0:
        return (10000 * cos(radians(angel))) / distance
    else:
        return  (distance * cos(radians(angel))) / 100000

def _get_reward_value6(task_heading, current_heading, distance):
    return -distance/1000.0

def _get_reward_value7(task_heading, current_heading, distance):
    angel = abs(task_heading - current_heading)
    pylog.info("task_heading:%s current_heading:%s angel:%s distance:%s" % (task_heading, current_heading, angel, distance))
    cos_value = cos(radians(angel))
    if cos_value >= 0:
        return (10000 * cos(radians(angel))) / distance
    else:
        return 0.0

def _get_reward_value8(task_heading, current_heading, distance):
    angel = abs(task_heading - current_heading)
    cos_value = cos(radians(angel))
    if cos_value >= 0:
        reward = (10000 * cos(radians(angel))) / distance
        #pylog.info("positive move get %s reward" % reward)
        return reward
    else:
        neg_reward = (distance * cos(radians(angel))) / 10000
        #pylog.info("negtive move : distance:%s neg_reward:%s" % (distance, neg_reward))
        return neg_reward
