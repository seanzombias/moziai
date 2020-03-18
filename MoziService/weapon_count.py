#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : weapon_count.py
# Create date : 2019-12-06 13:57
# Modified date : 2020-01-09 18:36
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pylog
from MoziService.paser_func import get_side_dic
from MoziService.paser_core import get_care_class_units_from_side

def get_unit_mounts_lt(item):
    mounts_str = item.get("m_Mounts", "")
    mounts_lt = []
    if mounts_str:
        #pylog.info(mounts_str)
        mounts_lt = mounts_str.split("@")
    return mounts_lt

def get_unit_loadout(item, all_info_dict):
    loadout_guid = item.get("m_LoadoutGuid", "")

    loadout_item = None
    if loadout_guid:
        #pylog.info(loadout_guid)
        loadout_item = all_info_dict[loadout_guid]
    #else:
    #    pylog.info("do not have m_LoadoutGuid")
    return loadout_item

def get_weapon_remain_dic(side_guid, all_info_dict):
    units_dic = get_care_class_units_from_side(side_guid, all_info_dict)
    #pylog.info(len(units_dic))
    weapon_dic = {}
    for key in units_dic:
        item = units_dic[key]
        #show_item_info(item)
        #mozi_unit.show_mozi_unit(item)
        mount_lt = get_unit_mounts_lt(item)
        for guid in mount_lt:
            mount_item = all_info_dict[guid]
            weapon_dic[guid] = mount_item

        loadout_item = get_unit_loadout(item, all_info_dict)
        if loadout_item:
            weapon_dic[loadout_item["strGuid"]] = loadout_item

    weapon_remain_dic = create_weapon_remain_dic(weapon_dic)
    pylog.info(weapon_remain_dic)
    raise

def create_weapon_remain_dic(weapon_dic):
    weapon_remain_dic = {}
    for guid in weapon_dic:
        item = weapon_dic[guid]
        #pylog.info(item)
        iDBID = item.get("iDBID")
        ret = weapon_remain_dic.get(iDBID)
        if ret:
            ret["current"] += int(item.get("strLoadWeaponCount").strip()[1:-1].split("/")[0])
        else:
            dic = {}
            dic["current"] = int(item.get("strLoadWeaponCount").strip()[1:-1].split("/")[0])

            weapon_remain_dic[iDBID] = dic

    return weapon_remain_dic

def get_weapon_remain(all_info_dict):
    side_dic = get_side_dic(all_info_dict)
    for guid in side_dic:
        get_weapon_remain_dic(guid, all_info_dict)

