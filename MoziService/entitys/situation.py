# -*- coding:utf-8 -*-
##########################################################################################################
# File name : situation.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################8
import logging
import time
import random
import json
from datetime import datetime
from .sensor import CSensor
from .loadout import CLoadout 
from .magazine import CMagazine
from .mount import CMount
from .ship import CShip
from .satellite import Csatellite
from .facility import CFacility
from .side import CSide
from .submarine import Csubmarine
from .aircraft import CAircraft
from .weapon import CWeapon
from .contact import  CContact
from .group import CGroup
from .waypoint import CWayPoint
from .weather import CWeather
from .referencepoint import CReferencePoint
from .mission import CMission 
from .doctrine import CDoctrine
from .loggedmessage import CLoggedMessage
from .simEvent import CSimEvent
import pylog
import json


def get_red_missile_info(all_info_dict):
    red_missile_info = {}
    red_missile_guid = []
    for guid in list(all_info_dict.keys()):
        item = all_info_dict[guid]
        if item["ClassName"] == "CAircraft":
            red_missile_guid.append(guid)
            red_missile_info[guid] = item
    return red_missile_info


class CSituation():
    '''推演'''
    def __init__(self,mozi_server):
        """Constructor"""
        self.all_guid = []
        self.all_info_dict = {}
        self.red_info_dict = {}
        #传感器字典
        self.sensor_dic = {}
        #挂载字典
        self.loadout_dic = {}
        #弹药库字典
        self.magazine_dic = {}
        #挂架字典
        self.mount_dic = {}
        #推演方字典，所有的实体单元都存在这个字典
        self.side_dic = {}
        self.waponit_dic = {}
        #天气类
        self.weather = None
        self.all_situation_dic = {}
        #条令字典
        self.doctrine = {}
        self.simEvent_dic = {}
        #记录所有guid对应的类型，和推演方。用于维护所有态势使用
        self.all_guid_info = {}
        self.acrionPoints = {}
        self.mozi_server = mozi_server
    
    def update_red_info_dict(self, red_missile_info,red_info_dict):
        for guid in list(red_missile_info.keys()):
            item = red_missile_info[guid]
            for key in list(item.keys()):
                try:
                    red_info_dict[guid][key] = red_missile_info[guid][key]
                except Exception as e:
                    pylog.error("error:%s key:%s" % (e, key))
                    raise
        self.red_info_dict = None
        self.red_info_dict = red_info_dict 

    def init_situation(self, mozi_server,scenario):
        '''获取全局态势'''
        load_success = False
        for i in range(20):
            load_result = mozi_server.sendAndRecv("Isload")
            if load_result == "True":
                load_success = True
                break
            time.sleep(1)
        if not load_success:
            logging.info("Interrupted, the situation object can not be created!")
            return False

        situation_str = mozi_server.sendAndRecv("GetAllState")
        self.parse_init_situation(situation_str,scenario)
    
    def parse_init_situation(self, situation_str,scenario):
        """
        传入初始获取全局态势字符串，构建本地对象体系框架
        :param situation_str:  str, 初始全局态势字符串
        :return:
        """
        try:
            situation_dict = json.loads(situation_str)
            self.all_guid = list(situation_dict.keys())
            self.all_info_dict = situation_dict
            pylog.info(self.all_info_dict)
            # 解析态势
            #parse_side(situation_dict)
            #parse_aircraft(situation_dict)
        except Exception as e:
            pylog.error("Failed to json initial situation' return %s" % e)
            return False
        for key ,vaule in situation_dict.items():
            if vaule["ClassName"] == "CSensor":
                self.parse_sensor(vaule)
            elif vaule["ClassName"] == "CLoadout":
                self.parse_loadout(vaule)
            elif vaule["ClassName"] == "CMagazine":
                self.parse_magazine(vaule)
            elif vaule["ClassName"] == "CMount":
                self.parse_mount(vaule)  
            elif vaule["ClassName"] == "CShip":
                self.parse_ship(vaule)
            elif vaule["ClassName"] == "CSatellite":
                self.parse_satellite(vaule)
            elif vaule["ClassName"] == "CSubmarine":
                self.parse_submarine(vaule)
            elif vaule["ClassName"] == "CFacility":
                self.parse_facility(vaule)
            elif vaule["ClassName"] == "CAircraft":
                self.parse_aircraft(vaule)
            elif vaule["ClassName"] == "CWeapon":
                self.parse_weapon(vaule)
            elif vaule["ClassName"] == "CContact":
                self.parse_contact(vaule) 
            elif vaule["ClassName"] == "CGroup":
                self.parse_group(vaule)
            elif vaule["ClassName"] == "CWeather":
                self.parse_weather(vaule)    
            elif vaule["ClassName"] == "CReferencePoint":
                self.parse_referencePoint(vaule)
            elif vaule["ClassName"] == "CSide":
                self.parse_side(vaule)
            elif vaule["ClassName"] == "CMission":
                self.parse_mission(vaule)
            elif vaule["ClassName"] == "CCurrentScenario":
                self.parse_scenario(vaule,scenario)
            elif vaule["ClassName"] == "CActionPoints":
                self.acrionPoints[vaule["strGuid"]] = vaule
            elif vaule["ClassName"] == "CSimEvent":
                self.parse_simEvent(vaule)    
                
    def update_situation(self,mozi_server,scenario):
        """
        更新态势
        :return:
        """
        update_data = mozi_server.sendAndRecv("UpdateState")
        situation_data = self.parse_update_situation(update_data,scenario)
        return situation_data
    
    def parse_update_situation(self, update_data,scenario):
        """
        传入更新的态势字符串，解析后更新到本地框架对象中
        :param update_data: str, 更新的态势字符串
        :return:
        """
        if isinstance(update_data, str):
            try:
                situation_data = json.loads(update_data.strip())
            except Exception as e:
                pylog.error("Failed to json update situation's resturn:%s" % e)
                return
        else:
            situation_data = update_data
        for key ,vaule in situation_data.items():
            if vaule["ClassName"] == "CSensor":
                self.parse_sensor(vaule)
            elif vaule["ClassName"] == "CLoadout":
                self.parse_loadout(vaule)
            elif vaule["ClassName"] == "CMagazine":
                self.parse_magazine(vaule)
            elif vaule["ClassName"] == "CMount":
                self.parse_mount(vaule)  
            elif vaule["ClassName"] == "CShip":
                self.parse_ship(vaule)
            elif vaule["ClassName"] == "CSatellite":
                self.parse_satellite(vaule)
            elif vaule["ClassName"] == "CSubmarine":
                self.parse_submarine(vaule)
            elif vaule["ClassName"] == "CFacility":
                self.parse_facility(vaule)
            elif vaule["ClassName"] == "CAircraft":
                self.parse_aircraft(vaule)
            elif vaule["ClassName"] == "CWeapon":
                self.parse_weapon(vaule)
            elif vaule["ClassName"] == "CContact":
                self.parse_contact(vaule) 
            elif vaule["ClassName"] == "CGroup":
                self.parse_group(vaule)
            elif vaule["ClassName"] == "CWeather":
                self.parse_weather(vaule)    
            elif vaule["ClassName"] == "CReferencePoint":
                self.parse_referencePoint(vaule)
            elif vaule["ClassName"] == "Delete":
                self.parse_delete(vaule)   
            elif vaule["ClassName"] == "CSide":
                self.parse_side(vaule)
            elif vaule["ClassName"] == "CMission":
                self.parse_mission(vaule)
            elif vaule["ClassName"] == "CActionPoints":
                scenario.acrionPoints = vaule
            elif vaule["ClassName"] == "CSimEvent":
                self.parse_simEvent(vaule)     
            elif vaule["ClassName"] == "CCurrentScenario":
                self.parse_scenario(vaule,scenario)                
        return situation_data  
        

    def parse_sensor(self, sensor_json):
        guid = sensor_json["strGuid"]
        if guid in self.all_guid_info:
            sensor = self.sensor_dic[guid]
        else:
            sensor = CSensor()
        sensor.strGuid = guid
        if "strName" in sensor_json:
            sensor.strName = sensor_json["strName"]
        if "m_ParentPlatform" in sensor_json:
            sensor.m_ParentPlatform = sensor_json["m_ParentPlatform"]
        if "m_ComponentStatus" in sensor_json:
            # 部件状态
            sensor.m_ComponentStatus = sensor_json["m_ComponentStatus"]
        if "m_DamageSeverity" in sensor_json:
            # 毁伤程度的轻,中,重
            sensor.m_DamageSeverity = sensor_json["m_DamageSeverity"]
        if "m_CoverageArc" in sensor_json:
            # 挂载方位
            sensor.m_CoverageArc = sensor_json["m_CoverageArc"]
        if "bActive" in sensor_json:
            # 是否开机
            sensor.bActive = sensor_json["bActive"]
        if "strDescription" in sensor_json:
            # 传感器类型描述
            sensor.strDescription = sensor_json["strDescription"]
        if "strWorkStatus" in sensor_json:
            # 传感器工作状态
            sensor.strWorkStatus = sensor_json["strWorkStatus"]
        if "m_SensorType" in sensor_json:
            # 传感器类型
            sensor.m_SensorType = sensor_json["m_SensorType"]
        if "m_SensorRole" in sensor_json:
            # 传感器角色
            sensor.m_SensorRole = sensor_json["m_SensorRole"]
        if "fCruiseSpeed" in sensor_json:
            # 最大探测距离
            sensor.fMaxRange = sensor_json["fMaxRange"]
        if "fMinRange" in sensor_json:
            # 最小探测距离
            sensor.fMinRange = sensor_json["fMinRange"]
        if "i_TrackingTargetsWhenUsedAsDirector" in sensor_json:
            # 当传感器用作武器指示器时，正在跟踪照射的目标列表数量
            sensor.i_TrackingTargetsWhenUsedAsDirector = sensor_json["i_TrackingTargetsWhenUsedAsDirector"]
        if "m_TrackingTargetsWhenUsedAsDirector" in sensor_json:
            # 当传感器用作武器指示器时，正在跟踪照射的目标列表集合
            sensor.m_TrackingTargetsWhenUsedAsDirector = sensor_json["m_TrackingTargetsWhenUsedAsDirector"]
        if "m_SensorCapability" in sensor_json:
            # 传感器能力
            sensor.m_SensorCapability = sensor_json["m_SensorCapability"]
        # # 对空探测
        # # sensor.airSearch = sensor_json["airSearch"]
        # # # 对地/海面搜索
        # # sensor.surfaceSearch = sensor_json["surfaceSearch"]
        # # # 潜艇搜索
        # # sensor.submarineSearch = sensor_json["submarineSearch"]
        # # # 地面搜索-移动设备
        # # sensor.landSearch_Mobile = sensor_json["landSearch_Mobile"]
        # # # 地面搜索-固定设施
        # # sensor.landSearch_Fixed = sensor_json["landSearch_Fixed"]
        # # # 潜望镜搜索
        # # sensor.periscopeSearch = sensor_json["periscopeSearch"]
        # # # 太空搜索-ABM （反弹道导弹）
        # # sensor.ABM_SpaceSearch = sensor_json["ABM_SpaceSearch"]
        # # # 水/地雷与障碍物搜索
        # # sensor.m_bMineObstacleSearch = sensor_json["m_bMineObstacleSearch"]
        # # # 距离信息
        # # sensor.rangeInformation = sensor_json["rangeInformation"]
        # # # 航向信息
        # # sensor.headingInformation = sensor_json["headingInformation"]
        # # # 高度信息
        # # sensor.altitudeInformation = sensor_json["altitudeInformation"]
        # # # 速度信息
        # # sensor.speedInformation = sensor_json["speedInformation"]
        # # # 仅导航
        # # sensor.navigationOnly = sensor_json["navigationOnly"]
        # # # 仅地面测绘
        # # sensor.groundMappingOnly = sensor_json["groundMappingOnly"]
        # # # 仅地形回避/跟随
        # # sensor.terrainAvoidanceOrFollowing = sensor_json["terrainAvoidanceOrFollowing"]
        # # # 仅气象探测
        # # sensor.weatherOnly = sensor_json["weatherOnly"]
        # # # 仅气象探测与导航
        # # sensor.weatherAndNavigation = sensor_json["weatherAndNavigation"]
        # # # OTH-B （后向散射超视距雷达）
        # # sensor.OTH_Backscatter = sensor_json["OTH_Backscatter"]
        # # # OTH-SW （表面波超视距雷达）
        # # sensor.OTH_SurfaceWave = sensor_json["OTH_SurfaceWave"]
        # # # 鱼雷告警
        # # sensor.torpedoWarning = sensor_json["torpedoWarning"]
        # # # 导弹逼近告警
        # # sensor.missileApproachWarning = sensor_json["missileApproachWarning"]
        # # sensor.PS1 = sensor_json["PS1"]  # 左弦尾1
        # # sensor.PMA1 = sensor_json["PMA1"]  # 左弦中后1
        # # sensor.PMF1 = sensor_json["PMF1"]  # 左弦中前
        # # sensor.PB1 = sensor_json["PB1"]  # 左弦首1
        # # sensor.SS1 = sensor_json["SS1"]  # 右弦尾1
        # # sensor.SMA1 = sensor_json["SMA1"]  # 右弦中后1
        # # sensor.SMF1 = sensor_json["SMF1"]  # 右弦中前1
        # # sensor.SB1 = sensor_json["SB1"]  # 右弦首1-bow
        # # sensor.PS2 = sensor_json["PS2"]  # 左弦尾2-stern
        # # sensor.PMA2 = sensor_json["PMA2"]  # 左弦中后2
        # # sensor.PMF2 = sensor_json["PMF2"]  # 左弦中前2
        # # sensor.PB2 = sensor_json["PB2"]  # 左弦首2
        # # sensor.SS2 = sensor_json["SS2"]  # 右弦尾2
        # # sensor.SMA2 = sensor_json["SMA2"]  # 右弦中后2
        # # sensor.SMF2 = sensor_json["SMF2"]  # 右弦中前2
        # # sensor.SB2 = sensor_json["SB2"]  # 右弦首2
        # TODO
        self.sensor_dic[guid] = sensor
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType": 1001}

             
    def parse_loadout(self,loadout_json):
        guid = loadout_json["strGuid"]
        if guid in self.all_guid_info:
            loadout = self.loadout_dic[guid]
            loadout.select = False
        else:
            loadout = CLoadout(guid)
            loadout.select = True
        if "strName" in loadout_json:
            loadout.strName = loadout_json["strName"]
        if "m_AircraftGuid" in loadout_json:
            loadout.m_AircraftGuid  = loadout_json["m_AircraftGuid"]
        if "m_LoadRatio" in loadout_json:
            # 挂载的数量和挂架载荷
            loadout.m_LoadRatio = loadout_json["m_LoadRatio"]
        if "bQuickTurnaround" in loadout_json:
            # 是否支持快速出动
            loadout.bQuickTurnaround = loadout_json["bQuickTurnaround"]
        if "iMaxSorties" in loadout_json:
            # 最大飞行波次
            loadout.iMaxSorties = loadout_json["iMaxSorties"]
        if "m_CargoType" in loadout_json:
            # 货物类型
            loadout.m_CargoType = loadout_json["m_CargoType"]
        if "iDBID" in loadout_json:
            loadout.iDBID = loadout_json["iDBID"]
        #TODO
        self.loadout_dic[guid] = loadout
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 1002}
        #解析过后查找挂载所属单元
        #找到放到单元中，找不到先不管
        if loadout.m_AircraftGuid in self.all_guid_info and loadout.select:
            self.bind_activeUnit(loadout,loadout.m_AircraftGuid)
            pass
        
    def parse_magazine(self,magazine_json):
        guid = magazine_json["strGuid"]
        if guid in self.all_guid_info:
            magazine = self.magazine_dic[guid]
            magazine.select = False
        else:
            magazine = CMagazine(guid)
            magazine.select = True
        if "strName" in magazine_json:
            magazine.strName = magazine_json["strName"]
        if "m_ParentPlatform" in magazine_json:
            magazine.m_ParentPlatform = magazine_json["m_ParentPlatform"]
        if "m_ComponentStatus" in magazine_json:
            magazine.m_ComponentStatus = magazine_json["m_ComponentStatus"]
        if "m_DamageSeverity" in magazine_json:
            # 毁伤程度的轻,中,重
            magazine.m_DamageSeverity = magazine_json["m_DamageSeverity"]
        if "m_CoverageArc" in magazine_json:
            # 覆盖角度
            magazine.m_CoverageArc = magazine_json["m_CoverageArc"]
        if "m_LoadRatio" in magazine_json:
            # 挂架已挂载的数量和挂架载荷
            magazine.m_LoadRatio = magazine_json["m_LoadRatio"]
        #TODO
        self.magazine_dic[guid] = magazine
        if guid not in self.all_guid_info:            
            self.all_guid_info[guid] = {"strType": 1003}
        #解析过后查找弹药库所属单元
        #找到放到单元中，找不到先不管
        if magazine.m_ParentPlatform in self.all_guid_info and magazine.select:
            self.bind_activeUnit(magazine,magazine.m_ParentPlatform)
            pass
        
    def parse_mount(self,mount_json):
        guid = mount_json["strGuid"]
        if guid in self.all_guid_info:
            mount = self.mount_dic[guid]
            mount.select = False
        else:
            mount = CMount(guid)
            mount.strName = mount_json["strName"]
            mount.m_ParentPlatform = mount_json["m_ParentPlatform"]
            mount.select = True
        if "m_ComponentStatus" in mount_json:
            # 部件状态
            mount.m_ComponentStatus = mount_json["m_ComponentStatus"]
        if "m_DamageSeverity" in mount_json:
            # 毁伤程度的轻,中,重
            mount.m_DamageSeverity = mount_json["m_DamageSeverity"]
        if "m_CoverageArc" in mount_json:
            # 挂载方位
            mount.m_CoverageArc = mount_json["m_CoverageArc"]
        if "strWeaponFireState" in mount_json:
            # 挂载的武器开火状态
            mount.strWeaponFireState = mount_json["strWeaponFireState"]
        if "strLoadWeaponCount" in mount_json:
            # 挂载的武器的数量
            mount.strLoadWeaponCount = mount_json["strLoadWeaponCount"]
        if "m_LoadRatio" in mount_json:
            # 获取挂架下武器的最大载弹量和当前载弹量集合
            mount.m_LoadRatio = mount_json["m_LoadRatio"]
        if "m_Sensors" in mount_json:
            # 传感器的guid
            mount.m_Sensors = mount_json["m_Sensors"]
        if "m_ReloadPrioritySet" in mount_json:
            # 重新装载优先级选中的武器DBID集合
            mount.m_ReloadPrioritySet = mount_json["m_ReloadPrioritySet"]

        # # 左弦尾1
        # mount.PS1 = mount_json["PS1"]
        # # 左弦中后1
        # mount.PMA1 = mount_json["PMA1"]
        # # 左弦中前
        # mount.PMF1 = mount_json["PMF1"]
        # # 左弦首1
        # mount.PB1 = mount_json["PB1"]
        # # 右弦尾1
        # mount.SS1 = mount_json["SS1"]
        # # 右弦中后1
        # mount.SMA1 = mount_json["SMA1"]
        # # 右弦中前1
        # mount.SMF1 = mount_json["SMF1"]
        # # 右弦首1-bow
        # mount.SB1 = mount_json["SB1"]
        # # 左弦尾2-stern
        # mount.PS2 = mount_json["PS2"]
        # # 左弦中后2
        # mount.PMA2 = mount_json["PMA2"]
        # # 左弦中前2
        # mount.PMF2 = mount_json["PMF2"]
        # # 左弦首2
        # mount.PB2 = mount_json["PB2"]
        # # 右弦尾2
        # mount.SS2 = mount_json["SS2"]
        # # 右弦中后2
        # mount.SMA2 = mount_json["SMA2"]
        # # 右弦中前2
        # mount.SMF2 = mount_json["SMF2"]
        # # 右弦首2
        # mount.SB2 = mount_json["SB2"]
        #TODO
        self.mount_dic[guid] = mount
        if guid not in self.all_guid_info:            
            self.all_guid_info[guid] = {"strType" : 1004}
        #解析过后查找弹药库所属单元
        #找到放到单元中，找不到先不管
        if mount.m_ParentPlatform in self.all_guid_info and mount.select:
            self.bind_activeUnit(mount,mount.m_ParentPlatform)
            pass

    def parse_ship(self,ship_json):
        guid = ship_json["strGuid"]
        if guid in self.all_guid_info:
            ship =self.side_dic[self.all_guid_info[guid]['side']].ships[guid]
        else:
            ship = CShip()  
            ship.strGuid = guid
            ship.mozi_server = self.mozi_server
        if "strName" in ship_json:
            ship.strName = ship_json["strName"]
        if "m_Side" in ship_json:
            ship.m_Side = ship_json["m_Side"]
        if "m_BearingType" in ship_json:
            # 方位类型
            ship.m_BearingType =ship_json["m_BearingType"]
        if "m_Bearing" in ship_json:
            # 方位
            ship.m_Bearing = ship_json["m_Bearing"]
        if "m_Distance" in ship_json:
            # 距离（转换为千米）
            ship.m_Distance = ship_json["m_Distance"]
        if "bSprintAndDrift" in ship_json:
            # 高低速交替航行
            ship.bSprintAndDrift = ship_json["bSprintAndDrift"]
        if "m_Category" in ship_json:
            # 以下为 CShip 的属性
            # 类别
            ship.m_Category = ship_json["m_Category"]
        if "m_CommandPost" in ship_json:
            # 指挥部
            ship.m_CommandPost = ship_json["m_CommandPost"]
        if "m_Rudder" in ship_json:
            # 船舵
            ship.m_Rudder = ship_json["m_Rudder"]
        if "strFuelState" in ship_json:
            # 获取作战单元燃油信息
            # 显示燃油信息
            ship.strFuelState = ship_json["strFuelState"]
        if "m_Type" in ship_json:
            ship.m_Type = ship_json["m_Type"]  #
        if "strCavitation" in ship_json:
            # 空泡
            ship.strCavitation = ship_json["strCavitation"]
        if "fHoverSpeed" in ship_json:
            # 悬停
            ship.fHoverSpeed = ship_json["fHoverSpeed"]
        if "fLowSpeed" in ship_json:
            # 低速
            ship.fLowSpeed = ship_json["fLowSpeed"]
        if "fCruiseSpeed" in ship_json:
            # 巡航
            ship.fCruiseSpeed = ship_json["fCruiseSpeed"]
        if "fMilitarySpeed" in ship_json:
            # 军力
            ship.fMilitarySpeed = ship_json["fMilitarySpeed"]
        if "fAddForceSpeed" in ship_json:
            # 加速
            ship.fAddForceSpeed = ship_json["fAddForceSpeed"]
        if "strDamageInfo" in ship_json:
            # 载艇-信息
            # 毁伤
            ship.strDamageInfo = ship_json["strDamageInfo"]
        if "strWeaponInfo" in ship_json:
            # 武器
            ship.strWeaponInfo = ship_json["strWeaponInfo"]
        if "strMagazinesInfo" in ship_json:
            # 弹药库
            ship.strMagazinesInfo = ship_json["strMagazinesInfo"]
        if "strFuelInfo" in ship_json:
            # 燃料
            ship.strFuelInfo = ship_json["strFuelInfo"]
        if "strStatusInfo" in ship_json:
            # 状态
            ship.strStatusInfo = ship_json["strStatusInfo"]
        if "strTimeToReadyInfo" in ship_json:
            # 就绪时间
            ship.strTimeToReadyInfo = ship_json["strTimeToReadyInfo"]
        if "m_CargoType" in ship_json:
            # 货物类型
            ship.m_CargoType = ship_json["m_CargoType"]
        # 油门高度-航路点信息
        # 航路点名称至少一个航速指令为0公里/小时,不能估计剩余航行距离/时间/燃油量
        # ship.strWayPointName = ship_json["strWayPointName"]
        if "bCanRefuelOrUNREP" in ship_json:
            ship.bCanRefuelOrUNREP = ship_json["bCanRefuelOrUNREP"]
        if "strShowTankerHeader" in ship_json:
            # 补给队列header
            ship.strShowTankerHeader = ship_json["strShowTankerHeader"]
        if "m_ShowTanker" in ship_json:
            # 补给队列明显
            ship.m_ShowTanker = ship_json["m_ShowTanker"]
        self.paser_activeunit(ship_json ,ship)
        if ship.m_Side in self.side_dic:
            self.side_dic[ship.m_Side].ships[guid] = ship
        else:
            side = CSide(ship.m_Side, self.mozi_server)
            side.ships[guid] = ship
            self.side_dic[ship.m_Side] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2001,"side": ship.m_Side}

    def parse_satellite(self, satellite_json):
        '''
        解析卫星
        '''
        guid = satellite_json["strGuid"]
        if guid in self.all_guid_info:
            satellite =self.side_dic[self.all_guid_info[guid]['side']].satellites[guid]
        else:
            satellite = Csatellite()
            satellite.mozi_server  = self.mozi_server
            satellite.strGuid = guid
        if "m_ShowTanker" in satellite_json:
            satellite.strName = satellite_json["strName"]
        if "m_Side" in satellite_json:
            satellite.m_Side = satellite_json["m_Side"]
        if "m_SatelliteCategory" in satellite_json:
            satellite.m_SatelliteCategory = satellite_json["m_SatelliteCategory"]  # 卫星类别
        if "m_TracksPoints" in satellite_json:
            satellite.m_TracksPoints = satellite_json["m_TracksPoints"]  # 卫星航迹线 航迹是根据卫星算法得出的
        self.paser_activeunit(satellite_json ,satellite)
        if satellite.m_Side in self.side_dic:
            self.side_dic[satellite.m_Side].satellites[guid] = satellite
        else:
            side = CSide(satellite.m_Side, self.mozi_server)
            side.satellites[guid] = satellite
            self.side_dic[satellite.m_Side] = side
        if guid not in self.all_guid_info:            
            self.all_guid_info[guid] = {"strType" : 2002,"side": satellite.m_Side}

    def parse_submarine(self, submarine_json):
        '''
        解析水面单元
        '''
        guid = submarine_json["strGuid"]
        if guid in self.all_guid_info:
            submarine =self.side_dic[self.all_guid_info[guid]['side']].submarines[guid]
        else:
            submarine = Csubmarine()
            submarine.strGuid = guid
        if "strName" in submarine_json:
            submarine.strName = submarine_json["strName"]
        if "m_Side" in submarine_json:
            submarine.m_Side = submarine_json["m_Side"]
        if "m_BearingType" in submarine_json:
            submarine.m_BearingType = submarine_json["m_BearingType"]  # 方位类型
        if "m_Bearing" in submarine_json:
            submarine.m_Bearing = submarine_json["m_Bearing"] # 方位
        if "m_Distance" in submarine_json:
            submarine.m_Distance = submarine_json["m_Distance"] # 距离（转换为千米）
        if "bSprintAndDrift" in submarine_json:
            submarine.bSprintAndDrift = submarine_json["bSprintAndDrift"]  # 高低速交替航行
        if "m_AITargets" in submarine_json:
            submarine.m_AITargets = submarine_json["m_AITargets"]  # 获取AI对象的目标集合
        if "m_AITargetsCanFiretheTargetByWCSAndWeaponQty" in submarine_json:
            submarine.m_AITargetsCanFiretheTargetByWCSAndWeaponQty = submarine_json["m_AITargetsCanFiretheTargetByWCSAndWeaponQty"] # 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        if "strDockAircraft" in submarine_json:
            submarine.strDockAircraft = submarine_json["strDockAircraft"]  # 载机按钮的文本描述
        if "strDockShip" in submarine_json:
            submarine.strDockShip = submarine_json["strDockShip"]  # 载艇按钮的文本描述
        if "m_Category" in submarine_json:
            # 以下为 CSubmarine 的属性
            submarine.m_Category = submarine_json["m_Category"]  # 类型类别
        if "m_CIC" in submarine_json:
            submarine.m_CIC = submarine_json["m_CIC"]  # 指挥部
        if "m_Rudder" in submarine_json:
            submarine.m_Rudder = submarine_json["m_Rudder"]  # 船舵
        if "m_PressureHull" in submarine_json:
            submarine.m_PressureHull = submarine_json["m_PressureHull"]  # 船身
        if "strFuelState" in submarine_json:
            # 获取作战单元燃油信息
            submarine.strFuelState = submarine_json["strFuelState"]  # 显示燃油状态
        if "dPercentageDiesel" in submarine_json:
            # 柴油剩余百分比
            submarine.dPercentageDiesel = submarine_json["dPercentageDiesel"]
        if "dPercentageBattery" in submarine_json:
            # 电池剩余百分比
            submarine.dPercentageBattery = submarine_json["dPercentageBattery"]
        if "dPercentageAIP" in submarine_json:
            # AIP剩余百分比
            submarine.dPercentageAIP = submarine_json["dPercentageAIP"]
        if "m_Type" in submarine_json:
            submarine.m_Type = submarine_json["m_Type"]
        if "strCavitation" in submarine_json:
            submarine.strCavitation = submarine_json["strCavitation"]
        if "fHoverSpeed" in submarine_json:
            submarine.fHoverSpeed = submarine_json["fHoverSpeed"] # 悬停
        if "fLowSpeed" in submarine_json:
            submarine.fLowSpeed = submarine_json["fLowSpeed"]  # 低速
        if "fCruiseSpeed" in submarine_json:
            submarine.fCruiseSpeed = submarine_json["fCruiseSpeed"]  # 巡航
        if "fMilitarySpeed" in submarine_json:
            submarine.fMilitarySpeed = submarine_json["fMilitarySpeed"] # 军力
        if "fAddForceSpeed" in submarine_json:
            submarine.fAddForceSpeed = submarine_json["fAddForceSpeed"] # 加速
        if "iThermoclineUpDepth" in submarine_json:
            submarine.iThermoclineUpDepth = submarine_json["iThermoclineUpDepth"]  # 温跃层上
        if "iThermoclineDownDepth" in submarine_json:
            submarine.iThermoclineDownDepth = submarine_json["iThermoclineDownDepth"]  # 温跃层下
        if "strDamageInfo" in submarine_json:
            # 载艇-信息
            submarine.strDamageInfo = submarine_json["strDamageInfo"]  # 毁伤
        if "strWeaponInfo" in submarine_json:
            submarine.strWeaponInfo = submarine_json["strWeaponInfo"] # 武器
        if "strMagazinesInfo" in submarine_json:
            submarine.strMagazinesInfo = submarine_json["strMagazinesInfo"]  # 弹药库
        if "strFuelInfo" in submarine_json:
            submarine.strFuelInfo = submarine_json["strFuelInfo"]  # 燃料
        if "strStatusInfo" in submarine_json:
            submarine.strStatusInfo = submarine_json["strStatusInfo"] # 状态
        if "strTimeToReadyInfo" in submarine_json:
            submarine.strTimeToReadyInfo = submarine_json["strTimeToReadyInfo"]  # 就绪时间
        if "strWayPointName" in submarine_json:
            # 油门高度-航路点信息
            submarine.strWayPointName = submarine_json["strWayPointName"] # 航路点名称
        #解析父类属性
        self.paser_activeunit(submarine_json ,submarine)
        #绑定类型关系
        if submarine.m_Side in self.side_dic:
            self.side_dic[submarine.m_Side].submarines[guid] = submarine
        else:
            side = CSide(submarine.m_Side, self.mozi_server)
            side.submarines[guid] = submarine
            self.side_dic[submarine.m_Side] = side
        if guid not in self.all_guid_info:            
            self.all_guid_info[guid] = {"strType" : 2003,"side": submarine.m_Side}

    def parse_weapon(self, weapon_json):
        '''
        解析武器
        '''
        guid = weapon_json["strGuid"]
        if guid in self.all_guid_info:
            weapon =self.side_dic[self.all_guid_info[guid]['side']].weapons[guid]
        else:
            weapon = CWeapon()
            weapon.strGuid = guid
            weapon.mozi_server = self.mozi_server
        if "m_Side" in weapon_json:
            weapon.m_Side = weapon_json["m_Side"]
        if "m_strDataLinkParentGuid" in weapon_json:
            # 提供数据链的活动单元
            weapon.m_strDataLinkParentGuid = weapon_json["m_strDataLinkParentGuid"]
        if "m_PrimaryTargetGuid" in weapon_json:
            # 主要目标
            weapon.m_PrimaryTargetGuid = weapon_json["m_PrimaryTargetGuid"]
        if "fRangeASWMin" in weapon_json:
            # 反潜模式使用时最小作用距离
            weapon.fRangeASWMin = weapon_json["fRangeASWMin"]
        if "fRangeASWMax" in weapon_json:
            # 反潜模式使用时最大作用距离
            weapon.fRangeASWMax = weapon_json["fRangeASWMax"]
        if "fRangeLandMin" in weapon_json:
            # 最小射程
            weapon.fRangeLandMin = weapon_json["fRangeLandMin"]
        if "fRangeLandMax" in weapon_json:
            # 最大射程
            weapon.fRangeLandMax = weapon_json["fRangeLandMax"]
        if "fRangeASUWMin" in weapon_json:
            # 反舰模式使用时最小距离
            weapon.fRangeASUWMin = weapon_json["fRangeASUWMin"]
        if "fRangeASUWMax" in weapon_json:
            # 反舰模式使用时最大距离
            weapon.fRangeASUWMax = weapon_json["fRangeASUWMax"]
        if "fRangeAAWMin" in weapon_json:
            # 防空作战最小大作用距离
            weapon.fRangeAAWMin = weapon_json["fRangeAAWMin"]
        if "fRangeAAWMax" in weapon_json:
            # 防空作战最大作用距离
            weapon.fRangeAAWMax = weapon_json["fRangeAAWMax"]
        if "m_WeaponType" in weapon_json:
            # 武器类型
            weapon.m_WeaponType = weapon_json["m_WeaponType"]
        if "m_WeaponTargetType" in weapon_json:
            # 打击的目标类型
            weapon.m_WeaponTargetType = weapon_json["m_WeaponTargetType"]
        if "bIsOfAirLaunchedGuidedWeapon" in weapon_json:
            # 是否是空射制导武器
            weapon.bIsOfAirLaunchedGuidedWeapon = weapon_json["bIsOfAirLaunchedGuidedWeapon"]
        if "bSonobuoyActive" in weapon_json:
            # 是否是主动声纳
            weapon.bSonobuoyActive = weapon_json["bSonobuoyActive"]
        if "m_FiringUnitGuid" in weapon_json:
            # 发射单元GUID
            weapon.m_FiringUnitGuid = weapon_json["m_FiringUnitGuid"]
        if "m_ParentMount" in weapon_json:
            # 父挂架
            weapon.m_ParentMount = weapon_json["m_ParentMount"]
        if "m_ParentMagazine" in weapon_json:
            # 父弹药库
            weapon.m_ParentMagazine = weapon_json["m_ParentMagazine"]
        if "m_SonobuoyDepthSetting" in weapon_json:
            # 声呐深度设置
            weapon.m_SonobuoyDepthSetting = weapon_json["m_SonobuoyDepthSetting"]
        if "strSonobuoyRemainingTime" in weapon_json:
            # 如果是声纳浮标则发送它的剩余时间
            weapon.strSonobuoyRemainingTime = weapon_json["strSonobuoyRemainingTime"]
        self.paser_activeunit(weapon_json ,weapon)
        if weapon.m_Side in self.side_dic:
            self.side_dic[weapon.m_Side].weapons[guid] = weapon
        else:
            side = CSide(weapon.m_Side, self.mozi_server)
            side.weapons[guid] = weapon
            self.side_dic[weapon.m_Side] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2004,"side": weapon.m_Side}

    def parse_aircraft(self, aircraft_json):
        '''
        解析飞机
        '''
        guid = aircraft_json["strGuid"]
        if guid in self.all_guid_info:
            aircraft =self.side_dic[self.all_guid_info[guid]['side']].aircrafts[guid]
        else:
            aircraft = CAircraft()
        if "strActiveUnitStatus" in aircraft_json:
            aircraft.strActiveUnitStatus = aircraft_json["strActiveUnitStatus"]
        if "strName" in aircraft_json:
            aircraft.strName = aircraft_json["strName"]
        if "m_Side" in aircraft_json:
            aircraft.m_Side = aircraft_json["m_Side"]
        if "m_loadout" in aircraft_json:
            aircraft.loadout = aircraft_json["m_loadout"]
        if "m_BearingType" in aircraft_json: 
        # 方位类型
            aircraft.m_BearingType = aircraft_json["m_BearingType"]
        if "m_Bearing" in aircraft_json:
        # 方位
            aircraft.m_Bearing =aircraft_json["m_Bearing"]
        if "m_Distance" in aircraft_json:
        # 距离（转换为千米）
            aircraft.m_Distance =aircraft_json["m_Distance"]
        if "bSprintAndDrift" in aircraft_json:
        # 高低速交替航行
            aircraft.bSprintAndDrift = aircraft_json["bSprintAndDrift"]
        if "strDockAircraft" in aircraft_json:
        # 载机按钮的文本描述
            aircraft.strDockAircraft = aircraft_json["strDockAircraft"]
        if "m_Category" in aircraft_json:
        # 类别
            aircraft.m_Category = aircraft_json["m_Category"]
        if "fHoverSpeed" in aircraft_json:
        # 悬停
            aircraft.fHoverSpeed = aircraft_json["fHoverSpeed"]
        if "fLowSpeed" in aircraft_json:
        # 低速
            aircraft.fLowSpeed = aircraft_json["fLowSpeed"]
        if "fCruiseSpeed" in aircraft_json:
        # 巡航
            aircraft.fCruiseSpeed = aircraft_json["fCruiseSpeed"]
        if "fMilitarySpeed" in aircraft_json:
        # 军力
            aircraft.fMilitarySpeed = aircraft_json["fMilitarySpeed"]
        if "fAddForceSpeed" in aircraft_json:
        # 加速
            aircraft.fAddForceSpeed = aircraft_json["fAddForceSpeed"]
        if "m_Type" in aircraft_json:
        # 机型（战斗机，多用途，加油机...)
            aircraft.m_Type = aircraft_json["m_Type"]
        if "m_CurrentHostUnit" in aircraft_json:
        # 宿主单元对象
            aircraft.m_CurrentHostUnit = aircraft_json["m_CurrentHostUnit"]
        if "iLoadoutDBID" in aircraft_json:
        # 挂载方案的DBID
            aircraft.iLoadoutDBID = aircraft_json["iLoadoutDBID"]
        if "m_LoadoutGuid" in aircraft_json:
        # 挂载方案的GUid
            aircraft.m_LoadoutGuid = aircraft_json["m_LoadoutGuid"]
        if "strAirOpsConditionString" in aircraft_json:
        # 获取当前行动状态
            aircraft.strAirOpsConditionString = aircraft_json["strAirOpsConditionString"]
        if "strFinishPrepareTime" in aircraft_json:
        # 完成准备时间
            aircraft.strFinishPrepareTime = aircraft_json["strFinishPrepareTime"]
        if "strQuickTurnAroundInfo" in aircraft_json:
        # 快速出动信息
            aircraft.strQuickTurnAroundInfo = aircraft_json["strQuickTurnAroundInfo"]
        if "strFuelState" in aircraft_json:
        # 显示燃油信息
            aircraft.strFuelState = aircraft_json["strFuelState"]
        if "fDesiredAltitude" in aircraft_json:
        # 期望高度
            aircraft.fDesiredAltitude =aircraft_json["fDesiredAltitude"]
        if "m_MaintenanceLevel" in aircraft_json:
        # 维护状态
            aircraft.m_MaintenanceLevel = aircraft_json["m_MaintenanceLevel"]
        if "fFuelConsumptionCruise" in aircraft_json:
            aircraft.fFuelConsumptionCruise = aircraft_json["fFuelConsumptionCruise"]
        if "fAbnTime" in aircraft_json:
            aircraft.fAbnTime = aircraft_json["fAbnTime"]
        if "iFuelRecsMaxQuantity" in aircraft_json:
            aircraft.iFuelRecsMaxQuantity = aircraft_json["iFuelRecsMaxQuantity"]
        if "iCurrentFuelQuantity" in aircraft_json:
        # 当前油量
            aircraft.iCurrentFuelQuantity = aircraft_json["iCurrentFuelQuantity"]
        if "bQuickTurnaround_Enabled" in aircraft_json:
        # 是否快速出动
            aircraft.bQuickTurnaround_Enabled = aircraft_json["bQuickTurnaround_Enabled"]
        if "bIsAirRefuelingCapable" in aircraft_json:
        # 是否有空中加油能力
            aircraft.bIsAirRefuelingCapable = aircraft_json["bIsAirRefuelingCapable"]
        if "strShowTankerHeader" in aircraft_json:
        # 加油队列header
            aircraft.strShowTankerHeader = aircraft_json["strShowTankerHeader"]
        if "m_ShowTanker" in aircraft_json:
        # 加油队列明细
            aircraft.m_ShowTanker = aircraft_json["m_ShowTanker"]
        if "m_bProbeRefuelling" in aircraft_json:
        # 可受油探管加油
            aircraft.m_bProbeRefuelling = aircraft_json["m_bProbeRefuelling"]
        if "m_bBoomRefuelling" in aircraft_json:
        # 可输油管加油
            aircraft.m_bBoomRefuelling = aircraft_json["m_bBoomRefuelling"]
        if "strWayPointName" in aircraft_json:
        # from dong:
        # # 航路点名称
            aircraft.strWayPointName = aircraft_json["strWayPointName"]
        if "strWayPointDescription" in aircraft_json:
        # # 航路点描述
            aircraft.strWayPointDescription = aircraft_json["strWayPointDescription"]
        if "strWayPointDTG" in aircraft_json:
        # # 航路点剩余航行距离
            aircraft.strWayPointDTG = aircraft_json["strWayPointDTG"]
        if "WayPointTTG" in aircraft_json:
        # 航路点剩余航行时间
            aircraft.WayPointTTG = aircraft_json["WayPointTTG"]
        if "strWayPointFuel" in aircraft_json:
        # 航路点需要燃油数
            aircraft.strWayPointFuel = aircraft_json["strWayPointFuel"]
        self.paser_activeunit(aircraft_json ,aircraft)
        if aircraft.m_Side in self.side_dic:
            self.side_dic[aircraft.m_Side].aircrafts[guid] = aircraft
        else:
            side = CSide(aircraft.m_Side, self.mozi_server)
            side.aircrafts[guid] = aircraft
            self.side_dic[aircraft.m_Side] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2005,"side": aircraft.m_Side}        

    def parse_facility(self, facility_json):
        '''
        解析地面单元，人员
        '''
        guid = facility_json["strGuid"]
        if guid in self.all_guid_info:
            facility =self.side_dic[self.all_guid_info[guid]['side']].facilitys[guid]
        else:
            side_guid = facility_json["m_Side"]
            facility = CFacility(side_guid)
            facility.mozi_server = self.mozi_server
            facility.m_Side = side_guid
            facility.strGuid = guid
        if "strName" in facility_json:
            facility.strName = facility_json["strName"]
        # 方位类型
        if "m_BearingType" in facility_json:
            facility.m_BearingType = facility_json["m_BearingType"]
        # 方位
        if "m_Bearing" in facility_json:
            facility.m_Bearing = facility_json["m_Bearing"]
        # 距离（千米）
        if "m_Distance" in facility_json:
            facility.m_Distance = facility_json["m_Distance"]
        # 是否高速交替航行
        if "bSprintAndDrift" in facility_json:
            facility.bSprintAndDrift = facility_json["bSprintAndDrift"]
        # 载机按钮的文本描述
        if "strDockAircraft" in facility_json:
            facility.strDockAircraft = facility_json["strDockAircraft"]
        # 类别
        if "m_Category" in facility_json:
            facility.m_Category = facility_json["m_Category"]
        # 悬停
        if "fHoverSpeed" in facility_json:
            facility.fHoverSpeed = facility_json["fHoverSpeed"]
        # 低速
        if "fLowSpeed" in facility_json:
            facility.fLowSpeed = facility_json["fLowSpeed"]
        # 巡航
        if "fCruiseSpeed" in facility_json:
            facility.fCruiseSpeed = facility_json["fCruiseSpeed"]
        # 军力
        if "fMilitarySpeed" in facility_json:
            facility.fMilitarySpeed = facility_json["fMilitarySpeed"]
        # 加速
        # facility.fAddForceSpeed = 0.0
        # 载艇按钮的文本描述
        if "strDockShip" in facility_json:
            facility.strDockShip = facility_json["strDockShip"]
        if "m_CommandPost" in facility_json:
            facility.m_CommandPost = facility_json["m_CommandPost"]
        ## 加油队列明细
        #facility.m_ShowTanker = facility_json["m_ShowTanker"]
        self.paser_activeunit(facility_json ,facility)
        if facility.m_Side in self.side_dic:
            self.side_dic[facility.m_Side].facilitys[guid] = facility
        else:
            side = CSide(facility.m_Side, self.mozi_server)
            side.facilitys[guid]= facility
            self.side_dic[facility.m_Side] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2006,"side": facility.m_Side}

    def parse_contact(self,contact_json):
        '''
        解析目标
        '''
        guid = contact_json["strGuid"]
        if guid in self.all_guid_info:
            contact =self.side_dic[self.all_guid_info[guid]['side']].contacts[guid]
        else:
            contact =  CContact(guid, self.mozi_server)
        if "m_Side" in contact_json:  
            contact.m_Side = contact_json["m_Side"]
        if "strName" in contact_json:
            contact.strName = contact_json["strName"]
        # 实体类别
        if "strUnitClass" in contact_json:
            contact.strUnitClass = contact_json["strUnitClass"]
        # 当前纬度
        if "dLatitude" in contact_json:
            contact.dLatitude = contact_json["dLatitude"]
        # 当前经度
        if "dLongitude" in contact_json:
            contact.dLongitude = contact_json["dLongitude"]
        # 当前朝向
        if "fCurrentHeading" in contact_json:
            contact.fCurrentHeading =contact_json["fCurrentHeading"]
        # 当前速度
        if "fCurrentSpeed" in contact_json:
            contact.fCurrentSpeed = contact_json["fCurrentSpeed"]
        # 当前海拔高度
        if "fCurrentAltitude_ASL" in contact_json:
            contact.fCurrentAltitude_ASL = contact_json["fCurrentAltitude_ASL"]
        # 倾斜角
        if "fPitch" in contact_json:
            contact.fPitch = contact_json["fPitch"]
        # 翻转角
        if "fRoll" in contact_json:
            contact.fRoll = contact_json["fRoll"]
        # 是否在陆地上
        if "bIsOnLand" in contact_json:
            contact.bIsOnLand = contact_json["bIsOnLand"]
        # 可能匹配结果
        #contact.m_MatchingDBIDList = contact_json["m_MatchingDBIDList"]
        # 识别出的辐射平台
        #contact.strRadiantPoint = contact_json["strRadiantPoint"]
        if "strIconType" in contact_json:
            contact.strIconType = contact_json["strIconType"]
        if "strCommonIcon" in contact_json:
            contact.strCommonIcon = contact_json["strCommonIcon"]
        # 目标类型
        if "m_ContactType" in contact_json:
            contact.m_ContactType = contact_json["m_ContactType"]
        # 属方是否已知
        if "bSideIsKnown" in contact_json:
            contact.bSideIsKnown = contact_json["bSideIsKnown"]
        # 单元的识别状态
        if "m_IdentificationStatus" in contact_json:
            contact.m_IdentificationStatus = contact_json["m_IdentificationStatus"]
        # 本身单元的GUID
        if "m_ActualUnit" in contact_json:
            contact.m_ActualUnit = contact_json["m_ActualUnit"]
        # 探测到的推演方
        if "m_OriginalDetectorSide" in contact_json:
            contact.m_OriginalDetectorSide = contact_json["m_OriginalDetectorSide"]
        if "m_SidePostureStanceDictionary" in contact_json:
            # 其它推演方对本目标的立场姿态
            contact.m_SidePostureStanceDictionary = contact_json["m_SidePostureStanceDictionary"]
        # 速度是否已知
        if "bSpeedKnown" in contact_json:
            contact.bSpeedKnown = contact_json["bSpeedKnown"]
        # 朝向是否已知
        if "bHeadingKnown" in contact_json:
            contact.bHeadingKnown = contact_json["bHeadingKnown"]
        # 高度是否已知
        if "bAltitudeKnown" in contact_json:
            contact.bAltitudeKnown = contact_json["bAltitudeKnown"]
        # 电磁辐射Title
        if "strElectromagnetismEradiateTitle" in contact_json:
            contact.strElectromagnetismEradiateTitle = contact_json["strElectromagnetismEradiateTitle"]
        # 电磁辐射集合
        #contact.strElectromagnetismEradiate = contact_json["strElectromagnetismEradiate"]
        # 匹配结果标题
        if "strMatchingTitle" in contact_json:
            contact.strMatchingTitle = contact_json["strMatchingTitle"]
        # 侦察记录
        if "m_DetectionRecord" in contact_json:
            contact.m_DetectionRecord = contact_json["m_DetectionRecord"]
        # 不确定区域集合
        if "m_UncertaintyArea" in contact_json:
            contact.m_UncertaintyArea = contact_json["m_UncertaintyArea"]
        # 目标持续时间
        if "strAge" in contact_json:
            contact.strAge = contact_json["strAge"]
        # 取目标发射源容器中传感器的最大探测距离
        if "fMaxDetectRange" in contact_json:
            contact.fMaxDetectRange = contact_json["fMaxDetectRange"]
        # 获取最大对海探测范围
        if "fMaxRange_DetectSurfaceAndFacility" in contact_json:
            contact.fMaxRange_DetectSurfaceAndFacility = contact_json["fMaxRange_DetectSurfaceAndFacility"]
        # 获取最大对潜探测范围
        if "fMaxRange_DetectSubsurface" in contact_json:
            contact.fMaxRange_DetectSubsurface = contact_json["fMaxRange_DetectSubsurface"]
        # 获取目标探测时间
        #contact.fTimeSinceDetection_Visual = contact_json["fTimeSinceDetection_Visual"]
        # 获取瞄准目标的武器数量
        if "iWeaponsAimingAtMe" in contact_json:
            contact.iWeaponsAimingAtMe = contact_json["iWeaponsAimingAtMe"]
        if "fAirRangeMax" in contact_json:
            # 目标武器对空最大攻击距离
            contact.fAirRangeMax = contact_json["fAirRangeMax"]
        if "fSurfaceRangeMax" in contact_json:
            # 目标武器对海最大攻击距离
            contact.fSurfaceRangeMax = contact_json["fSurfaceRangeMax"]
        if "fLandRangeMax" in contact_json:
            # 目标武器对陆最大攻击距离
            contact.fLandRangeMax = contact_json["fLandRangeMax"]
        if "fSubsurfaceRangeMax" in contact_json:
            # 目标武器对潜最大攻击距离
            contact.fSubsurfaceRangeMax = contact_json["fSubsurfaceRangeMax"]
        if "strContactEmissions" in contact_json:
            # 态势控制——目标电磁辐射显示信息
            contact.strContactEmissions = contact_json["strContactEmissions"]
        if contact.m_OriginalDetectorSide in self.side_dic:
            self.side_dic[contact.m_OriginalDetectorSide].contacts[guid] = contact
        else:
            side = CSide(contact.m_OriginalDetectorSide, self.mozi_server)
            side.contacts[guid]= contact
            self.side_dic[contact.m_OriginalDetectorSide] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2007,"side": contact.m_OriginalDetectorSide}
            
    def parse_group(self,group_json):
        guid = group_json["strGuid"]
        name = group_json["strName"]
        side_guid = group_json["m_Side"]
        group = CGroup()
        if "m_GroupCenter" in group_json:
            group.m_GroupCenter = group_json["m_GroupCenter"]            
        group.strDockAircraft = group_json["strDockAircraft"]
        # 悬停速度
        group.fHoverSpeed = group_json["fHoverSpeed"]
        # 低速
        group.fLowSpeed = group_json["fLowSpeed"]
        # 巡航
        group.fCruiseSpeed = group_json["fCruiseSpeed"]
        # 军用/全速
        group.fMilitarySpeed = group_json["fMilitarySpeed"]
        # 加速/最大
        group.fAddForceSpeed = group_json["fAddForceSpeed"]
        # 期望高度
        group.fDesiredAltitude = group_json["fDesiredAltitude"]
        # 是否在陆地上
        group.bIsOnLand = group_json["bIsOnLand"]
        # 航路点需要燃油数
        group.strWayPointFuel = group_json["strWayPointFuel"]
        # 编组领队
        group.m_GroupLead = group_json["m_GroupLead"]
        # 编组类型
        group.m_GroupType = group_json["m_GroupType"]
        # 载艇按钮的文本描述
        group.strDockShip = group_json["strDockShip"]
        # 编组所有单元GUID
        group.m_UnitsInGroup = group_json["m_UnitsInGroup"]
        # 航路点剩余航行距离
        group.strWayPointDTG = group_json["strWayPointDTG"]
        # 航路点描述
        group.strWayPointDescription = group_json["strWayPointDescription"]
        # 发送队形方案详情
        group.m_FormationFormula = group_json["m_FormationFormula"]
        # 航路点剩余航行时间
        group.strWayPointTTG = group_json["strWayPointTTG"]
        # 发送队形方案选择的索引
        group.iFormationSelectedIndex = group_json["iFormationSelectedIndex"]
        # 航路点名称
        group.strWayPointName = group_json["iFormationSelectedIndex"]
        # from dong
        # 编组中心点经度
        group.m_GroupCenterLongitude = group_json["m_GroupCenterLongitude"]
        # 编组中心点纬度
        group.m_GroupCenterLatitude = group_json["m_GroupCenterLatitude"]
        # 编组中心点高度
        group.m_GroupCenterAltitude_ASL = group_json["m_GroupCenterAltitude_ASL"]
        if side_guid in self.side_dic:
            self.side_dic[side_guid].groups[guid] = group
        else:
            side = CSide(side_guid, self.mozi_server)
            side.groups[guid]= group
            self.side_dic[side_guid] = side
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2008,"side": side_guid}        
            
    def parse_waypoint(self,waypoint_json):
        guid = waypoint_json["strGuid"]
        name = waypoint_json["strName"]
        ActiveUnit = waypoint_json["m_ActiveUnit"]        
        waypoint = CWayPoint(guid, name, ActiveUnit, self.mozi_server)
         # 经度
        waypoint.dLongitude = waypoint_json["dLongitude"]
        # 纬度
        waypoint.dLatitude = waypoint_json["dLatitude"]
        # 高度
        waypoint.fAltitude = waypoint_json["fAltitude"]
        # 路径点类型
        waypoint.m_WaypointType = waypoint_json["m_WaypointType"]
        # 枚举类-进气道压力
        waypoint.m_ThrottlePreset = waypoint_json["m_ThrottlePreset"]
        # 高空压力
        waypoint.m_AltitudePreset = waypoint_json["m_AltitudePreset"]
        # 深潜压力
        waypoint.m_DepthPreset = waypoint_json["m_DepthPreset"]
        # 是否采用地形跟随
        waypoint.bTerrainFollowing = waypoint_json["bTerrainFollowing"]
        # 作战条令
        waypoint.m_Doctrine = waypoint_json["m_Doctrine"]
        # 雷达状态
        waypoint.m_RadarState = waypoint_json["m_RadarState"]
        # 声纳状态
        waypoint.m_SonarState = waypoint_json["m_SonarState"]
        # 电磁干扰状态
        waypoint.m_ECMState = waypoint_json["m_ECMState"]
        # 航路点描述
        waypoint.strWayPointDescription = waypoint_json["strWayPointDescription"]
        # 航路点剩余航行距离
        waypoint.strWayPointDTG = waypoint_json["strWayPointDTG"]
        # 航路点剩余航行时间
        waypoint.strWayPointTTG = waypoint_json["strWayPointTTG"]
        # 航路点需要燃油数
        waypoint.strWayPointFuel = waypoint_json["strWayPointFuel"]
        # 航路点名称
        waypoint.strWayPointName = waypoint_json["strWayPointName"]
        # 预期速度        
        waypoint.fDesiredSpeed = waypoint_json["fDesiredSpeed"]
        # 预期高度
        waypoint.fDesiredAltitude = waypoint_json["fDesiredAltitude"]
        # 温跃层上
        waypoint.nThermoclineUpDepth = waypoint_json["nThermoclineUpDepth"]
        # 温跃层下
        waypoint.nThermoclineDownDepth = waypoint_json["nThermoclineDownDepth"]          
        self.waponit_dic[guid] = waypoint
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 1005}             
        
    def parse_weather(self,weather_json):      
        weather = CWeather(self.mozi_server)
        weather.fSkyCloud = weather_json["fSkyCloud"]
        weather.fRainFallRate = weather_json["fRainFallRate"]
        weather.dTemperature = weather_json["dTemperature"]
        weather.iSeaState = weather_json["iSeaState"]
        self.weather = weather
        
    def parse_referencePoint(self,referencePoint_json):
        guid = referencePoint_json["strGuid"]
        name = referencePoint_json["strName"]
        side_guid = referencePoint_json["m_Side"]         
        referencePoint = CReferencePoint(guid, name, side_guid)
        # 经度
        referencePoint.dLongitude = referencePoint_json["dLongitude"]
        # 纬度
        referencePoint.dLatitude = referencePoint_json["dLatitude"]
        # 高度
        referencePoint.fAltitude = referencePoint_json["fAltitude"]
        # 相对单元guid
        referencePoint.m_RelativeToUnit = referencePoint_json["m_RelativeToUnit"]
        # 相对方位角
        referencePoint.fRelativeBearing = referencePoint_json["fRelativeBearing"]
        # 相对距离
        referencePoint.fRelativeDistance = referencePoint_json["fRelativeDistance"]
        # 方向类型
        # 0 固定的，不随领队朝向变化而变化
        # 1 旋转的，随领队朝向改变旋转
        referencePoint.m_BearingType = referencePoint_json["m_BearingType"]
        # 是否锁定
        referencePoint.bIsLocked = referencePoint_json["bIsLocked"]   
        if side_guid in self.side_dic:
            self.side_dic[side_guid].referencePoints[guid] = referencePoint
        else:
            side = CSide(side_guid, self.mozi_server)
            side.referencePoints[guid]= referencePoint
            self.side_dic[side_guid] = side 
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2009,"side": side_guid}             
            
      
        
    def parse_side(self ,side_json):
        side_guid=side_json["strGuid"]
        if side_guid in self.side_dic:
            side = self.side_dic[side_guid]
        else:
            side = CSide(side_guid, self.mozi_server)        
        #side.current_point = side_json["current_point"]  # 当前得分
        #side.point_record = side_json["point_record"] # 得分记录
        #side.simulate_time = side_json["simulate_time"] # 当前推演时间
        #side.last_step_missing = side_json["last_step_missing"] # 当前决策步损失的单元（我方），丢掉或击毁的单元（敌方）
        #side.last_step_new = side_json["last_step_new"] # 当前决策步新增的单元（我方），新增的情报单元（敌方）
        #side.all_units = side_json["all_units"]
        #side.activeunit  = side_json["activeunit"]
        if 'strName' in side_json:
            side.strName = side_json["strName"]  # 名称
        if 'm_PosturesDictionary' in side_json:
            side.m_PosturesDictionary=side_json["m_PosturesDictionary"]#获取针对其它推演方的立场
        #side.m_Doctrine=side_json["m_Doctrine"]#作战条令                                   
        #side.m_ProficiencyLevel=side_json["m_ProficiencyLevel"]
        #side.m_AwarenessLevel=side_json["m_AwarenessLevel"]
        #side.iTotalScore=side_json["iTotalScore"]
        #side.m_Expenditures=side_json["m_Expenditures"]#战损           
        #side.m_Losses=side_json["m_Losses"]#战耗
        #side.iScoringDisaster=side_json["iScoringDisaster"]# 完败阀值          
        #side.iScoringTriumph=side_json["iScoringTriumph"]#完胜阀值
        #side.bCATC=side_json["bCATC"]#自动跟踪非作战单元
        #side.bCollectiveResponsibility=side_json["bCollectiveResponsibility"]#集体反应
        #side.bAIOnly=side_json["bAIOnly"]#只由计算机扮演
        #side.strBriefing=side_json["strBriefing"]#简要 
        #side.strCloseResult=side_json["strCloseResult"]#战斗结束后的结果
        if 'fCamerAltitude' in side_json:
            side.fCamerAltitude=side_json["fCamerAltitude"]#中心点相机高度
        if 'fCenterLatitude' in side_json:
            side.fCenterLatitude=side_json["fCenterLatitude"] #地图中心点纬度
        if 'fCenterLongitude' in side_json:
            side.fCenterLongitude=side_json["fCenterLongitude"] #地图中心点经度
        if 'strSideColorKey' in side_json:
            side.strSideColorKey=side_json["strSideColorKey"] #推演方颜色Key
        if 'strFriendlyColorKey' in side_json:
            side.strFriendlyColorKey=side_json["strFriendlyColorKey"] #友方颜色Key
        if 'strNeutralColorKey' in side_json:
            side.strNeutralColorKey=side_json["strNeutralColorKey"] #中立方颜色Key
        if 'strUnfriendlyColorKey' in side_json:
            side.strUnfriendlyColorKey =side_json["strUnfriendlyColorKey"]#非友方颜色Key
        if 'strHostileColorKey' in side_json:
            side.strHostileColorKey=side_json["strHostileColorKey"] #敌方颜色Key
        #side.iSideStopCount =side_json["iSideStopCount"] #推演方剩余停止次数                    
        #side.m_ScoringLogs =side_json["m_ScoringLogs"]
        #side.m_ContactList=side_json["m_ContactList"] #所有的目标
        #side.m_WarDamageOtherTotal=side_json["m_WarDamageOtherTotal"] #战损的其它统计，包含但不限于(统计损失单元带来的经济和人员损失)
        self.side_dic[side_guid] = side
        if side_guid not in self.all_guid_info:
            self.all_guid_info[side_guid] = {"strType" : 1006}
    
    def parse_mission(self,mission_json):
        name = mission_json["strName"]
        guid = mission_json["strGuid"]
        side_guid = mission_json["m_Side"]
        mission = CMission(guid, name, side_guid, self.mozi_server)
        # 任务类别
        mission.m_Category = mission_json["m_Category"]
        # 任务类型
        mission.m_MissionClass = mission_json["m_MissionClass"]
        # 任务状态side_guidside_guidside_guidside_guidside_guid
        mission.m_MissionStatus = mission_json["m_MissionStatus"]
        # 飞机设置-编队规模
        mission.m_FlightSize = mission_json["m_FlightSize"]
        # 空中加油任务设置-任务执行设置 -加油机遵循受油机的飞行计划是否选中
        mission.bTankerFollowsReceivers = mission_json["bTankerFollowsReceivers"]
        # 任务描述
        mission.strDescription = mission_json["strDescription"]
        # 空中加油任务设置-任务规划设置 加油机没到位的情况下启动任务
        mission.bLaunchMissionWithoutTankersInPlace = mission_json["bLaunchMissionWithoutTankersInPlace"]
        # 水面舰艇/潜艇设置-水面舰艇/潜艇树低于编队规模要求,不能出击(根据基地编组)
        mission.bUseGroupSizeHardLimit = mission_json["bUseGroupSizeHardLimit"]
        # 已分配单元的集合
        mission.m_AssignedUnits = mission_json["m_AssignedUnits"]
        # 空中加油任务设置-任务执行设置 - 每架加油机允许加油队列最大长度
        mission.strMaxReceiversInQueuePerTanker_Airborne = mission_json["strMaxReceiversInQueuePerTanker_Airborne"]
        # 水面舰艇/潜艇设置-编队规模
        mission.m_GroupSize = mission_json["m_GroupSize"]
        # 空中加油-  点击配置  显示如下两个选项： 返回选中的值1.使用优良充足的最近加油机加油2.使用已分配特定任务的加油机加油
        mission.m_TankerUsage = mission_json["m_TankerUsage"]
        # 条令
        mission.m_Doctrine = mission_json["m_Doctrine"]
        # 空中加油任务设置-任务规划设置 阵位上加油机最小数量
        mission.strTankerMinNumber_Station = mission_json["strTankerMinNumber_Station"]
        # 未分配单元的集合
        mission.m_UnassignedUnits = mission_json["m_UnassignedUnits"]
        # 单元航线
        mission.m_strSideWayGUID = mission_json["m_strSideWayGUID"]
        # 空中加油任务设置-任务执行设置 -受油机寻找加油机的时机条件
        mission.strFuelQtyToStartLookingForTanker_Airborne = mission_json["strFuelQtyToStartLookingForTanker_Airborne"]
        # 空中加油选项是否与上级保持一致
        mission.bUseRefuel = mission_json["bUseRefuel"]
        # 飞机数低于编队规模要求,不能起飞
        mission.bUseFlightSizeHardLimit = mission_json["bUseFlightSizeHardLimit"]
        # 飞机设置-空中加油
        mission.m_UseRefuel = mission_json["m_UseRefuel"]
        # 行动预案
        mission.bUseActionPlan = mission_json["bUseActionPlan"]
        # 空中加油任务设置-任务规划设置 留空的加油机最小数量
        mission.strTankerMinNumber_Airborne = mission_json["strTankerMinNumber_Airborne"]
        # 空中加油任务设置-任务规划设置1.需要加油机的最小数量
        mission.strTankerMinNumber_Total = mission_json["strTankerMinNumber_Total"]      
        if side_guid in self.side_dic:
            self.side_dic[side_guid].missions[guid] = mission
        else:
            side = CSide(side_guid, self.mozi_server)
            side.missions[guid] = mission
            self.side_dic[side_guid] = side  
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2010,"side": side_guid}              
        
    
    def parse_scenario(self ,scenario_json,scenario):
        # GUID
        scenario.strGuid = scenario_json["strGuid"]
        if "strTitle" in scenario_json:
            scenario.strTitle = scenario_json["strTitle"]
        if "strScenFileName" in scenario_json:
            # 想定文件名
            scenario.strScenFileName = scenario_json["strScenFileName"]
        if "strDescription" in scenario_json:
            # 描述
            scenario.strDescription = scenario_json["strDescription"]
        if "m_Time" in scenario_json:
            # 当前时间
            scenario.m_Time = scenario_json["m_Time"]
        if "bDaylightSavingTime" in scenario_json:
            # 是否是夏令时
            scenario.bDaylightSavingTime = scenario_json["bDaylightSavingTime"]
        if "m_FirstTimeRunDateTime" in scenario_json:
            # 当前想定第一次启动的开始时间
            scenario.m_FirstTimeRunDateTime = scenario_json["m_FirstTimeRunDateTime"]
        ## 用不上
        #scenario.m_FirstTimeLastProcessed = scenario_json["m_FirstTimeLastProcessed"]
        ## 用不上
        #scenario.m_grandTimeLastProcessed = scenario_json["m_grandTimeLastProcessed"]
        ## 夏令时开始时间（基本不用）
        #scenario.strDaylightSavingTime_Start = scenario_json["strDaylightSavingTime_Start"]
        ## 夏令结束时间（基本不用）
        #scenario.strDaylightSavingTime_End = scenario_json["strDaylightSavingTime_End"]
        if "m_StartTime" in scenario_json:
            # 想定开始时间
            scenario.m_StartTime = scenario_json["m_StartTime"]
        if "m_Duration" in scenario_json:
            # 想定持续时间
            scenario.m_Duration = scenario_json["m_Duration"]
        if "sMeta_Complexity" in scenario_json:
            # 想定精细度
            scenario.sMeta_Complexity = scenario_json["sMeta_Complexity"]
        if "sMeta_Difficulty" in scenario_json:
            # 想定困难度
            scenario.sMeta_Difficulty = scenario_json["sMeta_Difficulty"]
        if "strMeta_ScenSetting" in scenario_json:
            # 想定发生地
            scenario.strMeta_ScenSetting = scenario_json["strMeta_ScenSetting"]
        if "strDeclaredFeatures" in scenario_json:
            # 想定精细度的枚举类集合
            scenario.strDeclaredFeatures = scenario_json["strDeclaredFeatures"]
        if "strCustomFileName" in scenario_json:
            # 想定的名称
            scenario.strCustomFileName = scenario_json["strCustomFileName"]
        if "iEditCountDown" in scenario_json:
            # 编辑模式剩余时间
            scenario.iEditCountDown = scenario_json["iEditCountDown"]
        if "iStartCountDown" in scenario_json:
            # 推演模式剩余时间
            scenario.iStartCountDown = scenario_json["iStartCountDown"]
        if "iSuspendCountDown" in scenario_json:
            # 暂停剩余时间
            scenario.iSuspendCountDown = scenario_json["iSuspendCountDown"]
        if "m_CurrentStage" in scenario_json:
            # 获取推演的阶段模式
            scenario.m_CurrentStage = scenario_json["m_CurrentStage"]
        if "m_sides" in scenario_json:
            #推演方
            scenario.m_sides = scenario_json["m_sides"]
        
        
    def paser_activeunit(self , activeunit_json , activeunit):
        if "strUnitClass" in activeunit_json:
            # 实体类别
            activeunit.strUnitClass = activeunit_json["strUnitClass"]
        if "dLatitude" in activeunit_json:
            # 当前纬度
            activeunit.dLatitude = activeunit_json["dLatitude"]
        if "dLongitude" in activeunit_json:
            # 当前经度
            activeunit.dLongitude = activeunit_json["dLongitude"]
        if "fCurrentHeading" in activeunit_json:
            # 当前朝向
            activeunit.fCurrentHeading = activeunit_json["fCurrentHeading"]
        if "fCurrentSpeed" in activeunit_json:
            # 当前速度
            activeunit.fCurrentSpeed = activeunit_json["fCurrentSpeed"]
        if "fCurrentAltitude_ASL" in activeunit_json:
            # 当前海拔高度
            activeunit.fCurrentAltitude_ASL = activeunit_json["fCurrentAltitude_ASL"]
        if "fPitch" in activeunit_json:
            # 倾斜角
            activeunit.fPitch = activeunit_json["fPitch"]
        if "fRoll" in activeunit_json:
            # 翻转角
            activeunit.fRoll = activeunit_json["fRoll"]
        if "bIsOnLand" in activeunit_json:
            # 是否在陆地上
            activeunit.bIsOnLand = activeunit_json["bIsOnLand"]
        if "m_MatchingDBIDList" in activeunit_json:
            # 可能匹配结果
            activeunit.m_MatchingDBIDList = activeunit_json["m_MatchingDBIDList"]
        if "strRadiantPoint" in activeunit_json:
            # 识别出的辐射平台
            activeunit.strRadiantPoint = activeunit_json["strRadiantPoint"]
        if "strIconType" in activeunit_json:
            activeunit.strIconType = activeunit_json["strIconType"]
        if "strCommonIcon" in activeunit_json:
            activeunit.strCommonIcon = activeunit_json["strCommonIcon"]
        if "m_ContactType" in activeunit_json:
            # 目标类型
            activeunit.m_ContactType = activeunit_json["m_ContactType"]
        if "bSideIsKnown" in activeunit_json:
            # 属方是否已知
            activeunit.bSideIsKnown = activeunit_json["bSideIsKnown"]
        if "m_IdentificationStatus" in activeunit_json:
            # 单元的识别状态
            activeunit.m_IdentificationStatus = activeunit_json["m_IdentificationStatus"]
        if "m_ActualUnit" in activeunit_json:
            # 本身单元的GUID
            activeunit.m_ActualUnit = activeunit_json["m_ActualUnit"]
        if "m_OriginalDetectorSide" in activeunit_json:
            # 探测到的推演方
            activeunit.m_OriginalDetectorSide = activeunit_json["m_OriginalDetectorSide"]
        if "m_SidePostureStanceDictionary" in activeunit_json:
            # 其它推演方对本目标的立场姿态
            activeunit.m_SidePostureStanceDictionary = activeunit_json["m_SidePostureStanceDictionary"]
        if "bSpeedKnown" in activeunit_json:
            # 速度是否已知
            activeunit.bSpeedKnown = activeunit_json["bSpeedKnown"]
        if "bHeadingKnown" in activeunit_json:
            # 朝向是否已知
            activeunit.bHeadingKnown = activeunit_json["bHeadingKnown"]
        if "bAltitudeKnown" in activeunit_json:
            # 高度是否已知
            activeunit.bAltitudeKnown = activeunit_json["bAltitudeKnown"]
        if "strElectromagnetismEradiateTitle" in activeunit_json:
            # 电磁辐射Title
            activeunit.strElectromagnetismEradiateTitle = activeunit_json["strElectromagnetismEradiateTitle"]
        if "strElectromagnetismEradiate" in activeunit_json:
            # 电磁辐射集合
            activeunit.strElectromagnetismEradiate = activeunit_json["strElectromagnetismEradiate"]
        if "strMatchingTitle" in activeunit_json:
            # 匹配结果标题
            activeunit.strMatchingTitle = activeunit_json["strMatchingTitle"]
        if "m_DetectionRecord" in activeunit_json:
            # 侦察记录
            activeunit.m_DetectionRecord = activeunit_json["m_DetectionRecord"]
        if "m_UncertaintyArea" in activeunit_json:
            # 不确定区域集合
            activeunit.m_UncertaintyArea = activeunit_json["m_UncertaintyArea"]
        if "strAge" in activeunit_json:
            # 目标持续时间
            activeunit.strAge = activeunit_json["strAge"]
        if "fMaxDetectRange" in activeunit_json:
            # 取目标发射源容器中传感器的最大探测距离
            activeunit.fMaxDetectRange = activeunit_json["fMaxDetectRange"]
        if "fMaxRange_DetectSurfaceAndFacility" in activeunit_json:
            # 获取最大对海探测范围
            activeunit.fMaxRange_DetectSurfaceAndFacility = activeunit_json["fMaxRange_DetectSurfaceAndFacility"]
        if "fMaxRange_DetectSubsurface" in activeunit_json:
            # 获取最大对潜探测范围
            activeunit.fMaxRange_DetectSubsurface = activeunit_json["fMaxRange_DetectSubsurface"]
        if "fTimeSinceDetection_Visual" in activeunit_json:
            # 获取目标探测时间
            activeunit.fTimeSinceDetection_Visual = activeunit_json["fTimeSinceDetection_Visual"]
        if "iWeaponsAimingAtMe" in activeunit_json:
            # 获取瞄准目标的武器数量
            activeunit.iWeaponsAimingAtMe = activeunit_json["iWeaponsAimingAtMe"]
        if "fAirRangeMax" in activeunit_json:
            # 目标武器对空最大攻击距离
            activeunit.fAirRangeMax = activeunit_json["fAirRangeMax"]
        if "fSurfaceRangeMax" in activeunit_json:
            # 目标武器对海最大攻击距离
            activeunit.fSurfaceRangeMax = activeunit_json["fSurfaceRangeMax"]
        if "fLandRangeMax" in activeunit_json:
            # 目标武器对陆最大攻击距离
            activeunit.fLandRangeMax = activeunit_json["fLandRangeMax"]
        if "fSubsurfaceRangeMax" in activeunit_json:
            # 目标武器对潜最大攻击距离
            activeunit.fSubsurfaceRangeMax = activeunit_json["fSubsurfaceRangeMax"]
        if "strContactEmissions" in activeunit_json:
            # 态势控制——目标电磁辐射显示信息
            activeunit.strContactEmissions = activeunit_json["strContactEmissions"]
            
        if "m_Magazines" in activeunit_json:
            # 态势控制——目标电磁辐射显示信息
            activeunit.m_Magazines = activeunit_json["m_Magazines"]
            mgazines_list=activeunit.m_Magazines.split('@')
            for mgazine in mgazines_list:
                if mgazine in self.all_guid_info:
                    self.bind_activeUnit(activeunit, mgazine,'magazine')
            
        if "m_LoadoutGuid" in activeunit_json:
            # 态势控制——目标电磁辐射显示信息
            activeunit.m_LoadoutGuid= activeunit_json["m_LoadoutGuid"]
            loadoutGuid_list=activeunit.m_LoadoutGuid.split('@')
            for loadout in loadoutGuid_list:
                if loadout in self.all_guid_info:
                    self.bind_activeUnit(activeunit, loadout,'loadout')            
        if "m_Mounts" in activeunit_json:
            # 态势控制——目标电磁辐射显示信息
            activeunit.m_Mounts = activeunit_json["m_Mounts"]
            mounts_list=activeunit.m_Mounts.split('@')
            for mount in mounts_list:
                if mount in self.all_guid_info:
                    self.bind_activeUnit(activeunit, mount,'mount')            
        if "m_Sensors" in activeunit_json:
            # 态势控制——目标电磁辐射显示信息
            activeunit.m_Sensors = activeunit_json["m_NoneMCMSensors"]
            sensors_list=activeunit.m_Sensors.split('@')
            for sensor in sensors_list:
                if sensor in self.all_guid_info:
                    self.bind_activeUnit(activeunit, sensor,'sensor')             
        
        
    def parse_loggedmessage(self ,loggedmessage_json):
        guid = loggedmessage_json["strGuid"]
        side_guid = loggedmessage_json["m_Side"]  
        loggedmessage=CLoggedMessage(guid, side_guid)
        # 事件的内容
        loggedmessage.MessageText = loggedmessage_json["MessageText"]
        # 消息发生的时间
        loggedmessage.TStamp = loggedmessage_json["TStamp"]
        # 消息类型
        loggedmessage.MessageType = loggedmessage_json["MessageType"]
        # 消息编号
        loggedmessage.Increment = loggedmessage_json["Increment"]
        # 等级
        loggedmessage.iLevel = loggedmessage_json["iLevel"]
        # 经度
        loggedmessage.Longitude = loggedmessage_json["Longitude"]
        # 纬度
        loggedmessage.Latitude = loggedmessage_json["Latitude"]
        # 报告者GUID
        loggedmessage.ReporterID = loggedmessage_json["ReporterID"]
        # 事件关联的目标本身单元的GUID
        loggedmessage.ContactActiveUnitGUID = loggedmessage_json["ContactActiveUnitGUID"]   
        if side_guid in self.side_dic:
            self.side_dic[side_guid].logged_messages[guid] = loggedmessage
        else:
            side = CSide(side_guid, self.mozi_server)
            side.logged_messages[guid] = loggedmessage
            self.side_dic[side_guid] = side            
        if guid not in self.all_guid_info:
            self.all_guid_info[guid] = {"strType" : 2011,"side": side_guid}
            
    def parse_Doctrine(self ,doctrine_json):
        doctrine = CDoctrine(self.mozi_server)
        # 条令的拥有者GUID（具体作用对象）
        doctrine.m_DoctrineOwner =  doctrine_json["m_DoctrineOwner"]
        # 核武器使用规则
        doctrine.m_Nukes = doctrine_json["m_Nukes"]
        # 对空目标武器控制规则
        doctrine.m_WCS_Air = doctrine_json["m_WCS_Air"]
        # 对海目标武器控制规则C
        doctrine.m_WCS_Surface = doctrine_json["m_WCS_Surface"]
        # 对潜目标武器控制规则
        doctrine.m_WCS_Submarine = doctrine_json["m_WCS_Submarine"]
        # 对地目标武器控制规则
        doctrine.m_WCS_Land = doctrine_json["m_WCS_Land"]
        # 进攻时是否忽略绘制航线规则
        doctrine.m_IgnorePlottedCourseWhenAttacking = doctrine_json["m_IgnorePlottedCourseWhenAttacking"]
        # 对不明目标的行为态度规则
        doctrine.m_BehaviorTowardsAmbigousTarget = doctrine_json["m_BehaviorTowardsAmbigousTarget"]
        # 对临机目标进行射击规则
        doctrine.m_ShootTourists = doctrine_json["m_ShootTourists"]
        # 受攻击时是否考虑电磁管控规则
        doctrine.m_IgnoreEMCONUnderAttack = doctrine_json["m_IgnoreEMCONUnderAttack"]
        # 鱼雷使用动力航程规则
        doctrine.m_UseTorpedoesKinematicRange = doctrine_json["m_UseTorpedoesKinematicRange"]
        # 是否自动规避目标规则
        doctrine.m_AutomaticEvasion = doctrine_json["m_AutomaticEvasion"]
        # 是否可加油/补给规则
        doctrine.m_UseRefuel = doctrine_json["m_UseRefuel"]
        # 对所选单元加油/补给时加油机选择规则
        doctrine.m_RefuelSelection = doctrine_json["m_RefuelSelection"]
        # 与盟军单元加油/补给规则
        doctrine.m_RefuelAllies = doctrine_json["m_RefuelAllies"]
        # 空战节奏规则
        doctrine.m_AirOpsTempo = doctrine_json["m_AirOpsTempo"]
        # 快速出动规则
        doctrine.m_QuickTurnAround = doctrine_json["m_QuickTurnAround"]
        # 预先规划终止任务返回基地油量阈值规则
        doctrine.m_BingoJoker = doctrine_json["m_BingoJoker"]
        # 编组成员达到预先规划油量状态时编组或成员返回基地规则
        doctrine.m_BingoJokerRTB = doctrine_json["m_BingoJokerRTB"]
        # 预先规划武器使用规则、武器状态与平台脱离战斗规则
        doctrine.m_WeaponState = doctrine_json["m_WeaponState"]
        # 编组成员达到预先规划武器状态时，编组或成员返回基地规则
        doctrine.m_WeaponStateRTB = doctrine_json["m_WeaponStateRTB"]
        # 航炮是否对地面目标扫射规则
        doctrine.m_GunStrafeGroundTargets = doctrine_json["m_GunStrafeGroundTargets"]
        # 受到攻击时是否抛弃弹药规则
        doctrine.m_JettisonOrdnance = doctrine_json["m_JettisonOrdnance"]
        # 以反舰模式使用舰空导弹规则
        doctrine.m_SAM_ASUW = doctrine_json["m_SAM_ASUW"]
        # 与目标保持一定距离规则
        doctrine.m_MaintainStandoff = doctrine_json["m_MaintainStandoff"]
        # 尽可能规避目标规则
        doctrine.m_AvoidContact = doctrine_json["m_AvoidContact"]
        # 探测到威胁目标后下潜规则
        doctrine.m_DiveWhenThreatsDetected = doctrine_json["m_DiveWhenThreatsDetected"]
        # 巡逻任务充电时电池剩余电量规则
        doctrine.m_RechargePercentagePatrol = doctrine_json["m_RechargePercentagePatrol"]
        # 进攻战充电时电池剩余电量规则
        doctrine.m_RechargePercentageAttack = doctrine_json["m_RechargePercentageAttack"]
        # AIP推进技术使用规则
        doctrine.m_AIPUsage = doctrine_json["m_AIPUsage"]
        # 吊放声呐使用规则
        doctrine.m_DippingSonar = doctrine_json["m_DippingSonar"]
        # 毁伤达到阈值时应撤退规则
        doctrine.m_WithdrawDamageThreshold = doctrine_json["m_WithdrawDamageThreshold"]
        # 油量达到阈值时应撤退规则
        doctrine.m_WithdrawFuelThreshold = doctrine_json["m_WithdrawFuelThreshold"]
        # 进攻战武器数量达到阈值应撤退规则
        doctrine.m_WithdrawAttackThreshold = doctrine_json["m_WithdrawAttackThreshold"]
        # 防御战武器数量达到阈值应撤退规则
        doctrine.m_WithdrawDefenceThreshold = doctrine_json["m_WithdrawDefenceThreshold"]
        # 毁伤达到阈值时应重新部署规则
        doctrine.m_RedeployDamageThreshold = doctrine_json["m_RedeployDamageThreshold"]
        # 油量达到阈值时应重新部署规则
        doctrine.m_RedeployFuelThreshold = doctrine_json["m_RedeployFuelThreshold"]
        # 进攻战武器数量达到阈值时应重新部署规则
        doctrine.m_RedeployAttackDamageThreshold = doctrine_json["m_RedeployAttackDamageThreshold"]
        # 防御战武器数量达到阈值时应重新部署规则
        doctrine.m_RedeployDefenceDamageThreshold = doctrine_json["m_RedeployDefenceDamageThreshold"]
        # 电磁管控设置是否有值
        doctrine.m_bEMCON_AccordingSuperior = doctrine_json["m_bEMCON_AccordingSuperior"]
        # 雷达管控规则设置模式
        doctrine.m_EMCON_SettingsForRadar = doctrine_json["m_EMCON_SettingsForRadar"]
        # 声呐管控规则设置模式
        doctrine.m_EMCON_SettingsForSonar = doctrine_json["m_EMCON_SettingsForSonar"]
        # 进攻型电子对抗措施（干扰机）管控规则设置模式
        doctrine.m_EMCON_SettingsForOECM = doctrine_json["m_EMCON_SettingsForOECM"]
        # 武器使用规则的武器DBID
        doctrine.m_WRA_WeaponRule_WeaponDBID = doctrine_json["m_WRA_WeaponRule_WeaponDBID"]
        # 武器使用规则
        doctrine.m_WRA_WeaponRule = doctrine_json["m_WRA_WeaponRule"]
        # 使用核武器
        doctrine.bchkUseNuclerWeapon = doctrine_json["bchkUseNuclerWeapon"]
        # 武器控制状态对空是否允许用户编辑
        doctrine.bchkWeaponStateAir = doctrine_json["bchkWeaponStateAir"]
        # 武器控制状态对海是否允许用户编辑
        doctrine.bchkWeaponStateSea = doctrine_json["bchkWeaponStateSea"]
        # 武器控制状态对潜是否允许用户编辑
        doctrine.bchkWeaponStateSeaLatent = doctrine_json["bchkWeaponStateSeaLatent"]
        # 武器控制状态对地是否允许用户编辑
        doctrine.bchkWeaponStateland = doctrine_json["bchkWeaponStateland"]
        # 受到攻击时忽略计划航线是否允许用户编辑
        doctrine.bchkIgnoreRoutes = doctrine_json["bchkIgnoreRoutes"]
        # 接战模糊位置目标是否允许用户编辑
        doctrine.bchkFuzzlocationOfTheReceIvingstation = doctrine_json["bchkFuzzlocationOfTheReceIvingstation"]
        # 接战临机出现目标是否允许用户编辑
        doctrine.bchkImminentTarget = doctrine_json["bchkImminentTarget"]
        # 受攻击时忽略电磁管控是否允许用户编辑
        doctrine.bchkIgnoreElectromagneticControl = doctrine_json["bchkIgnoreElectromagneticControl"]
        # 鱼雷使用动力航程是否允许用户编辑
        doctrine.bchkTopedopower = doctrine_json["bchkTopedopower"]
        # 自动规避是否允许用户编辑
        doctrine.bchkAutoAcoid = doctrine_json["bchkAutoAcoid"]
        # 加油/补给是否允许用户编辑
        doctrine.bchkComeOn = doctrine_json["bchkComeOn"]
        # 对所选单元进行加油/补给是否允许用户编辑
        doctrine.bchkSelectUnitComeOn = doctrine_json["bchkSelectUnitComeOn"]
        # 对盟军单元进行加油/补给是否允许用户编辑
        doctrine.bchkAlliedUnitComeOn = doctrine_json["bchkAlliedUnitComeOn"]
        # 空战节奏是否允许用户编辑
        doctrine.bchkAirOpsTempo_Player = doctrine_json["bchkAirOpsTempo_Player"]
        # 快速出动是否允许用户编辑
        doctrine.bchkQTA_Player = doctrine_json["bchkQTA_Player"]
        # 燃油状态，预先规划是否允许用户编辑
        doctrine.bchkBingoJoker_Player = doctrine_json["bchkBingoJoker_Player"]
        # 燃油状态—返航是否允许用户编辑
        doctrine.bchkBingoJokerRTB_Player = doctrine_json["bchkBingoJokerRTB_Player"]
        # 武器状态, 预先规划是否允许用户编辑
        doctrine.bchkWeaponStateFirast = doctrine_json["bchkWeaponStateFirast"]
        # 武器状态-返航是否允许用户编辑
        doctrine.bchkWeaponStateReturn = doctrine_json["bchkWeaponStateReturn"]
        # 空对地扫射(航炮)是否允许用户编辑
        doctrine.bchkAirToGroundUserEdit = doctrine_json["bchkAirToGroundUserEdit"]
        # 抛弃弹药是否允许用户编辑
        doctrine.bchkAbandonedAmmunition = doctrine_json["bchkAbandonedAmmunition"]
        # 以反舰模式使用舰空导弹规则是否允许用户编辑
        doctrine.bchkSAM_ASUW_Player = doctrine_json["bchkSAM_ASUW_Player"]
        # 与目标保持一定距离规则是否允许用户编辑
        doctrine.bchkKeepTargetDistance = doctrine_json["bchkKeepTargetDistance"]
        # 规避搜索规则是否允许用户编辑
        doctrine.bchkToAvoidTheSearch = doctrine_json["bchkToAvoidTheSearch"]
        # 探测到威胁进行下潜规则是否允许用户编辑
        doctrine.bchkThreatWasDetectedAndDived = doctrine_json["bchkThreatWasDetectedAndDived"]
        # 电池充电 %, 出航/阵位是否允许用户编辑
        doctrine.bchkSetSail = doctrine_json["bchkSetSail"]
        # 电池充电%, 进攻/防御是否允许用户编辑
        doctrine.bchkAttack = doctrine_json["bchkAttack"]
        # 使用AIP推进技术是否允许用户编辑
        doctrine.bchkAPI = doctrine_json["bchkAPI"]
        # 吊放声纳是否允许用户编辑
        doctrine.bchkDippingSonar = doctrine_json["bchkDippingSonar"]
        #条令是条令目标对象的guid，使用时应该查找
        self.doctrine[doctrine.m_DoctrineOwner] =doctrine
        if doctrine.m_DoctrineOwner not in self.all_guid_info:
            self.all_guid_info[doctrine.m_DoctrineOwner] = {"strType" : 1007}        
        
        
    def parse_simEvent(self , simEvent_json):
        simEvent =  CSimEvent(self.mozi_server)
        simEvent.strName = simEvent_json["strName"]
        simEvent.strGuid = simEvent_json["strGuid"]
        simEvent.strDescription = simEvent_json["strDescription"]
        simEvent.bIsRepeatable = simEvent_json["bIsRepeatable"]
        simEvent.bIsActive = simEvent_json["bIsActive"]
        simEvent.bIsMessageShown = simEvent_json["bIsMessageShown"]
        simEvent.sProbability = simEvent_json["sProbability"]
        simEvent.m_Triggers = simEvent_json["m_Triggers"]
        simEvent.m_Conditions = simEvent_json["m_Conditions"]
        simEvent.m_Actions = simEvent_json["m_Actions"]  
        self.simEvent_dic[simEvent.strGuid] = simEvent
        if simEvent.strGuid not in self.all_guid_info:
            self.all_guid_info[simEvent.strGuid] = {"strType" : 1008}
            
    def parse_delete(self,delete_json):
        '''
        解析删除命令，删除对应对象，并删除查询字典
        如果找不到返回
        '''
        guid =  delete_json["strGuid"]
        if guid in self.all_guid_info:
            guid_info = self.all_guid_info[guid]
            strType =  guid_info["strType"]
            if strType > 2000:
                side_guid = guid_info["side"]
                if strType == 2001:
                    #ship
                    self.side_dic[side_guid].ships.pop(guid)
                elif  strType == 2002:
                    #satellite
                    self.side_dic[side_guid].satellite.pop(guid)
                elif  strType == 2003:
                    #submarine
                    self.side_dic[side_guid].submarines.pop(guid)
                elif  strType == 2004:
                    #weapon
                    self.side_dic[side_guid].weapons.pop(guid)
                elif  strType == 2005:
                    #aircraft
                    self.side_dic[side_guid].aircrafts.pop(guid)
                elif  strType == 2006:
                    #facility
                    self.side_dic[side_guid].facilitys.pop(guid)
                elif  strType == 2007:
                    #contact
                    self.side_dic[side_guid].contacts.pop(guid)
                elif  strType == 2008:
                    #group
                    self.side_dic[side_guid].groups.pop(guid)
                elif  strType == 2009:
                    #referencePoint
                    self.side_dic[side_guid].referencePoints.pop(guid)
                elif  strType == 2010:
                    #mission
                    self.side_dic[side_guid].missions.pop(guid)
                elif  strType == 2011:
                    #loggedmessage
                    self.side_dic[side_guid].logged_messages.pop(guid)
                else:
                    return
            else:
                if strType == 1001:
                    #sensor
                    self.sensor_dic.pop(guid)
                elif  strType == 1002:
                    #loadout
                    self.loadout_dic.pop(guid)
                elif  strType == 1003:
                    #magazine
                    self.magazine_dic.pop(guid)
                elif  strType == 1004:
                    #mount
                    self.mount_dic.pop(guid)
                elif  strType == 1005:
                    #waypoint
                    self.waponit_dic.pop(guid)
                elif  strType == 1006:
                    #side
                    self.side_dic.pop(guid)
                elif  strType == 1007:
                    #Doctrine
                    self.doctrine.pop(guid)
                else:
                    return                        
            self.all_guid_info.pop(guid)
                     
            
    def bind_activeUnit(self,obj,guid,element_type=''):
        guid_info = self.all_guid_info[guid]
        strType =  guid_info["strType"]
        if strType > 2000:
            side_guid = guid_info["side"]
            if strType == 2001:
                #ship
                ship = self.side_dic[side_guid].ships[guid]
                return self.bind(ship,obj,element_type)
            elif  strType == 2002:
                #satellite
                satellite = self.side_dic[side_guid].satellite[guid]
                return self.bind(satellite,obj,element_type)
            elif  strType == 2003:
                #submarine
                submarine = self.side_dic[side_guid].submarines[guid]
                return self.bind(submarine,obj,element_type)
            elif  strType == 2004:
                #weapon
                weapon = self.side_dic[side_guid].weapons[guid]
                return  self.bind(weapon,obj,element_type)
            elif  strType == 2005:
                #aircraft
                aircraft = self.side_dic[side_guid].aircrafts[guid]
                return self.bind(aircraft,obj,element_type)
            elif  strType == 2006:
                #facility
                facility = self.side_dic[side_guid].facilitys[guid]
                return self.bind(facility,obj,element_type)
            elif  strType == 2007:
                #contact
                contact = self.side_dic[side_guid].contacts[guid]
                return self.bind(contact,obj,element_type)
            elif  strType == 2008:
                #group
                group = self.side_dic[side_guid].groups[guid]
                return self.bind(group,obj,element_type)
            elif  strType == 2009:
                #referencePoint
                referencePoint = self.side_dic[side_guid].referencePoints[guid]
                return self.bind(referencePoint,obj,element_type)
            elif  strType == 2010:
                #mission
                mission = self.side_dic[side_guid].missions[guid]
                return self.bind(mission,obj,element_type)
            elif  strType == 2011:
                #loggedmessage
                loggedmessage = self.side_dic[side_guid].logged_messages[guid]
                return self.bind(loggedmessage,obj,element_type)
            else:
                return obj
        else:
            if strType == 1001:
                #sensor
                element_type ='sensor'
                sensor= self.sensor_dic[guid]
                return self.bind(obj,sensor,element_type)
            elif  strType == 1002:
                #loadout
                element_type ='loadout'
                loadout= self.loadout_dic[guid]
                return self.bind(obj,loadout,element_type)
            elif  strType == 1003:
                #magazine
                element_type ='magazine'
                magazine= self.magazine_dic[guid]
                return self.bind(obj,magazine,element_type)
            elif  strType == 1004:
                #mount
                element_type ='mount'
                mount= self.mount_dic[guid]
                return self.bind(obj,mount,element_type)
            elif  strType == 1005:
                #waypoint
                element_type ='waypoint'
                waypoint= self.waponit_dic[guid]
                return self.bind(obj,waypoint,element_type)
            elif  strType == 1007:
                #doctrine
                element_type ='doctrine'
                doctrine = self.doctrine[guid]
                return self.bind(obj,doctrine,element_type)
            else:
                return obj
    

    def bind(self,activeunit,element,element_type):
        if element_type == 'sensor':
            activeunit.sensors[element.strGuid] = element
        elif element_type == 'loadout':
            activeunit.loadouts[element.strGuid] = element
        elif element_type == 'magazine':
            activeunit.magazines[element.strGuid] = element
        elif element_type == 'mount':
            activeunit.mounts[element.strGuid] = element
        elif element_type == 'waypoint':
            activeunit.way_points[element.strGuid] = element
        elif element_type == 'doctrine':
            activeunit.m_Doctrine = element
        return activeunit
