#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : aircraft.py
# Create date : 2019-11-06 19:38
# Modified date : 2019-12-25 16:09
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from .commonfunction import parse_weapons_record
from .loadout import CLoadout
from ..entitys.activeunit import CActiveUnit
from ..entitys import database as db


class CAircraft(CActiveUnit):
    '''飞机'''

    def __init__(self):
        '''飞机'''
        super().__init__()
        self.loadouts = {}

        # 方位类型
        self.m_BearingType = 0
        # 方位
        self.m_Bearing = 0.0
        # 距离（转换为千米）
        self.m_Distance = 0.0
        # 高低速交替航行
        self.bSprintAndDrift = False
        # 载机按钮的文本描述
        self.strDockAircraft = ""
        # 类别
        self.m_Category = 0
        # 悬停
        self.fHoverSpeed = 0.0
        # 低速
        self.fLowSpeed = 0.0
        # 巡航
        self.fCruiseSpeed = 0.0
        # 军力
        self.fMilitarySpeed = 0.0
        # 加速
        self.fAddForceSpeed = 0.0
        # 机型（战斗机，多用途，加油机...)
        self.m_Type = 0
        # 宿主单元对象
        self.m_CurrentHostUnit = ""
        # 挂载方案的DBID
        self.iLoadoutDBID = 0
        # 挂载方案的GUid
        self.m_LoadoutGuid = ""
        # 获取当前行动状态
        self.strAirOpsConditionString = 0
        # 完成准备时间
        self.strFinishPrepareTime = ""
        # 快速出动信息
        self.strQuickTurnAroundInfo = ""
        # 显示燃油信息
        self.strFuelState = ""
        # 期望高度
        self.fDesiredAltitude = 0.0
        # 维护状态
        self.m_MaintenanceLevel = 0
        self.fFuelConsumptionCruise = 0.0
        self.fAbnTime = 0.0
        self.iFuelRecsMaxQuantity = 0
        # 当前油量
        self.iCurrentFuelQuantity = 0
        # 是否快速出动
        self.bQuickTurnaround_Enabled = False
        # 是否有空中加油能力
        self.bIsAirRefuelingCapable = False
        # 加油队列header
        self.strShowTankerHeader = ""
        # 加油队列明细
        self.m_ShowTanker = ""
        # 可受油探管加油
        self.m_bProbeRefuelling = False
        # 可输油管加油 
        self.m_bBoomRefuelling = False
        # from dong:
        # 航路点名称
        self.strWayPointName = ""
        # 航路点描述
        self.strWayPointDescription = ""
        # 航路点剩余航行距离
        self.strWayPointDTG = ""
        # 航路点剩余航行时间
        self.WayPointTTG = ""
        # 航路点需要燃油数
        self.strWayPointFuel = ""

    def get_loadout_info(self):
        pass

    def delete_sub_object(self):
        """
        当删除本元素时，删除子对象
        返回需要先删除的子对象guid列表
        :return:
        """
        del_list = self.delete_sub_object()  # guid 列表  sensors.keys()， mounts.keys()

        if self.loadout is not None:
            del_list.append(self.loadout.guid)
            del self.loadout
        return del_list

    def air_get_loadout_info(self):
        """
        获取挂载方案的武器信息
        :return:
        """
        if self.loadout is None:
            return ""
        else:
            info = [{
                "loadout_name": self.loadout.strName,
                "loadout_guid": self.loadout.guid,
                "loadout_dbid": self.loadout.iDBID,
                "loadout_weapons": parse_weapons_record(self.loadout.m_LoadRatio)
            }]
        return info

    def air_get_valid_weapons(self):
        """
        获取飞机有效的武器
        :return:
        """
        info = {}
        # mount.values 可能是不同的mount，mount_obj.strWeapon,说明mount_obj 是一个对象
        for mount_obj in self.mounts.values():
            if (mount_obj.strWeaponFireState == "就绪" or "秒" in mount_obj.strWeaponFireState) \
                    and mount_obj.m_ComponentStatus <= 1:
                mount_weapons = parse_weapons_record(mount_obj.m_LoadRatio)
                for w_record in mount_weapons:
                    w_dbid = w_record['wpn_dbid']
                    if db.check_weapon_attack(w_dbid):
                        if w_dbid in info:
                            info[w_dbid] += w_record['wpn_current']
                        else:
                            info[w_dbid] = w_record['wpn_current']
        if self.loadout is not None:
            mount_weapons = parse_weapons_record(self.loadout.m_LoadRatio)
            for w_record in mount_weapons:
                w_dbid = w_record['wpn_dbid']
                if db.check_weapon_attack(w_dbid):
                    if w_dbid in info:
                        info[w_dbid] += w_record['wpn_current']
                    else:
                        info[w_dbid] = w_record['wpn_current']
        return info

    def air_get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            # "guid": self.guid,
            "guid": self.strGuid,
            "DBID": self.iDBID,
            "subtype": str(self.m_Type),
            "facilityTypeID": "",
            "name": self.strName,
            # "side": self.side_name,
            "proficiency": self.m_ProficiencyLevel,  # ?
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "altitude_asl": self.iAltitude_ASL,
            # "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,  # ?
            "fuelstate": self.strFuelState,  # ?
            "weaponstate": -1,  # ?
            "mounts": self.get_mounts_info(),
            "targetedBy": self.get_target_by_info(),
            "pitch": self.fPitch,
            "roll": self.fRoll,
            "yaw": self.fCurrentHeading,  # ?
            "loadout": self.get_loadout_info(),
            "type": "Aircraft",
            "fuel": self.iCurrentFuelQuantity,  # ?
            "damage": self.strDamageState,  # ?
            "sensors": self.get_sensors_info(),
            "weaponsValid": self.get_valid_weapons()
        }
        return info_dict

    def get_status_type(self):
        """
        获取飞机状态
        :return: int
        """
        if self.strAirOpsConditionString in (1, 2, 4, 8, 9, 18, 23, 24, 26):
            # 在基地可马上部署飞行任务
            return 'validToFly'
        elif self.strAirOpsConditionString in (0, 13, 14, 15, 16, 19, 20, 21, 22):
            # 在空中可部署巡逻，进攻，航路规划
            return 'InAir'
        elif self.strAirOpsConditionString in (5, 10, 11, 17, 25):
            # 在空中返航或降落
            return 'InAirRTB'
        else:
            return 'WaitReady'

    def air_set_waypoint(self, longitude, latitude):
        '''
        类别：推演所用函数
        设置飞机下一个航路点
        :param strGuid:
        :param longitude:
        :param latitude:
        :return:
        '''
        lua_str = "ScenEdit_SetUnit({side= '%s', guid='%s', course={ { Description = ' ', TypeOf = 'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
            self.strName, self.strGuid, longitude, latitude)
        return self.mozi_server.sendAndRecv(lua_str)

    def air_autoattack_target(self, target_guid):
        """
        自动攻击
        target_guid 目标guid
        """
        ret = self.mozi_server.sendAndRecv(
            "ScenEdit_AttackContact ('%s', '%s', {mode=0})" % (self.strGuid, target_guid))
        return ret

    def air_get_guid_from_name(self, target_name, all_info_dict):
        '''
        查找飞机guid通过飞机名称
        target_name : 要查找的单元名称
        all_info_dict : 单元字典

        return :
        '25368-sddssfas-sddsdwe-5dsacdc'/False
        '''
        for guid in all_info_dict:
            item = all_info_dict[guid]
            name = item.get("strName", "")
            class_name = item["ClassName"]
            if class_name != "CContact":
                if name == target_name:
                    return guid
        return False

    def air_check_is_exist_target(self, target_name, all_info_dict):
        '''
        类别：推演所用函数
        检查目标是否存在
        param ：
        target_name ：目标名称
        all_info_dict ：所有单元信息字典
        return : true（存在）/false（不存                                                                                                                                                                                                                                                                                                                                                                                        ）
        '''
        ret = self.get_guid_from_name(target_name, all_info_dict)
        if ret:
            return True
        return False

    def air_manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        类别：推演所用函数
        飞机手动开火函数
        作者：解洋
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量        
        return :
        lua执行成功/lua执行失败
        '''
        return super().manual_pick_war(target_guid, weapon_dbid, weapon_num)

    def set_up_throttleI(self):
        '''
        类别：推演所用函数
        升油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == 0:
            throttle_str = "Loiter"
        elif self.m_CurrentThrottle == 1:
            throttle_str = "Full"
        elif self.m_CurrentThrottle == 2:
            throttle_str = "Flank"
        elif self.m_CurrentThrottle == 3:
            throttle_str = "Cruise"
        else:
            return None
        return super().set_throttle(throttle_str)

    def set_down_throttleI(self):
        '''        
        类别：推演所用函数
        降油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == 1:
            throttle_str = "FullStop"
        if self.m_CurrentThrottle == 2:
            throttle_str = "Loiter"
        if self.m_CurrentThrottle == 3:
            throttle_str = "Full"
        if self.m_CurrentThrottle == 4:
            throttle_str = "Flank"
        return super().set_throttle(throttle_str)

    def ops_singleout(self, base_guid):
        '''
        类别：推演所用函数
        设置在基地内飞机单机出动
        base_guid : 飞机所在机场的guid
        return :
        lua执行成功/lua执行失败
        '''
        return super().unitops_singleout(base_guid, self.strGuid)

    def set_rader_shutdown(self, trunoff):
        '''
        类别：推演所用函数
        设置雷达开关机
        guid : 要设置单元唯一标识（guid）
        '''
        return super().set_rader_shutdown(trunoff)

    def air_desired_height(self, desired_height):
        """
        类别：推演所用函数
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        return super().set_desired_height(desired_height)

    def return_to_base(self):
        '''
        类别：推演所用函数
        飞机返回基地
        '''
        return super().return_to_base()

    def plotted_course(self, course_list):
        """
        类别：推演所用函数
        飞机航线规划
        :param course_list: list, [(lat, lon)], 例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        return super().plotted_course(course_list)

    def deploy_dipping_sonar(self):
        '''
        类别：推演所用函数
        部署吊放声呐
        '''
        return self.mozi_server.sendAndRecv("Hs_DeployDippingSonar('{}')".format(self.strGuid))

    def assign_unitList_to_missionEscort(self, mission_name):
        """
        类别：推演所用函数
        将单元分配为某打击任务的护航任务
        :param mission_name: 任务名称
        """
        return super().assign_unitList_to_missionEscort(mission_name)

    def drop_active_sonobuoy(self, sideName, deepOrShallow):
        '''
        类别：推演所用函数
        投放主动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: deep ，shallow
        '''
        return super().drop_active_sonobuoy(sideName, deepOrShallow)

    def drop_passive_sonobuoy(self, sideName, deepOrShallow):
        '''
        类别：推演所用函数
        投放被动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return super().drop_passive_sonobuoy(sideName, deepOrShallow)

    def set_airborne_time(self, unitNameOrId, hour, minute, scond):
        '''
        类别：编辑所用函数
        设置留空时间
        unitNameOrId 单元
        hour 小时
        minute 分钟
        scond 秒
        '''
        lua_scrpt = "Hs_SetAirborneTime('{}',{},{},{})".format(unitNameOrId, hour, minute, scond)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def time_To_ready(self, time):
        '''
        类别：编辑所用函数
        Hs_ScenEdit_TimeToReady 空中任务设置出动准备时间
        time 时间
        '''
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_TimeToReady({},{})".format(time, self.strGuid))

    def quick_turnaround(self, true_or_false, sorties_total):
        '''
        类别：推演所用函数
        函数功能：让指定飞机快速出动。
        参数说明：
        1）UnitNameOrID：字符串。单元名称或 GUID； 
        2）TrueOrFalse：布尔值。是否快速出动的状态标识符；
        3）SortiesTotal：数值型。出动架次总数
        '''
        lua = "Hs_QuickTurnaround('%s',%s,%s)" % (self.strGuid, true_or_false, sorties_total)
        self.mozi_server.scenAndRecv(lua)

    def set_fuel_qty(self, remainingFuel):
        '''
        类别：编辑所用函数
        函数功能：通过设置飞机的剩余油量来。
        参数说明：
        1）UnitNameOrID：字符串。单元名称或 GUID； 
        2）RemainingFuel：字符串。剩余测量。
        '''
        lua = " Hs_SetFuelQty('%s','%s')" % (self.strName, remainingFuel)
        self.mozi_server.scenAndRecv(lua)

    def ReadyImmediately(self, EnableQuickTurnarour, comboBox, immediatelyGo, optionalWeapon, igmoreWeapon):
        """
        作者：赵俊义
        日期：2020-3-10
        函数功能：飞机立即完成出动准备。
        函数类型：编辑 函数
        @param EnableQuickTurnarour:布尔值。是否支持快速出动(true 支持、false 不支持)
        @param comboBox:为快速出动值,不支持时填-1，支持填 0
        @param immediatelyGo:是否立即出动（true 为立即出动）
        @param optionalWeapon:是否不含可选武器（true 不含可选武器）
        @param igmoreWeapon:是否不忽略武器（true 不忽略武器）
        @return:
        """
        lua_scrpt = "Hs_ReadyImmediately('{}',{},{},{},{},{},{})".format(self.strGuid, self.iLoadoutDBID,
                                                                         EnableQuickTurnarour, comboBox, immediatelyGo,
                                                                         optionalWeapon, igmoreWeapon)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def OKReadyMission(self, EnableQuickTurnarour, comboBox):
        """
        作者：赵俊义
        日期：2020-3-10
        函数功能：飞机按对应的挂载方案所需准备时间完成出动准备
        函数类型：编辑 函数
        @param EnableQuickTurnarour: 布尔值。是否支持快速出动(true 支持、false 不支持)
        @param comboBox: 为快速出动值,不支持时填-1，支持填 0
        @return:
        """
        lua_scrpt = "Hs_OKReadyMission(a.guid, 18282,true,3)".format(self.strGuid,
                                                                     self.iLoadoutDBID, EnableQuickTurnarour, comboBox)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def air_group_out(self, air_guid_list):
        """
        编组出动
        :param air_guid_list: 飞机的guid，例子：['71136bf2-58ba-4013-92f5-2effc99d2wds','71136bf2-58ba-4013-92f5-2effc99d2fa0']
        :return:
        """
        table = str(air_guid_list).replace('[', '{').replace(']', '}')
        lua_scrpt = "Hs_LUA_AirOpsGroupOut('{}',{})".format(self.strGuid, table)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def AirOpsAbortLaunch(self):
        """
        作者：赵俊义
        日期：2020-3-10
        函数功能：让正在出动中的飞机立即终止出动。
        函数类型：推演函数
        @return:
        """
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_AirOpsAbortLaunch({})".format(self.strGuid))

    def set_waypoint(self, side_name, guid, longitude, latitude):
        '''
        设置飞机下一个航路点
        :param strGuid:
        :param longitude:
        :param latitude:
        :return:
        '''
        lua_str = "ScenEdit_SetUnit({side= '%s', guid='%s', course={ { Description = ' ', TypeOf = 'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
        side_name, guid, longitude, latitude)
        self.mozi_server.sendAndRecv(lua_str)

    def autoattack_target(self, target_guid):
        '''
        自动攻击
        target_guid 目标guid
        '''
        ret = self.mozi_server.sendAndRecv("ScenEdit_AttackContact ('%s', '%s', {mode=0})" % (self.strGuid, target_guid))
        return ret
