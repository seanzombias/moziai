# -*- coding:utf-8 -*-
##########################################################################################################
# File name : magazine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CMagazine():
    '''弹药库'''
    def __init__(self, guid):
        #弹药库guid
        self.strGuid = guid
        # 弹药库名称
        self.strName = ''
        # 父平台guid
        self.m_ParentPlatform = ''
        # 状态
        self.m_ComponentStatus = 0
        # 毁伤程度的轻,中,重
        self.m_DamageSeverity = 0
        # 覆盖角度
        self.m_CoverageArc = ""
        # 挂架已挂载的数量和挂架载荷
        self.m_LoadRatio = ""
        self.select = False # 选择是否查找所属单元


    def setMagazineState(self, unit_guid,  state):
        """
        函数功能：设置弹药库状态
        函数类型：编辑函数
        unit_guid 单元guid
        state  状态
        """
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetMagazineState({guid='%s', magazine_guid='%s',state='%s'}" % (unit_guid, self.guid, state))

    def removeMagazineWeapon(self, unit_guid):
        """
        函数功能：删除单元中指定弹药库下的指定武器
        函数类型：编辑函数
        unit_guid 单元guid
        """
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_RemoveMagazineWeapon({GUID='%s',WPNREC_GUID='%s'})" % (unit_guid, self.guid))

    def removeMagazine(self, unit_guid,):
        '''
        函数功能： 删除弹药库
        函数类型：编辑函数
        unit_guid 单元guid
        '''
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_RemoveMagazine({guid='%s', magazine_guid='%s'})" % (unit_guid, self.guid))
