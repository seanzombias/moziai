# -*- coding:utf-8 -*-
##########################################################################################################
# File name : CWayPoint.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CWayPoint():
    def __init__(self, guid, name, activeUnit_guid , mozi_server):     
        self.mozi_server = mozi_server
        # 对象名
        self.strName = name
        # guid
        self.strGuid = guid
        # 经度
        self.dLongitude = 0.0
        # 纬度
        self.dLatitude = 0.0
        # 高度
        self.fAltitude = 0.0
        #上一级单元guid
        self.m_ActiveUnit = activeUnit_guid
        # 路径点类型
        self.m_WaypointType = 0
        # 枚举类-进气道压力
        self.m_ThrottlePreset = 0
        # 高空压力
        self.m_AltitudePreset = 0
        # 深潜压力
        self.m_DepthPreset = 0
        # 是否采用地形跟随
        self.bTerrainFollowing = False
        # 作战条令
        self.m_Doctrine = ""
        # 雷达状态
        self.m_RadarState = 0
        # 声纳状态
        self.m_SonarState = 0
        # 电磁干扰状态
        self.m_ECMState = 0
        # 航路点描述
        self.strWayPointDescription = ""
        # 航路点剩余航行距离
        self.strWayPointDTG = ""
        # 航路点剩余航行时间
        self.strWayPointTTG = ""
        # 航路点需要燃油数
        self.strWayPointFuel = ""
        # 航路点名称
        self.strWayPointName = ""
        # 预期速度
        self.fDesiredSpeed = 0.0
        # 预期高度
        self.fDesiredAltitude = 0.0
        # 温跃层上
        self.nThermoclineUpDepth = 0
        # 温跃层下
        self.nThermoclineDownDepth = 0

