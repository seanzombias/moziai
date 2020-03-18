#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : situation_paser.py
# Create date : 2019-12-05 13:56
# Modified date : 2020-01-12 22:46
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pylog
from MoziService import mozi_unit

from MoziService.paser_func import fill_str_guid
from MoziService.paser_func import get_class_dic

from MoziService.paser_core import get_all_units_from_side
from MoziService.paser_core import get_all_sides_dic
from MoziService.paser_core import get_units_from_side
from MoziService.paser_core import get_contact_actual_unit_dic
from MoziService.paser_core import get_unit_side_name
from MoziService.paser_core import get_contacts_from_side

from MoziService.weapon_count import get_weapon_remain
from MoziService.paser_show import show_class_info
from MoziService.paser_show import show_item_info

from MoziService.update_core import just_update_situation
from MoziService.update_core import update_situation_count

from MoziService.entitys.aircraft import CAircraft
from MoziService.entitys.facility import CFacility


def set_element_info(element_obj, info_dict):
    for item, value in info_dict.items():
        element_obj.__setattr__(item, value)


def get_aircraft_obj(guid, item, side_name, mozi_task):
    plane = CAircraft()
    plane.strGuid =guid
    plane.strName = item["strName"]
    plane.side_name = side_name
    plane.mozi_server = mozi_task
    set_element_info(plane, item)
    return plane


def get_facility_obj(guid, item, side_name, mozi_task):
    f = CFacility(guid, item["strName"], side_name, mozi_task)
    f.strGuid = guid
    f.strName = item["strName"]
    f.side_name = side_name
    f.mozi_server = mozi_task
    # pylog.info(f)
    set_element_info(f, item)
    return f


def get_entity_from_guid(guid, all_info_dict, mozi_task):
    # pylog.info(guid)
    item = all_info_dict.get(guid, False)
    if item:
        if item["ClassName"] == "CAircraft":
            plane = get_aircraft_obj(guid, item, "红方", mozi_task)
            #       summary_info = plane.get_summary_info()
            #       pylog.info(summary_info)
            return plane

        if item["ClassName"] == "CFacility":
            facility = get_facility_obj(guid, item, "红方", mozi_task)
            return facility
    return item


def paser_situation(all_info_dict):
    fill_str_guid(all_info_dict)


def update_situation(update_situation_data, all_info_dict):
    fill_str_guid(update_situation_data)
    update_situation_count(update_situation_data, all_info_dict)
    # just_update_situation(update_situation_data, all_info_dict)


def paser_interface_test(all_info_dict):
    side_dic = get_all_sides_dic(all_info_dict)
    for side_guid in side_dic:
        # pylog.info(side_guid)
        a_side_dic = get_all_units_from_side(side_guid, all_info_dict)
        a_side_class_dic = get_class_dic(a_side_dic)
        # show_class_info(a_side_class_dic)

        aircraft_list = get_units_from_side(side_guid, "CAircraft", all_info_dict)
        if aircraft_list:
            pylog.info("aircraft:%s" % len(aircraft_list))

        facility_list = get_units_from_side(side_guid, "CFacility", all_info_dict)
        if facility_list:
            pylog.info("facility:%s" % len(facility_list))

        contacts_dic = get_contacts_from_side(side_guid, all_info_dict)
        if contacts_dic:
            pylog.info("contacts:%s" % len(contacts_dic))

            for guid in contacts_dic:
                # pylog.info("contact guid:%s" % guid)
                actual_unit = get_contact_actual_unit_dic(guid, all_info_dict)
                # pylog.info(actual_unit["strName"])
                # pylog.info("dLatitude:%s" % actual_unit["dLatitude"])
                # pylog.info("dLongitude:%s" % actual_unit["dLongitude"])
                # pylog.info("m_Side:%s" % actual_unit["m_Side"])
                side_name = get_unit_side_name(actual_unit, all_info_dict)
                # pylog.info("side name:%s" % side_name)
                # raise
