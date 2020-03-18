#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : env.py
# Create date : 2020-01-04 23:31
# Modified date : 2020-03-06 18:04
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from MoziService.mozi_service import MoziService
from . import pylog

from MoziService.mozi_service import MoziService
from MoziService.paser_core import get_side_guid_from_side_name
from MoziService.paser_core import get_units_from_side
from MoziService.paser_core import check_is_exist_target
from MoziService.paser_core import get_target_contact_guid_from_target_name
from MoziService.paser_func import get_a_side_dic
from MoziService.paser_func import get_class_dic
from MoziService.paser_show import show_class_info
from MoziService.paser_show import show_item_info

from .geo import get_point_with_point_bearing_distance
from .task_reward import get_distance_reward
from .task_reward import get_target_distance

from . import etc
import numpy as np
import random

class MoziEnv():
    def __init__(self, IP, AIPort, scenario_name, simulate_compression):
        self.control_noise = True
        self.SERVER_PLAT = "linux"
        self.SERVER_IP = IP
        self.SERVER_PORT = AIPort
        self.connect_mode = 1
        self.DURATION_INTERVAL = etc.DURATION_INTERVAL
        self.simulate_compression = simulate_compression
        self.scenario_name = scenario_name
        self.mozi_service = MoziService(IP, AIPort, self.scenario_name, connect_mode = self.connect_mode)

        self.action_space = 4
        self.action_max = 1
        self.element_item_count = 8
        self.observation_space = self.element_item_count * 4 # two red aircraft, two blue aircraft

        self.last_situation_time = None
        self.red_unit_list = None
        self.blue_unit_list = None
        self.observation = None
        self.red_side_name = "红方"
        self.blue_side_name = "蓝方"

        self.last_red_aircraft_num = 0
        self.last_blue_aircraft_num = 0
        self.red_aircraft_num = 0
        self.blue_aircraft_num = 0

    def _get_mounts_guid_lt(self, item_dic):
        mounts_str = item_dic["m_Mounts"]
        guid_lt = mounts_str.split("@")
        #pylog.info("%s mounts guid:%s" %(item_dic["strUnitClass"], guid_lt))
        return guid_lt

    def _get_loadout_guid_lt(self, item_dic):
        mounts_str = item_dic["m_LoadoutGuid"]
        guid_lt = mounts_str.split("@")
        #pylog.info("%s loadout guid:%s" %(item_dic["strUnitClass"], guid_lt))
        return guid_lt

    def _show_mounts_info(self, mounts_guid_lt):
        for mounts_guid in mounts_guid_lt:
            pylog.info("mount guid:%s" % mounts_guid)
            item = self.mozi_service.all_info_dict[mounts_guid]
            for key in item:
                pylog.info("%s:%s" % (key, item[key]))

    def _show_loadout_info(self, guid_lt):
        for loadout_guid in guid_lt:
            pylog.info("loadout guid:%s" % loadout_guid)
            item = self.mozi_service.all_info_dict[loadout_guid]
            pylog.info("strName:%s" % item["strName"])
            pylog.info("m_AircraftGuid:%s" % item["m_AircraftGuid"])
            pylog.info("strLoadWeaponCount:%s" % item["strLoadWeaponCount"])
            pylog.info("m_LoadRatio:%s" % item["m_LoadRatio"])
            #for key in item:
           #    pylog.info("%s:%s" % (key, item[key]))

    def _init_red_unit_list(self):
        side_name = self.red_side_name

        ret_lt = []
        side_guid = get_side_guid_from_side_name(side_name, self.mozi_service.all_info_dict)
        side_dic = get_a_side_dic(side_guid, self.mozi_service.all_info_dict)
        aircraft_list_dic = get_units_from_side(side_guid, "CAircraft", self.mozi_service.all_info_dict)
        for key in aircraft_list_dic:
            item = aircraft_list_dic[key]
            if item["strUnitClass"] == '苏-35S型“超级侧卫”战斗机':
                ret_lt.append(key)
        return ret_lt

    def _init_blue_unit_list(self):
        side_name = self.blue_side_name

        ret_lt = []
        side_guid = get_side_guid_from_side_name(side_name, self.mozi_service.all_info_dict)
        side_dic = get_a_side_dic(side_guid, self.mozi_service.all_info_dict)
        aircraft_list_dic = get_units_from_side(side_guid, "CAircraft", self.mozi_service.all_info_dict)
        for key in aircraft_list_dic:
            item = aircraft_list_dic[key]
            if item["strUnitClass"] == 'F-15E型“攻击鹰式”战斗机':
                ret_lt.append(key)
        return ret_lt

    def _show_mounts_and_loadout(self):
        for guid in self.blue_unit_list:
            item = self.mozi_service.all_info_dict.get(guid, "")
            if item != "":
                mounts_guid_lt = self._get_mounts_guid_lt(item)
                #self._show_mounts_info(mounts_guid_lt)
                loadout_guid_lt = self._get_loadout_guid_lt(item)
                self._show_loadout_info(loadout_guid_lt)

        for guid in self.red_unit_list:
            item = self.mozi_service.all_info_dict.get(guid, "")
            if item != "":
                mounts_guid_lt = self._get_mounts_guid_lt(item)
                #self._show_mounts_info(mounts_guid_lt)
                loadout_guid_lt = self._get_loadout_guid_lt(item)
                self._show_loadout_info(loadout_guid_lt)

    def _init_unit_list(self):
        self.red_unit_list = self._init_red_unit_list()
        #pylog.info(len(self.red_unit_list))
        self.last_red_aircraft_num = len(self.red_unit_list)
        self.blue_unit_list = self._init_blue_unit_list()
        #pylog.info(len(self.blue_unit_list))
        self.last_blue_aircraft_num = len(self.blue_unit_list)

    def _get_a_side_observation(self, unit_list):
        obs_lt = []
        num = 0
        for key in unit_list:
            unit = self.mozi_service.all_info_dict.get(key,"")
            if unit:
                obs_lt.append(unit["fFuelConsumptionCruise"])
                obs_lt.append(unit["dLongitude"])
                obs_lt.append(unit["dLatitude"])
                obs_lt.append(unit["fCurrentHeading"])
                obs_lt.append(unit["fCurrentSpeed"])
                obs_lt.append(unit["fCurrentAlt"])
                obs_lt.append(unit["fPitch"])
                obs_lt.append(unit["fRoll"])
                num += 1
            else:
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)

        return obs_lt, num

    def _get_blue_observation(self):
        unit_list = self.blue_unit_list
        obs_lt,num = self._get_a_side_observation(unit_list)
        self.blue_aircraft_num = num
        return obs_lt

    def _get_red_observation(self):
        unit_list = self.red_unit_list
        obs_lt,num = self._get_a_side_observation(unit_list)
        self.red_aircraft_num = num
        return obs_lt

    def _get_observation(self):
        red_obs_lt = self._get_red_observation()
        #pylog.info(red_obs_lt)
        blue_obs_lt = self._get_blue_observation()
        #pylog.info(blue_obs_lt)
        red_obs_lt.extend(blue_obs_lt)
        #pylog.info(red_obs_lt)
        self.observation = red_obs_lt

        return  red_obs_lt

    def _set_duration_interval(self):
        self.mozi_service.mozi_task.sendAndRecv("Hs_OneTimeStop('Stop', %d)" % self.DURATION_INTERVAL)

    def _reset(self):
        ret = self.mozi_service.suspend_simulate()
        self.mozi_service.all_info_dict = {}
        self.scenario = self.mozi_service.load_scenario(plat=self.SERVER_PLAT)
        self._set_duration_interval()

        ret = self.mozi_service.set_run_mode()
        ret = self.mozi_service.set_simulate_compression(self.simulate_compression)
        ret = self.mozi_service.set_compression_mode(False)

        self._run_simulate()

    def _run_simulate(self):
        pylog.info("run simulation")
        return self.mozi_service.run_simulate()

    def _check_duration(self):
        update_situation_time = self.mozi_service.mozi_task.getCurrentTime()
        if self.last_situation_time != None:
            duration_time = float(update_situation_time) - float(self.last_situation_time)
            if int(duration_time) != self.DURATION_INTERVAL:
                pylog.error("duration_time:%s is differet from etc.DURATION_INTERVAL:%s" % (duration_time, self.DURATION_INTERVAL))

        self.last_situation_time = update_situation_time

    def _run_with_situation_data(self):
        self.mozi_service.update_situation(self.scenario)
        #self._check_duration()

    def _get_waypoint_heading(self, last_heading, action_value):
        current_heading = last_heading + action_value
        if current_heading < 0:
            current_heading += 360
        if current_heading > 360:
            current_heading -= 360
        return current_heading

    def _get_new_waypoint(self, heading, lat, lon, distance=20.0):
        dic = get_point_with_point_bearing_distance(lat, lon, heading, distance)
        return dic

    def _deal_point_data(self, waypoint):
        if self.control_noise:
            lon = str(float(waypoint["longitude"]) + random.random() / 10.0 - 0.05)
            lat = str(float(waypoint["latitude"]) + random.random() / 10.0 - 0.05)
        else:
            lon = str(waypoint["longitude"]),
            lat = str(waypoint["latitude"]),
        return lon, lat

    def _check_is_drop_sonobuoy(self, action_value):
        if action_value[1].item() > 0:
            return True
        return False

    def _get_aircraft_waypoint(self, action_value):
        obs = self.observation
        #pylog.info(obs)

        longitude = obs[0]
        latitude = obs[1]
        heading = obs[2]

        #waypoint_heading = self._get_waypoint_heading(heading, action_value[0].item() * 90)
        waypoint_heading = self._get_waypoint_heading(heading, action_value * 90)
        waypoint = self._get_new_waypoint(waypoint_heading, latitude, longitude)
        distance = get_target_distance(latitude, longitude)
        return waypoint, distance

    def _get_a_aircraft_waypoint(self, obs_item, action_value):

        longitude = obs_item[0]
        latitude = obs_item[1]
        heading = obs_item[2]

        waypoint_heading = self._get_waypoint_heading(heading, action_value * 90)
        #pylog.info("waypoint_heading:%s" % waypoint_heading)

        waypoint = self._get_new_waypoint(waypoint_heading, latitude, longitude)
        #pylog.info("waypoint:%s" % waypoint)

        return waypoint

    def _execute_action(self, action_value):
        count = 0
        for guid in self.red_unit_list:
            #pylog.info(guid)
            #pylog.info("observation:%s" % self.observation)
            obs_item = self.observation[count*self.element_item_count:(count+1)*self.element_item_count]
            #pylog.info("obs_item:%s" % obs_item)
            waypoint = self._get_a_aircraft_waypoint(obs_item, action_value[count].item())
            #pylog.info(waypoint)
            aircraft = self.mozi_service.get_entity(guid)
            if aircraft:
                lon, lat = self._deal_point_data(waypoint)
                aircraft.set_waypoint(self.red_side_name, guid, lon, lat)
                #if True:
                    #aircraft.set_up_throttleI(self.mozi_service.mozi_task)
                #    aircraft.set_up_throttleI()
                #else:
                    #aircraft.set_down_throttleI(self.mozi_service.mozi_task)
                #    aircraft.set_down_throttleI()

#               if True:
#                   aircraft.set_up_Alt(self.mozi_service.mozi_task)
#               else:
#                   aircraft.set_down_Alt(self.mozi_service.mozi_task)
            else:
                pylog.debug("aircraft:%s has been destroyed" % guid)
            count += 1


#       if self._check_is_find_target():
#           target_guid = self._get_target_guid()
#           aircraft.autoattack_target(target_guid, self.mozi_service.mozi_task)
#       else:
#           if distance < etc.target_radius:
#               if self._check_is_drop_sonobuoy(action_value):
#                   aircraft.drop_sonobuoy(self.red_side_name, "shallow", "active", self.mozi_service.mozi_task)

#           lon, lat = self._deal_point_data(waypoint)
#           aircraft.set_waypoint(self.red_side_name, guid, lon, lat, self.mozi_service.mozi_task)

    def _check_done(self):
        if not self._check_red_aircraft_exist():
            #pylog.info("do not has any red aircraft exit")
            if not self._check_red_missile_exist():
                #pylog.info("do not has any red missile exit")
                return True

        if not self._check_blue_aircraft_exist():
            #pylog.info("do not has any blue aircraft exit")
            if not self._check_blue_missile_exist():
                #pylog.info("do not has any blue missile exit")
                return True
        return False

    def _check_red_missile_exist(self):
        if self._get_red_missile_num() != 0:
            return True
        return False

    def _check_blue_missile_exist(self):
        if self._get_blue_missile_num() != 0:
            return True
        return False

    def _check_red_aircraft_exist(self):
        obs = self.observation
        for i in range(2*self.element_item_count):
            if obs[i] != 0.0:
                return True
        return False

    def _check_blue_aircraft_exist(self):
        obs = self.observation
        for i in range(2*self.element_item_count, 4*self.element_item_count):
            if obs[i] != 0.0:
                return True
        return False

    def _check_target_exist(self):
        if not check_is_exist_target(etc.target_name, self.mozi_service.all_info_dict):
            return False
        return True

    def _get_target_guid(self):
        target_name = etc.target_name
        target_guid = get_target_contact_guid_from_target_name(self.red_side_name, target_name, self.mozi_service.all_info_dict)
        return target_guid

    def _get_reward(self, action_value):
        reward = 0.0
        # get reward -1 when loss an aircraft
        reward += - (self.last_red_aircraft_num - self.red_aircraft_num ) * 1
        # get reward 1 when destroy an aircraft
        reward += (self.last_blue_aircraft_num - self.blue_aircraft_num) * 1

        self.last_red_aircraft_num = self.red_aircraft_num
        self.last_blue_aircraft_num = self.blue_aircraft_num

        if reward != 0.0:
            pylog.info("reward:%s" % reward)
            pylog.info("cur red aircraft num:%s cur blue aircraft num:%s" % (self.last_red_aircraft_num, self.last_blue_aircraft_num))
            pylog.info("cur red missile num:%s cur blue missile num:%s" % (self._get_red_missile_num(), self._get_blue_missile_num()))

        #self._show_mounts_and_loadout()

        return reward

    def _get_red_missile_num(self):
        side_name = self.red_side_name
        return self._get_missile_num(side_name)

    def _get_missile_num(self, side_name):
        missile_count = 0
        side_guid = get_side_guid_from_side_name(side_name, self.mozi_service.all_info_dict)
        side_dic = get_a_side_dic(side_guid, self.mozi_service.all_info_dict)
        for key in side_dic:
            if side_dic[key]["ClassName"] == "CWeapon":
                missile_count += 1
                #pylog.info(side_dic[key])
                pylog.info("m_PrimaryTargetGuid:%s" % side_dic[key]["m_PrimaryTargetGuid"])
                pylog.info("m_FiringUnitGuid:%s" % side_dic[key]["m_FiringUnitGuid"])
                #for k in side_dic[key]:
                #    pylog.info("%s:%s" % (k, side_dic[key][k]))

        return missile_count

    def _get_blue_missile_num(self):
        side_name = self.blue_side_name
        return self._get_missile_num(side_name)

    def reset(self):
        self._reset()
        self.mozi_service.init_situation(self.scenario)
        self._init_unit_list()
        obs = self._get_observation()
        return np.array(obs)

    def step(self, action):
        self._execute_action(action)
        self._run_with_situation_data()
        obs = self._get_observation()

        reward = self._get_reward(action)
        done = self._check_done()
        info = ""
        return np.array(obs), reward, done, info

    def connect_server(self):
        if not self.mozi_service.connect_mozi_server(self.SERVER_IP, self.SERVER_PORT):
            return False
        else:
            return True

