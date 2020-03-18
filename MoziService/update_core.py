#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : update_core.py
# Create date : 2019-12-06 19:59
# Modified date : 2020-01-09 18:35
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pylog
from MoziService.paser_func import get_class_dic
from MoziService.paser_show import show_class_info

def delete_situation_item(guid, all_info_dict):
    ret = all_info_dict.pop(guid,"")
    return ret

def try_add_situation_item(guid, item, all_info_dict):
    old_item = all_info_dict.get(guid, "")
    if not old_item:
        all_info_dict[guid] = item

def try_change_situation_item(guid, item, all_info_dict):
    old_item = all_info_dict.get(guid, "")
    if old_item:
        for key in item:
            old_value = old_item.get(key, "")
            if old_value != item[key]:
                old_item[key] = item[key]

def just_update_situation(update_situation_data, all_info_dict):
    class_dic = get_class_dic(update_situation_data)
    for class_name in class_dic:
        a_class_dic = class_dic[class_name]
        for guid in a_class_dic:
            if class_name != "Delete":
                item = a_class_dic[guid]
                try_change_situation_item(guid, item, all_info_dict)
                try_add_situation_item(guid, item, all_info_dict)
            else:
                delete_situation_item(guid, all_info_dict)

#更新态势测试函数 输出计数统计
def update_situation_count(update_situation_data, all_info_dict):
    class_dic = get_class_dic(update_situation_data)
    #show_class_info(class_dic)
    #增加
    #修改
    same_count = 0
    diff_count = 0
    do_not_exist_count = 0
    add_item = 0
    delete_item_count = 0
    null_delete_count = 0
    delete_aircraft_count = 0
    for class_name in class_dic:
        a_class_dic = class_dic[class_name]
        for guid in a_class_dic:
            if class_name != "Delete":
                old_item = all_info_dict.get(guid, "")
                item = a_class_dic[guid]
                if old_item:
                    for key in item:
                        old_value = old_item.get(key, "")
                        if old_value != item[key]:
                            if old_value:
                                #pylog.info("old_item key:%s value:%s" % (key, old_value))
                                pass
                            else:
                                #pylog.info("old_item key:%s value:do not exist" % (key))
                                do_not_exist_count += 1
                            old_item[key] = item[key]
                            diff_count += 1
                        else:
                            if key != "ClassName" and key != "strGuid" and key != "strName":
                                same_count += 1
                else:
                    #pylog.info("add item:%s" % item)
                    all_info_dict[guid] = item
                    add_item += 1
            else:
                #删除
                ret = all_info_dict.pop(guid,"")
                if ret:
                    delete_item_count += 1
                    if ret["ClassName"] == "CAircraft":
                        pylog.info("delete a aircraft")
                        delete_aircraft_count += 1
                else:
                    null_delete_count += 1

    #pylog.info("sum:%s same:%s diff:%s do not exist:%s add item:%s delete item:%s null delete:%s delete aircraft:%s" % (same_count + diff_count, same_count, diff_count, do_not_exist_count, add_item, delete_item_count, null_delete_count, delete_aircraft_count))

