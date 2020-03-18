# -*- coding:utf-8 -*-
##########################################################################################################
# File name : loadout.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CLoadout():
    def __init__(self, guid):
        self.sensors = {}
        self.strGuid = guid
        self.strName = ''
        # 挂载的武器的数量
        self.strLoadWeaponCount = 0
        # 挂载的数量和挂架载荷
        self.m_LoadRatio = ""
        # 飞机的guid
        self.m_AircraftGuid = ''
        # 是否支持快速出动
        self.bQuickTurnaround = False
        # 最大飞行波次
        self.iMaxSorties = 0
        # 货物类型
        self.m_CargoType = 0
        self.iDBID = ''
        self.select = False #是否查找挂实体

    def delete_sub_object(self):
        """
        删除时删除子对象
        :return:
        """
        del_list = list(self.sensors.keys())
        del self.sensors
        return del_list
