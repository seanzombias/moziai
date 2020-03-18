# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : sensor.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################



class CSensor():
    '''传感器'''
    def __init__(self):
        #传感器guid
        self.strGuid =''
        #传感器名称
        self.strName =""
        # 所属单元GUID
        self.m_ParentPlatform = ''
        # 部件状态
        self.m_ComponentStatus = 0
        # 毁伤程度的轻,中,重
        self.m_DamageSeverity = 0
        # 挂载方位
        self.m_CoverageArc = ""
        # 是否开机
        self.bActive = False
        # 传感器类型描述
        self.strDescription = ""
        # 传感器工作状态
        self.strWorkStatus = ""
        # 传感器类型
        self.m_SensorType = 0
        # 传感器角色
        self.m_SensorRole = ""
        # 最大探测距离
        self.fMaxRange = 0.0
        # 最小探测距离
        self.fMinRange = 0.0
        # 当传感器用作武器指示器时，正在跟踪照射的目标列表数量
        self.i_TrackingTargetsWhenUsedAsDirector = 0
        # 当传感器用作武器指示器时，正在跟踪照射的目标列表集合
        self.m_TrackingTargetsWhenUsedAsDirector = ""
        # 传感器能力
        self.m_SensorCapability = ""
        # 对空探测
        self.airSearch = False
        # 对地/海面搜索
        self.surfaceSearch = False
        # 潜艇搜索
        self.submarineSearch = False
        # 地面搜索-移动设备
        self.landSearch_Mobile = False
        # 地面搜索-固定设施
        self.landSearch_Fixed = False
        # 潜望镜搜索
        self.periscopeSearch = False
        # 太空搜索-ABM （反弹道导弹）
        self.ABM_SpaceSearch = False
        # 水/地雷与障碍物搜索
        self.m_bMineObstacleSearch = False
        # 距离信息
        self.rangeInformation = False
        # 航向信息
        self.headingInformation = False
        # 高度信息
        self.altitudeInformation = False
        # 速度信息
        self.speedInformation = False
        # 仅导航
        self.navigationOnly = False
        # 仅地面测绘
        self.groundMappingOnly = False
        # 仅地形回避/跟随
        self.terrainAvoidanceOrFollowing = False
        # 仅气象探测
        self.weatherOnly = False
        # 仅气象探测与导航
        self.weatherAndNavigation = False
        # OTH-B （后向散射超视距雷达）
        self.OTH_Backscatter = False
        # OTH-SW （表面波超视距雷达）
        self.OTH_SurfaceWave = False
        # 鱼雷告警
        self.torpedoWarning = False
        # 导弹逼近告警
        self.missileApproachWarning = False
        self.PS1 = False  # 左弦尾1
        self.PMA1 = False  # 左弦中后1
        self.PMF1 = False  # 左弦中前
        self.PB1 = False  # 左弦首1
        self.SS1 = False  # 右弦尾1
        self.SMA1 = False  # 右弦中后1
        self.SMF1 = False  # 右弦中前1
        self.SB1 = False  # 右弦首1-bow
        self.PS2 = False  # 左弦尾2-stern
        self.PMA2 = False  # 左弦中后2
        self.PMF2 = False  # 左弦中前2
        self.PB2 = False  # 左弦首2
        self.SS2 = False  # 右弦尾2
        self.SMA2 = False  # 右弦中后2
        self.SMF2 = False  # 右弦中前2
        self.SB2 = False  # 右弦首2
        self.select = False #是否需要查找挂载单元

    def hs_scenEdit_set_sensor_switch(self,unit_guid,sensor_guid,is_active):
        '''
        类别：推演使用函数
        函数功能：设置单元上一个具体的传感器的开关状态。 
        参数说明： 
        1）table：表对象：
         guid：字符串。单元 GUID；
         SENSORGUID：字符串。传感器的组件 GUID；
         ISACTIVE：布尔值。开关状态标识符（true：开，false：关）。 
        '''
        lua ="Hs_ScenEdit_SetSensorSwitch({guid=%s,SENSORGUID=%sISACTIVE=%s})"%(unit_guid,sensor_guid,is_active)
        return self.mozi_service.scenAndRecv(lua)
    

        
    