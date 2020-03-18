# -*- coding:utf-8 -*-
##########################################################################################################
# File name : CReferencePoint.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CReferencePoint():
    def __init__(self, guid, name, side_guid):
        self.mozi_server = None
        # 类名
        self.ClassName = ""
        # 名称
        self.strName = name
        # GUID
        self.strGuid = guid
        # 方
        self.m_Side = side_guid
        # 经度
        self.dLongitude = 0.0
        # 纬度
        self.dLatitude = 0.0
        # 高度
        self.fAltitude = 0.0
        # 相对单元guid
        self.m_RelativeToUnit = ""
        # 相对方位角
        self.fRelativeBearing = 0.0
        # 相对距离
        self.fRelativeDistance = 0.0
        # 方向类型
        # 0 固定的，不随领队朝向变化而变化
        # 1 旋转的，随领队朝向改变旋转
        self.m_BearingType = 0
        # 是否锁定
        self.bIsLocked = False

    def setZone(self, sideName, zoneGuid, zoneTableMode):
        """
        创建和设置区域
        :param sideName: 推演方
        :param zoneGuid: 区域id
        :param zoneTableMode: ??
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_SetZone('{}', '{}',{})".format(sideName, zoneGuid, zoneTableMode))
