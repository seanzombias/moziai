#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : paser_func.py
# Create date : 2019-12-06 11:57
# Modified date : 2020-01-09 18:30
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
import pylog

def fill_str_guid(info_dic):
    for key in info_dic:
        #pylog.info(key)
        item = info_dic[key]
        item["strGuid"] = key

def add_item_to_dic(dic, item, key):
    ret = dic.get(item[key])

    if ret:
        if 'strGuid' in item:
            ret[item["strGuid"]] = item
    else:
        if 'strGuid' in item:
            item_dic = {}
            item_dic[item["strGuid"]] = item
            dic[item[key]] = item_dic

#按照类别分出一个字典
def get_class_dic(info_dic):
    '''按照类别分出一个字典'''
    dic = {}
    for key in info_dic:
        #pylog.info(key)
        item = info_dic[key]
        #pylog.info(item)
        add_item_to_dic(dic, item, "ClassName")
    return dic

#从态势数据中获得包含所有方的字典
def get_side_dic(all_info_dict):
    class_dic = get_class_dic(all_info_dict)
    #show_class_info(class_dic)
    side_dic = class_dic["CSide"]
    return side_dic

#获得一方所有态势的字典
def get_a_side_dic(side_guid, info_dic):
    dic = {}
    for key in info_dic:
        #pylog.info(key)
        item = info_dic[key]
        if item["ClassName"] != "CContact":
            m_Side = item.get("m_Side")
        else:
            m_Side = item.get("m_OriginalDetectorSide")

        if m_Side and m_Side == side_guid:
            dic[key] = item
    #pylog.info(dic)
    return dic

#获得一方所有单元的字典
def get_a_side_units_dic(a_side_class_dic, class_lt=["CFacility","CAircraft"]):
    dic = {}
    for key in a_side_class_dic:
        #pylog.info("side class:%s" % key)
        if key in class_lt:
            #pylog.info(a_side_class_dic[key])
            #pylog.info("should and to units dic")
            class_dic = a_side_class_dic[key]
            for guid in class_dic:
                item = class_dic[guid]
                #show_item_info(item)
                dic[guid] = item

    #pylog.info("side unit count:%s" % len(dic))
    return dic

#获得单元的方的名称
def get_unit_side_name(unit_dic, all_info_dict):
    side_unit = all_info_dict[unit_dic["m_Side"]]
    return side_unit["strName"]
