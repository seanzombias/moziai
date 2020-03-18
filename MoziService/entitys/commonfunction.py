# -*- coding:utf-8 -*-

import re
from datetime import datetime, timedelta
import pickle
import os
import math
import numpy as np
import json

import MoziService.entitys.database as db
from MoziService.entitys import geo

ZERO_TIME = datetime(1970, 1, 1, 0, 0, 0)

guid_list_pattern = re.compile("\[\d\] = \'([0-9a-z-^=]+)\'")
mission_guid_pattern = re.compile(r"mission {\r\n guid = '([a-z0-9-]+)',", re.M | re.S)
lus_mission_info_str = ""
lua_table2json = ""
lua_common_function_str = ""

lua_contacts_all_str = ""
lua_contact_str = ""
lua_units_all_str = ""
lua_unit_str = ""
lua_situation_str = ""

lua_detect_str = ""

lua_path = 'lua'


def get_lua_table2json():
    """
    获取Lua公共函数, table2json
    :return:
    """
    global lua_table2json
    if not lua_table2json:
        with open(os.path.join(lua_path, 'table_to_json.lua'), mode='r', encoding='ascii') as fp:
            lua_table2json = fp.read()
    return lua_table2json


def get_lua_mission_parser():
    """
    获取Lua公共函数，为任务详细信息解析
    :return:
    """
    global lus_mission_info_str
    if not lus_mission_info_str:
        with open(os.path.join(lua_path, 'lua_mission.lua'), mode='r', encoding='ascii') as fp:
            lus_mission_info_str = fp.read()
    return lus_mission_info_str

def get_lua_common_str():
    """
    获取Lua公共函数, 可为获取所有实体和情报实体
    :return:
    """
    global lua_common_function_str
    if not lua_common_function_str:
        with open(os.path.join(lua_path, 'lua_common_function.lua'), mode='r', encoding='ascii') as fp:
            lua_common_function_str = fp.read()
    return lua_common_function_str


def get_lua_contacts_all_str():
    """
    获取情报实体调用lua代码
    :return:
    """
    global lua_contacts_all_str
    if not lua_contacts_all_str:
        with open(os.path.join(lua_path, 'contacts_all.lua'), mode='r', encoding='ascii') as fp:
            lua_contacts_all_str = fp.read()
    return lua_contacts_all_str


def get_lua_contact_str():
    """
    获取情报实体调用lua代码
    :return:
    """
    global lua_contact_str
    if not lua_contact_str:
        with open(os.path.join(lua_path, 'contact.lua'), mode='r', encoding='ascii') as fp:
            lua_contact_str = fp.read()
    return lua_contact_str


def get_lua_units_all_str():
    """
    获取本方实体调用lua代码
    :return:
    """
    global lua_units_all_str
    if not lua_units_all_str:
        with open(os.path.join(lua_path, 'units_all.lua'), mode='r', encoding='ascii') as fp:
            lua_units_all_str = fp.read()
    return lua_units_all_str


def get_lua_unit_str():
    """
    获取本方实体调用lua代码
    :return:
    """
    global lua_unit_str
    if not lua_unit_str:
        with open(os.path.join(lua_path, 'unit.lua'), mode='r', encoding='ascii') as fp:
            lua_unit_str = fp.read()
    return lua_unit_str


def get_lua_situation_str():
    """
    获取Lua公共函数, 可为获取所有实体和情报实体
    :return:
    """
    global lua_situation_str
    if not lua_situation_str:
        with open(os.path.join(lua_path, 'situation.lua'), mode='r', encoding='ascii') as fp:
            lua_situation_str = fp.read()
    return lua_situation_str


def get_lua_detect_str():
    """
    获取Lua公共函数, 可为获取探测区域
    :return:
    """
    global lua_detect_str
    if not lua_detect_str:
        with open(os.path.join(lua_path, 'detect.lua'), mode='r', encoding='ascii') as fp:
            lua_detect_str = fp.read()
    return lua_detect_str

def mission_guid_parser(mission_return_str):
    """
    通过创建任务或获取任务返回的字符串，获取任务guid
    :param mission_return_str: 创建任务或获取任务详情返回的字符串,  mission {\r\n guid = 'fdbd661d-2c96-46fb-8e2d-ea0738764604', \r\n name =...
    :return: str, 任务guid
    """
    m_ret = mission_guid_pattern.match(mission_return_str)
    if m_ret is not None:
        guid = m_ret.group(1)
        return guid
    return None


def guid_list_parser(guid_list_str):
    """
    返回的guid列表字符串解析器
    :param guid_list_str: str, 获取的guid列表，例：'{ [1] = \'8cd0c4d5-4d58-408a-99fd-4a75dfa82364\', [2] = \'ef9ac5b8-008a-4042-bbdb-d6bafda6dfb3\' }'
    :return:
    """
    guid_list = []
    for match_guid in guid_list_pattern.finditer(guid_list_str):
        guid_list.append(match_guid.group(1))
    return guid_list


degree_unit = 1/120  # 经纬度划分单元
degree_unit_big = 1/12  # 稀疏区域经度划分单元
MIN_LONGITUDE = 43.5  # 比赛区域最小经度
MAX_LONGITUDE = 50.5  # 比赛区域最大经度
MIN_LATITUDE = 38.5  # 比赛区域最小纬度
MAX_LATITUDE = 42    # 比赛区域最大纬度
MID_LONGITUDE = 48.5  # 比赛区域划为两个区域，左边经度间隔1/120, 右边为单元很少的区域，经度间隔1/12

left_lon_count = round((MID_LONGITUDE - MIN_LONGITUDE) / degree_unit)
lon_unit_count = left_lon_count + round((MAX_LONGITUDE - MID_LONGITUDE) / degree_unit_big)
lat_unit_count = round((MAX_LATITUDE - MIN_LATITUDE) / degree_unit)
ALT_BANDS = [0, 6, 450, 1000, 3000, 7000, 10000]
max_band_index = len(ALT_BANDS) - 1

LAT_DEGREE_DISTANCE = 111.1973  # 每纬度距离
LAT_GRID_UNIT_LENGTH = LAT_DEGREE_DISTANCE*degree_unit  # 每单元格维度距离
LON_GRID_UNIT_LENGTH = math.cos(MIN_LATITUDE*geo.degree2radian)*LAT_GRID_UNIT_LENGTH  # 最大每单元格经度距离
DISTANCE_RANGE = math.sqrt(LAT_GRID_UNIT_LENGTH*LAT_GRID_UNIT_LENGTH + LON_GRID_UNIT_LENGTH*LON_GRID_UNIT_LENGTH)  # 每单元格对角线距离


def get_alt_index(alt):
    """
    获取高度序号值, 高度为真高
    :param alt: float, 高度值，m
    :return: int, 高度序号, 0,1...
    """
    for i in range(max_band_index):
        if ALT_BANDS[i] <= alt < ALT_BANDS[i + 1]:
            return i
    return max_band_index


def get_lon_index(lon):
    """
    获取经度序号值
    :param alt: float, 值
    :return: int, 序号, 0,1...
    """
    if not MIN_LONGITUDE <= lon < MAX_LONGITUDE:
        return None

    if lon < MID_LONGITUDE:
        lon_index = math.floor((lon - MIN_LONGITUDE) / degree_unit)
    else:
        lon_index = left_lon_count + math.floor((lon - MID_LONGITUDE) / degree_unit_big)
    return lon_index


def get_lat_index(lat):
    """
    获取纬度序号值
    :param alt: float, 值
    :return: int, 序号, 0,1...
    """
    if not MIN_LATITUDE <= lat < MAX_LATITUDE:
        return None

    lat_index = math.floor((lat - MIN_LATITUDE) / degree_unit)
    return lat_index


def get_grid_from_index(lat_index, lon_index, alt_index):
    """
    输入纬度编号，经度编号，高度编号，返回格子编号
    :param lat_index: int, 0,1...
    :param lon_index: int, 0,1...
    :param alt_index: int, 0,1...
    :return: int, 0,1...
    """
    return alt_index*1000000 + lat_index*1000 + lon_index


def get_grid(lat, lon, alt):
    """
    输入位置，输出格子编号
    :param lat: float, 纬度
    :param lon: float, 经度
    :param alt: float, 高度
    :return: int,  格子编号, 0,1...
    """
    lon_index = get_lon_index(lon)
    lat_index = get_lat_index(lat)
    alt_band_index = get_alt_index(alt)
    if lon_index is None or lat_index is None or alt_band_index is None:
        return None
    return get_grid_from_index(lat_index, lon_index, alt_band_index)


def get_grid_ex(lat, lon, alt_band_index):
    """
    输入位置，输出格子编号
    :param lat: float, 纬度
    :param lon: float, 经度
    :param alt_band_index: int, 高度层序号
    :return: int,  格子编号
    """
    lon_index = get_lon_index(lon)
    lat_index = get_lat_index(lat)
    if lon_index is None or lat_index is None:
        return None
    return get_grid_from_index(lat_index, lon_index, alt_band_index)


def get_lat(lat_index):
    """
    输入纬度编号，返回纬度
    :param lat_index: int, 0,1...
    :return: float
    """
    if not 0 <= lat_index < lat_unit_count:
        return None
    return MIN_LATITUDE + lat_index*degree_unit + degree_unit / 2


def get_lon(lon_index):
    """
    输入经度编号，返回经度
    :param lon_index: int, 0,1...
    :return: float
    """
    if not 0 <= lon_index < lon_unit_count:
        return None
    if lon_index < left_lon_count:
        lon = MIN_LONGITUDE + lon_index * degree_unit + degree_unit / 2
    else:
        lon = MID_LONGITUDE + (lon_index - left_lon_count) * degree_unit_big + degree_unit_big / 2
    return lon


def get_alt(alt_index):
    """
    输入高度编号，返回高度
    :param alt_index: 高度编号, 0,1...
    :return: float, 高度
    """
    if alt_index < 0 or alt_index > max_band_index:
        return 0
    return ALT_BANDS[alt_index]


def get_all_index_from_position(lat, lon, alt):
    """
    输入纬度经度高度，输出高纬经的编号
    :param lat: float, 纬度
    :param lon: float, 经度
    :param alt: float, 高度
    :return: tuple,  (alt_index, lat_index, lon_index)  格子编号
    """
    lon_index = get_lon_index(lon)
    lat_index = get_lat_index(lat)
    alt_band_index = get_alt_index(alt)
    return alt_band_index, lat_index, lon_index


def get_horizontal_position(lat_index, lon_index):
    """
    输入格子经纬编号，输出水平格子中心位置
    :param lat_index: int, start as 0
    :param lon_index: int, start as 0
    :return:
    """
    return get_lat(lat_index), get_lon(lon_index)


def get_position_from_index(alt_index, lat_index, lon_index):
    """
    输入格子经纬高编号，输出格子中心位置
    :param alt_index: int
    :param lat_index: int
    :param lon_index: int
    :return: tuple, (lat, lon, alt)
    """
    lat = get_lat(lat_index)
    lon = get_lon(lon_index)
    alt = get_alt(alt_index)
    return lat, lon, alt


def get_grid_index(grid_index):
    """
    输入格子编号，输出格子序号值
    :param grid_index: int, 0,1...
    :return: tuple, (alt_index, lat_index, lon_index)
    """    
    if grid_index is None:
        return None

    alt_index = grid_index // 1000000
    lat_index = (grid_index - 1000000*alt_index) // 1000
    lon_index = grid_index % 1000
    
    return (alt_index, lat_index, lon_index)


def get_grid_position(grid_index):
    """
    输入格子编号，输出格子中心位置
    :param grid_index: int
    :return: tuple, (lat, lon, alt)
    """
    alt_index, lat_index, lon_index = get_grid_index(grid_index)
    lat = get_lat(lat_index)
    lon = get_lon(lon_index)
    alt = get_alt(alt_index)
    return lat, lon, alt


def get_grid_length_width(lat_index, lon_index):
    """
    通过经纬度编号，返回格子纬度长，和经度宽
    :param lat_index: int
    :param lon_index: int
    :return: tuple (float, float), 格子纬度长，经度长
    """
    lat = get_lat(lat_index)
    if lon_index >= left_lon_count:
        width = LAT_DEGREE_DISTANCE * degree_unit_big * math.cos(geo.degree2radian*lat)
    else:
        width = LAT_DEGREE_DISTANCE * degree_unit * math.cos(geo.degree2radian * lat)
    return LAT_DEGREE_DISTANCE*degree_unit, width


CENTER_LAT_INDEX = lat_unit_count // 2
CENTER_LON_INDEX = left_lon_count // 2
CENTER_POSITION = (get_lat(CENTER_LAT_INDEX), get_lon(CENTER_LON_INDEX))
MAX_HALF_DISTANCE = geo.get_horizontal_distance(CENTER_POSITION, (get_lat(0), get_lon(CENTER_LON_INDEX)))


def set_degree_unit(set_unit):
    global degree_unit, left_lon_count, lon_unit_count, lat_unit_count, LAT_GRID_UNIT_LENGTH
    global CENTER_LAT_INDEX, CENTER_LON_INDEX, CENTER_POSITION, MAX_HALF_DISTANCE
    degree_unit = set_unit
    left_lon_count = round((MID_LONGITUDE - MIN_LONGITUDE) / degree_unit)
    lon_unit_count = left_lon_count + round((MAX_LONGITUDE - MID_LONGITUDE) / degree_unit_big)
    lat_unit_count = round((MAX_LATITUDE - MIN_LATITUDE) / degree_unit)
    LAT_GRID_UNIT_LENGTH = LAT_DEGREE_DISTANCE * degree_unit  # 每单元格维度距离

    CENTER_LAT_INDEX = lat_unit_count // 2
    CENTER_LON_INDEX = left_lon_count // 2
    CENTER_POSITION = (get_lat(CENTER_LAT_INDEX), get_lon(CENTER_LON_INDEX))
    MAX_HALF_DISTANCE = geo.get_horizontal_distance(CENTER_POSITION, (get_lat(0), get_lon(CENTER_LON_INDEX)))


def get_grid_index_from_distance2(location, distance_km):
    """
    返回某位置一定距离的格子序号列表
    :param location: tuple, (lat, lon)
    :param distance_km: float, km
    :return: list,   example: [24001, 240444]
    """
    index_list = []
    in_area, (min_lat_index, min_lon_index) = get_grid_from_distance2(location, distance_km, True)
    lat_valid_count, lon_valid_count = in_area.shape
    for i in range(lat_valid_count):
        one_array = np.where(in_area[i])[0]
        if one_array.size > 0:
            for j in one_array:
                grid_index = 1000*(i + min_lat_index) + j + min_lon_index
                index_list.append(grid_index)
    return index_list


cache_area_dict = {}


def get_grid_from_distance2(location, distance_km, subarray_ret=False):
    """
    获取某位置附近距离所有格子, 2维
    :param location: tuple, (lat, lon)
    :param distance_km: float, km
    :return: numpy.array
    """
    global cache_area_dict
    cal_dis = round(distance_km, 1)
    if cal_dis <= 0:
        return None, (0, 0)
    elif cal_dis >= MAX_HALF_DISTANCE:
        return calculate_area_from_distance(location, distance_km, subarray_ret)
    else:
        if cal_dis in cache_area_dict:
            in_area, (min_lat_index, min_lon_index) = cache_area_dict[cal_dis]
        else:
            in_area, (min_lat_index, min_lon_index) = calculate_area_from_distance(CENTER_POSITION, cal_dis, True)
        cache_area_dict[cal_dis] = in_area, (min_lat_index, min_lon_index)
        lat_index = get_lat_index(location[0])
        lon_index = get_lon_index(location[1])
        lat_delta = lat_index - CENTER_LAT_INDEX
        lon_delta = lon_index - CENTER_LON_INDEX
        new_lat_index = min_lat_index + lat_delta
        new_lon_index = min_lon_index + lon_delta
        if 0 <= new_lat_index < lat_unit_count - in_area.shape[0] \
                and 0 <= new_lon_index < left_lon_count - in_area.shape[1]:
            new_in_area = in_area
        else:
            if new_lat_index < 0:
                left_lat_index = 0 - new_lat_index
                end_lat_index = in_area.shape[0]
                new_lat_index = 0
            elif new_lat_index + in_area.shape[0] >= lat_unit_count:
                left_lat_index = 0
                end_lat_index = in_area.shape[0] - (new_lat_index + in_area.shape[0] - lat_unit_count)
            else:
                left_lat_index = 0
                end_lat_index = in_area.shape[0]
            if new_lon_index < 0:
                left_lon_index = 0 - new_lon_index
                end_lon_index = in_area.shape[1]
                new_lon_index = 0
            elif new_lon_index + in_area.shape[1] >= left_lon_count:
                left_lon_index = 0
                end_lon_index = in_area.shape[1] - (new_lon_index + in_area.shape[1] - left_lon_count)
            else:
                left_lon_index = 0
                end_lon_index = in_area.shape[1]
            new_in_area = in_area[left_lat_index:end_lat_index, left_lon_index:end_lon_index]
        if subarray_ret:
            return new_in_area, (new_lat_index, new_lon_index)
        else:
            all_area = np.zeros((lat_unit_count, lon_unit_count), dtype=np.int8)
            all_area[new_lat_index: new_lat_index + new_in_area.shape[0], new_lon_index: new_lon_index + new_in_area.shape[1]] = new_in_area
            return all_area


def calculate_area_from_distance(location, distance_km, subarray_ret=False):
    """
    计算某位置附近距离所有格子, 2维
    :param location: tuple, (lat, lon)
    :param distance_km: float, km
    :return: numpy.array
    """
    air_lat_index = get_lat_index(location[0])
    air_lon_index = get_lon_index(location[1])
    lon_degree_dis = LAT_DEGREE_DISTANCE * math.cos(location[0] * geo.degree2radian)
    min_lon = max(MIN_LONGITUDE, location[1] - distance_km / lon_degree_dis)
    max_lon = min(MAX_LONGITUDE - 1E-4, location[1] + distance_km / lon_degree_dis)
    min_lat = max(MIN_LATITUDE, location[0] - distance_km / LAT_DEGREE_DISTANCE)
    max_lat = min(MAX_LATITUDE - 1E-4, location[0] + distance_km / LAT_DEGREE_DISTANCE)
    min_lat_index = get_lat_index(min_lat)
    max_lat_index = get_lat_index(max_lat)
    min_lon_index = get_lon_index(min_lon)
    max_lon_index = get_lon_index(max_lon)
    lat_valid_count = max_lat_index - min_lat_index + 1
    lon_valid_count = max_lon_index - min_lon_index + 1
    in_area = np.zeros((lat_valid_count, lon_valid_count), dtype=np.int8)
    max_axis_unit_count = max(lat_valid_count, lon_valid_count)
    if max_axis_unit_count < 11:
        lon_degree_unit_dis = lon_degree_dis * degree_unit
        delta_lat = math.floor(distance_km / LAT_GRID_UNIT_LENGTH / math.sqrt(2)) - 1
        delta_lon = math.floor(distance_km / lon_degree_unit_dis / math.sqrt(2)) - 1
        valid_min_lat = max(air_lat_index - delta_lat, min_lat_index) - min_lat_index
        valid_min_lon = max(air_lon_index - delta_lon, min_lon_index) - min_lon_index
        valid_max_lat = min(air_lat_index + delta_lat, max_lat_index) - min_lat_index + 1
        valid_max_lon = min(air_lon_index + delta_lon, max_lon_index) - min_lon_index + 1
        in_area[valid_min_lat:valid_max_lat, valid_min_lon:valid_max_lon] = 1
        for lat_index in range(min_lat_index, max_lat_index + 1):
            for lon_index in range(min_lon_index, max_lon_index + 1):
                if not (air_lat_index - delta_lat <= lat_index <= air_lat_index + delta_lat and
                        air_lon_index - delta_lon <= lon_index <= air_lon_index + delta_lon):
                    h_dis = geo.get_horizontal_distance(location, get_horizontal_position(lat_index, lon_index))
                    if h_dis < distance_km:
                        in_area[lat_index - min_lat_index][lon_index - min_lon_index] = 1
    elif max_axis_unit_count < 56:
        lon_grid_len_up = math.cos((location[0] + 1 / 60) * geo.degree2radian) * LAT_GRID_UNIT_LENGTH  # 每单元格经度距离 高纬度
        lon_grid_len_down = math.cos((location[0] - 1 / 60) * geo.degree2radian) * LAT_GRID_UNIT_LENGTH  # 每单元格经度距离 低纬度
        lon_grid_len_up *= lon_grid_len_up
        lon_grid_len_down *= lon_grid_len_down
        lon_all_count = math.floor(distance_km / lon_degree_dis / degree_unit)
        air_lat_index_array = air_lat_index - min_lat_index
        air_lon_index_array = air_lon_index - min_lon_index
        for i in range(1, lon_all_count):
            lon_delta = i - 1  # 经度格子变化数量
            lat_count_up = math.floor(
                math.sqrt(distance_km * distance_km - i * i * lon_grid_len_up) / LAT_GRID_UNIT_LENGTH) - 1
            lat_count_down = math.floor(
                math.sqrt(distance_km * distance_km - i * i * lon_grid_len_down) / LAT_GRID_UNIT_LENGTH) - 1
            r1 = max(0, air_lat_index_array - lat_count_down)
            r2 = min(lat_valid_count, air_lat_index_array + lat_count_up + 1)
            c1 = max(0, air_lon_index_array - lon_delta)
            c2 = min(lon_valid_count, air_lon_index_array + lon_delta + 1)
            in_area[r1:r2, c1:c2] = 1
        # 剩余的格子，判断距离，打1
        check_count2 = 0
        for lat_index in range(min_lat_index, max_lat_index + 1):
            have_in = False
            for lon_index in range(min_lon_index, max_lon_index + 1):
                if in_area[lat_index - min_lat_index][lon_index - min_lon_index] != 1:
                    check_count2 += 1
                    h_dis = geo.get_horizontal_distance(location, get_horizontal_position(lat_index, lon_index))
                    if h_dis < distance_km:
                        have_in = True
                        in_area[lat_index - min_lat_index][lon_index - min_lon_index] = 1
                    else:
                        if have_in:
                            break
    else:
        # start = datetime.now()
        in_area = np.zeros((lat_valid_count, lon_valid_count), dtype=np.int8)
        lon_grid_len_up = math.cos((location[0] + 1 / 60) * geo.degree2radian) * LAT_GRID_UNIT_LENGTH  # 每单元格经度距离 高纬度
        lon_grid_len_down = math.cos((location[0] - 1 / 60) * geo.degree2radian) * LAT_GRID_UNIT_LENGTH  # 每单元格经度距离 低纬度
        lon_grid_len_up *= lon_grid_len_up
        lon_grid_len_down *= lon_grid_len_down
        lon_all_count = math.floor(distance_km / lon_degree_dis / degree_unit)
        air_lat_index_array = air_lat_index - min_lat_index
        air_lon_index_array = air_lon_index - min_lon_index
        for i in range(1, lon_all_count):
            lon_delta = i - 1  # 经度格子变化数量
            lat_count_up = math.floor(
                math.sqrt(distance_km * distance_km - i * i * lon_grid_len_up) / LAT_GRID_UNIT_LENGTH) - 1
            lat_count_down = math.floor(
                math.sqrt(distance_km * distance_km - i * i * lon_grid_len_down) / LAT_GRID_UNIT_LENGTH) - 1
            r1 = max(0, air_lat_index_array - lat_count_down)
            c1 = max(0, air_lon_index_array - lon_delta)
            r2 = min(lat_valid_count, air_lat_index_array + lat_count_up + 1)
            c2 = min(lon_valid_count, air_lon_index_array + lon_delta + 1)
            in_area[r1:r2, c1:c2] = 1

        for r in [0, 1, 3, lat_valid_count - 3, lat_valid_count - 2, lat_valid_count - 1]:
            h_dis = geo.get_horizontal_distance(location, get_horizontal_position(r + min_lat_index, air_lon_index))
            if h_dis < distance_km:
                in_area[r][air_lon_index_array] = 1

        for r in range(lat_valid_count):
            one_array = np.where(in_area[r])[0]
            if one_array.size > 0:
                if r == 0:
                    check_more_count = 10
                elif r < 5:
                    check_more_count = 20
                elif r < 13:
                    check_more_count = 8
                elif r < 20 or lat_valid_count - r < 15:
                    check_more_count = 5
                else:
                    check_more_count = 3
                left_check = max(0, one_array[0] - check_more_count)
                right_check = min(lon_valid_count, one_array[-1] + check_more_count)
                for i in range(left_check, one_array[0]):
                    h_dis = geo.get_horizontal_distance(location,
                                                        get_horizontal_position(r + min_lat_index, i + min_lon_index))
                    if h_dis < distance_km:
                        in_area[r][i] = 1
                for i in range(one_array[-1] + 1, right_check):
                    h_dis = geo.get_horizontal_distance(location,
                                                        get_horizontal_position(r + min_lat_index, i + min_lon_index))
                    if h_dis < distance_km:
                        in_area[r][i] = 1

        # end_t = datetime.now()
        # print('time elapsed:%.5lf' % (end_t - start).total_seconds())
        # start = end_t
        #
        # check_area = np.zeros((lat_valid_count, lon_valid_count), dtype=np.int8)
        # for lat_index in range(min_lat_index, max_lat_index + 1):
        #     for lon_index in range(min_lon_index, max_lon_index + 1):
        #         h_dis = geo.get_horizontal_distance(location, get_horizontal_position(lat_index, lon_index))
        #         if h_dis < distance_km:
        #             check_area[lat_index - min_lat_index][lon_index - min_lon_index] = 1
        #
        # end_t = datetime.now()
        # print('stand time elapsed:%.5lf' % (end_t - start).total_seconds())
        # start = end_t
        #
        # span_area = check_area - in_area
        # print('cal more count than stand:%d' % np.sum(span_area == -1))
        # print('cal less count:%d' % np.sum(span_area == 1))
        # print('all size:%d' % in_area.size)

    if subarray_ret:
        return in_area, (min_lat_index, min_lon_index)
    else:
        all_area = np.zeros((lat_unit_count, lon_unit_count), dtype=np.int8)
        all_area[min_lat_index: max_lat_index + 1, min_lon_index: max_lon_index + 1] = in_area
        return all_area


def get_grid_index_from_rect(lat_t, lat_b, lon_l, lon_r, alt):
    """
     获取给定高度、矩形区域内的格子编号集
    :param lat_t: float, 最大纬度
    :param lat_b: float, 最小经度
    :param lon_l: float, 最小纬度
    :param lon_r: float, 最大经度
    :param alt: float, 高度
    :return: list(int),  格子编号集
    """
    
    set_grid = set()
    
    lon_loop = lon_l
    while lon_loop < lon_r:
        lat_loop = lat_b
        while lat_loop < lat_t:
            grid_index = get_grid(lat_loop, lon_loop, alt)
            set_grid.add(grid_index)
            
            lat_loop += degree_unit
            
        lon_loop += degree_unit 

    return list(set_grid)


# def get_grid_index_from_distance_2d(lat, lon, alt, distance_m):
#     """
#      获取给定原点、半径的格子编号集 2维平面
#     :param lat: float, 纬度
#     :param lon: float, 经度
#     :param alt: float, 高度
#     :param distance: float, 距离, 米
#     :return: list(int),  格子编号集
#     """
#
#     '''数据有效性检查'''
#     if abs(distance_m) < 0.000001:
#         return []
#
#     '''获取圆外切矩形经纬度'''
#     (lat_t, lon_t) = geo.get_geopoint_from_distance((lat, lon), 0, distance_m)
#     (lat_r, lon_r) = geo.get_geopoint_from_distance((lat, lon), 90, distance_m)
#     (lat_b, lon_b) = geo.get_geopoint_from_distance((lat, lon), 180, distance_m)
#     (lat_l, lon_l) = geo.get_geopoint_from_distance((lat, lon), 270, distance_m)
#     lon_l = max(lon_l, MIN_LONGITUDE)
#     lon_r = min(lon_r, MAX_LONGITUDE)
#     lat_t = min(lat_t, MAX_LATITUDE)
#     lat_b = max(lat_b, MIN_LATITUDE)
#
#     list_grid= set()
#
#     lon_loop = lon_l
#     while lon_loop < lon_r:
#         lat_loop = lat_b
#         while lat_loop < lat_t:
#             grid_index = get_grid(lat_loop, lon_loop, alt)
#             dis_point = geo.get_slant_distance((lat, lon, alt), get_grid_position(grid_index))/1000.0
#             if dis_point < distance_m:
#                 list_grid.add(grid_index)
#             lat_loop += degree_unit
#         lon_loop += degree_unit
#
#     return list(list_grid)

def get_grid_index_from_hitdistance_3d(lat, lon, alt, distance_min, distance_max):
    """
     获取给定原点、半径的格子编号集 3维立体
    :param lat: float, 纬度
    :param lon: float, 经度
    :param alt: float, 高度
    :param distance_min: float, 最小距离, 米
    :param distance_max: float, 最大距离, 米
    :return: list(list(bytearray(int))),  格子编号集
    """

    '''数据有效性检查'''
    if abs(distance_max) < 0.000001:
        return []
    """
    lon_ncount = distance_max/3445
    lat_ncount = distance_max/4638.5
    lon_l = max(lon-lon_ncount*degree_unit, MIN_LONGITUDE)
    lon_r = min(lon+lon_ncount*degree_unit, MAX_LONGITUDE)
    lat_t = min(lat+lat_ncount*degree_unit, MAX_LATITUDE)
    lat_b = max(lat-lat_ncount*degree_unit, MIN_LATITUDE)
    """
    
    (lat_t, lon_t) = geo.get_geopoint_from_distance((lat, lon), 0, distance_max)
    (lat_r, lon_r) = geo.get_geopoint_from_distance((lat, lon), 90, distance_max)
    (lat_b, lon_b) = geo.get_geopoint_from_distance((lat, lon), 180, distance_max)
    (lat_l, lon_l) = geo.get_geopoint_from_distance((lat, lon), 270, distance_max)
    lon_l = max(lon_l, MIN_LONGITUDE)
    lon_r = min(lon_r, MAX_LONGITUDE)
    lat_t = min(lat_t, MAX_LATITUDE)
    lat_b = max(lat_b, MIN_LATITUDE)    

    list_grid=[]
    
    grid_index = get_grid_ex(lat_b, lon_l, 0)
    for alt_loop in ALT_BANDS:
        list_grid_level=[]
        index_lat = 0
        lat_loop = MIN_LATITUDE        
        while lat_loop+degree_unit < MAX_LATITUDE:
            index_lon = 0            
            list_lon=bytearray(int(lon_unit_count))
            if (abs(alt_loop-alt)<distance_max and lat_loop >= lat_b and lat_loop <= lat_t):
                lon_loop = MIN_LONGITUDE
                
                b_i = 0
                while lon_loop+degree_unit_big < MAX_LONGITUDE:
                    if (lon_loop >= lon_l and lon_loop <= lon_r):
                        #grid_index = int(index_h*1000000 + (((grid_index%1000000)/1000)+index_lat)*1000 + index_lon)
                        list_lon[index_lon] = 1
                    
                    index_lon += 1
                    if (lon_loop < MID_LONGITUDE):
                        lon_loop += degree_unit
                    else:
                        lon_loop += degree_unit_big
            index_lat += 1
            lat_loop += degree_unit
            list_grid_level.append(list_lon)
        list_grid.append(list_grid_level)
        
    return list_grid


def get_grid_index_area():
    """
     获取作战区域内所有格子编号
    :return: list(int),  格子编号集
    """
    
    list_grid=[]
    for alt in ALT_BANDS:
        list_grid += get_grid_index_from_rect(MAX_LATITUDE, MIN_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE, alt)
    return list_grid


def save_python_file(filename, filedata):
    """
    保存文件
    :param filename: 文件名
    :param filedata: 文件数据
    :return: 成功与否
    """    
    dictfile = open(filename, 'wb')
    if dictfile:
        pickle.dump(filedata, dictfile)
        dictfile.close()
        return True
    else:
        return False

def load_python_file(filename):
    """
    加载文件
    :return:文件数据, Python类型
    """
    filedata = None
    dictfile = open(filename, 'rb')
    if dictfile:
        filedata = pickle.load(dictfile)
        dictfile.close()
        
    return filedata

def np3_to_np1(np_3):
    """
    三维0/1数组转换成1维uint8的数组
    :param np_3: 三维0/1数组
    :return: 1维uint8的数组
    """       
    if np_3 is None:
        return None
    num = np_3.size//8
    if np_3.size%8 > 0:
        num += 1
    np_1 = np.zeros(num, dtype=np.uint8)

    (alt_num, lat_num, lon_num) = np_3.shape
    for x in range(alt_num):
        for y in range(lat_num):
            for z in range(lon_num):
                if np_3[x][y][z] > 0:
                    n_num = x*lat_num*lon_num + y*lon_num + z
                    index = n_num//8
                    bit = n_num%8
                    np_1[index] = np_1[index] | (pow(2, bit))

    return np_1

def np1_to_np3(np_1, shape):
    """
    1维uint8的数组转换成三维0/1数组
    :param np_1: 1维uint8的数组
    :param shape: tuple(num1, num2, num3)三维数组形状
    :return: 三维0/1数组
    """
    if np_1 is None or shape is None:
        return None
    
    (alt_num, lat_num, lon_num) = shape
    
    if np_1.size*8 < alt_num*lat_num*lon_num:
        return None
    
    np_3 = np.zeros((alt_num, lat_num, lon_num), dtype=np.uint8)
    for x in range(alt_num):
        for y in range(lat_num):
            for z in range(lon_num):
                n_num = x*lat_num*lon_num + y*lon_num + z
                index = n_num//8
                bit = n_num%8
                np_3[x][y][z] = (np_1[index] >> bit) & 1
    
    
    return np_3


def get_scenario_time(time_stamp):
    """
    获取当前想定时间，字符串格式
    :param time_stamp:
    :return:
    """
    current = ZERO_TIME + timedelta(seconds=(time_stamp + 28800))
    return current.strftime("%Y/%m/%d %H:%M:%S")


def get_sides(situation_str):
    """
    返回推演方 guid和推演方明
    :param situation_str:
    :return:
    """
    guid2name = {}
    side_pat = re.compile(r'{"ClassName":"CSide","strName":"([^,]+)","strGuid":"([a-z0-9-]+)')
    for re_ret in side_pat.findall(situation_str):
        guid2name[re_ret[1]] = re_ret[0]
    return guid2name


def parse_weapons_record(weapon_ratio):
    """
    返回武器的精简信息，适用于挂架，挂载，弹药库的武器解析
    :return:
    """
    info = []
    weapon_name_type = {}
    w_set = set()
    if '@' in weapon_ratio:
        load_ratios = weapon_ratio.split('@')
        for record in load_ratios:
            record_v = record.split('$')
            w_id = int(record_v[1])
            info.append({
                "wpn_guid": record_v[0],
                "wpn_dbid": w_id,
                "wpn_current": int(record_v[2]),
                "wpn_maxcap": int(record_v[3])
            })
            w_set.add(w_id)
    else:
        if '$' in weapon_ratio:
            record_v = weapon_ratio.split('$')
            w_id = int(record_v[1])
            info.append({
                "wpn_guid": record_v[0],
                "wpn_dbid": w_id,
                "wpn_current": int(record_v[2]),
                "wpn_maxcap": int(record_v[3])
            })
            w_set.add(w_id)
    if info:
        for wid in w_set:
            weapon_name_type[wid] = db.get_weapon_name_type(wid)
        for w_info in info:
            name_type = weapon_name_type[w_info["wpn_dbid"]]
            w_info["wpn_name"] = name_type[0]
            w_info["wpn_type"] = name_type[1]
    return info


# 设置武器使用规则
UNIT_WEAPON_ITEMS = {}
SIDE_WEAPON_ITEMS ={}

