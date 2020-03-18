#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : paser_core.py
# Create date : 2019-12-05 13:56
# Modified date : 2020-01-09 03:14
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pylog
from MoziService.paser_func import get_class_dic
from MoziService.paser_func import get_side_dic
from MoziService.paser_func import get_a_side_dic
from MoziService.paser_func import get_unit_side_name
from MoziService.paser_func import get_a_side_units_dic

from MoziService.paser_show import show_class_info
from MoziService.paser_show import show_item_info


# 获得所有方的字典
def get_all_sides_dic(all_info_dict):
    """获得所有方的字典"""
    side_dic = get_side_dic(all_info_dict)
    return side_dic


# 通过方名字或者方的guid
def get_side_guid_from_side_name(side_name, all_info_dict):
    """通过方的名字获得方的guid"""
    side_dic = get_side_dic(all_info_dict)
    for side_guid in side_dic:
        if side_dic[side_guid]["strName"] == side_name:
            return side_guid


# 获取方的所有种类单元的字典
def get_all_units_from_side(side_guid, all_info_dict):
    a_side_dic = get_a_side_dic(side_guid, all_info_dict)
    return a_side_dic


# 获得所有关心种类的单元的字典
def get_care_class_units_from_side(side_guid, all_info_dict):
    a_side_dic = get_all_units_from_side(side_guid, all_info_dict)
    a_side_class_dic = get_class_dic(a_side_dic)
    units_dic = get_a_side_units_dic(a_side_class_dic)
    return units_dic


# 获取方的感知单元的字典
def get_contacts_from_side(side_guid, all_info_dict):
    return get_units_from_side(side_guid, "CContact", all_info_dict)


# 获得方的某一类单元的字典
def get_units_from_side(side_guid, class_name, all_info_dict):
    a_side_dic = get_a_side_dic(side_guid, all_info_dict)
    # pylog.info(len(a_side_dic))
    a_side_class_dic = get_class_dic(a_side_dic)
    # show_class_info(a_side_class_dic)
    dic = a_side_class_dic.get(class_name)
    return dic


# 获取某一个单元的字典
def get_a_unit(guid, all_info_dict):
    unit = all_info_dict[guid]
    return unit


# 获取感知单元真实guid
def get_contact_actual_guid(contact_guid, all_info_dict):
    item = all_info_dict[contact_guid]
    # pylog.info(item)
    actual_guid = item["m_ActualUnit"]
    # pylog.info("actual guid:%s" % actual_guid)
    return actual_guid


# 获取感知单元真实单元字典
def get_contact_actual_unit_dic(contact_guid, all_info_dict):
    guid = get_contact_actual_guid(contact_guid, all_info_dict)
    actual_unit_dic = all_info_dict[guid]
    return actual_unit_dic


# 获取感知单元真实名字
def get_contact_actual_name(contact_guid, all_info_dict):
    unit_dic = get_contact_actual_unit_dic(contact_guid, all_info_dict)
    name = unit_dic["strName"]
    return name


# 从guid获得名字
def get_guid_from_name(search_name, all_info_dict):
    for guid in all_info_dict:
        item = all_info_dict[guid]
        name = item.get("strName", "")
        class_name = item["ClassName"]
        if class_name != "CContact":
            if name == search_name:
                return guid
    return False


# 检查是否存在目标
def check_is_exist_target(target_name, all_info_dict):
    ret = get_guid_from_name(target_name, all_info_dict)
    if ret:
        return True
    return False


# 获得目标感知guid 从目标名字
def get_target_contact_guid_from_target_name(side_name, target_name, all_info_dict):
    side_guid = get_side_guid_from_side_name(side_name, all_info_dict)
    red_contacts = get_units_from_side(side_guid, "CContact", all_info_dict)
    if red_contacts:
        for guid in red_contacts:
            name = get_contact_actual_name(guid, all_info_dict)
            # pylog.info(name)
            if name == target_name:
                # pylog.info(red_contacts[guid])
                return guid
    return False
