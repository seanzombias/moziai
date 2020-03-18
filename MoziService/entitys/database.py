# -*- coding:utf-8 -*-
##########################################################################################################
# File name : contact.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################
'''
数据库公共方法
目前只支持sqlite
'''
import sqlite3

CURSOR_INSTANCE = None
NM2KM = 1.852  # 海里转千米
FEET2M = 0.3048  # 英尺转米
WEAPONS_ASSIST = [1001, 2005, 2006, 2007, 2008, 3001, 3002, 3003, 3004, 4003, 4101, 6001, 7001, 9001, 9002, 9003]


def get_cursor():
    global CURSOR_INSTANCE
    if CURSOR_INSTANCE is None:
        conn = sqlite3.connect('./data/modeldata.db')
        CURSOR_INSTANCE = conn.cursor()
    return CURSOR_INSTANCE


def get_weapon_name_type(weapon_id):
    cursor = get_cursor()
    cursor.execute(
        "SELECT Name,Type FROM dataweapon WHERE ID = %d" % weapon_id)
    weapon_name = ""
    type = 0
    query_data = cursor.fetchone()
    if query_data:
        weapon_name = query_data[0]
        type = query_data[1]
    return weapon_name, type


def get_weapon_type(weapon_id):
    cursor = get_cursor()
    cursor.execute(
        "SELECT Type FROM dataweapon WHERE ID = %d" % weapon_id)
    weapon_type = 0
    query_data = cursor.fetchone()
    if query_data:
        weapon_type = query_data[0]
    return weapon_type


def get_weapon_info(weapon_id):
    cursor = get_cursor()
    data_collect={}
    cursor.execute(
        '''SELECT ID,Name,Type,AirRangeMin,AirRangeMax,LandRangeMin,LandRangeMax,
        LaunchSpeedMax,LaunchSpeedMin,LaunchAltitudeMin_ASL,LaunchAltitudeMax_ASL,TargetSpeedMax ,
        TargetSpeedMin,TargetAltitudeMax,TargetAltitudeMin 
        FROM dataweapon WHERE ID = %d''' % weapon_id)
    values = cursor.fetchone()
    if values:
        data_collect["ID"] = values[0]
        data_collect['Name'] = values[1]
        data_collect['Type'] = values[2]
        data_collect['AirRangeMin'] = values[3] * NM2KM
        data_collect['AirRangeMax'] = values[4] * NM2KM
        data_collect['LandRangeMin'] = values[5] * NM2KM
        data_collect['LandRangeMax'] = values[6] * NM2KM
        data_collect['LaunchSpeedMax'] = values[7] * NM2KM
        data_collect['LaunchSpeedMin'] = values[8] * NM2KM
        data_collect['LaunchAltitudeMin'] = values[9]
        data_collect['LaunchAltitudeMax'] = values[10]
        data_collect['TargetSpeedMax'] = values[11] * NM2KM
        data_collect['TargetSpeedMin'] = values[12] * NM2KM
        data_collect['TargetAltitudeMax'] = values[13]
        data_collect['TargetAltitudeMin'] = values[14]
    return data_collect


def check_weapon_attack(weapon_id):
    '''
    检查武器开火
    '''
    weapon_name, type = get_weapon_name_type(weapon_id)
    if type in WEAPONS_ASSIST:
        return False
    else:
        return True


def get_model_info(category_str, db_id):
    if category_str not in ['aircraft', 'facility', 'weapon']:
        return None

    cursor = get_cursor()
    cursor.execute("SELECT Name,Type FROM data%s where ID=%d" % (category_str, db_id))
    values = cursor.fetchone()
    if values:
        unit_info = {}
        unit_info['name'] = values[0]
        unit_info['type'] = values[1]
        return unit_info
    else:
        return None
