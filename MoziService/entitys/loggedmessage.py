# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : loggedmessage.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CLoggedMessage():
    def __init__(self, guid, side_guid):
        # 消息对象guid
        self.strGuid = ""
        # 方的GUID
        self.m_Side = side_guid
        # 事件的内容
        self.MessageText = ""
        # 消息发生的时间
        self.TStamp = 0.0
        # 消息类型
        self.MessageType = 0
        # 消息编号
        self.Increment = 0.0
        # 等级
        self.iLevel = ""
        # 经度
        self.Longitude = 0.0
        # 纬度
        self.Latitude = 0.0
        # 报告者GUID
        self.ReporterID = ""
        # 事件关联的目标本身单元的GUID
        self.ContactActiveUnitGUID = ""
