# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : mount.py
# Create date : 2020-1-8
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : magazine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CMount():
    '''挂载'''
    def __init__(self, guid):
        self.strGuid= guid
        self.strName = ''
        # 所属单元GUID
        self.m_ParentPlatform = ''
        # 部件状态
        self.m_ComponentStatus = 0
        # 毁伤程度的轻,中,重
        self.m_DamageSeverity = 0
        # 挂载方位
        self.m_CoverageArc = ""
        # 挂载的武器开火状态
        self.strWeaponFireState = ""
        # 挂载的武器的数量
        self.strLoadWeaponCount = ""
        # 获取挂架下武器的最大载弹量和当前载弹量集合
        self.m_LoadRatio = ""
        # 传感器的guid
        self.m_Sensors = ""
        # 重新装载优先级选中的武器DBID集合
        self.m_ReloadPrioritySet = ""
        # 左弦尾1
        self.PS1 = False
        # 左弦中后1
        self.PMA1 = False
        # 左弦中前
        self.PMF1 = False
        # 左弦首1
        self.PB1 = False
        # 右弦尾1
        self.SS1 = False
        # 右弦中后1
        self.SMA1 = False
        # 右弦中前1
        self.SMF1 = False
        # 右弦首1-bow
        self.SB1 = False
        # 左弦尾2-stern
        self.PS2 = False
        # 左弦中后2
        self.PMA2 = False
        # 左弦中前2
        self.PMF2 = False
        # 左弦首2
        self.PB2 = False
        # 右弦尾2
        self.SS2 = False
        # 右弦中后2
        self.SMA2 = False
        # 右弦中前2
        self.SMF2 = False
        # 右弦首2
        self.SB2 = False
        self.select = False

    def delete_sub_object(self):
        del_list = list(self.sensors.keys())
        del self.sensors
        return del_list


    def setWeaponReloadPriority(self, strCurrentUnitGuid, isReloadPriority):
        '''
        函数功能：设置武器重新装载优先级
        函数类型：推演函数
        strCurrentUnitGuid 单元guid
        isReloadPriority： 布尔值
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetWeaponReloadPriority({guid='%s',WPNREC_GUID='%s',IsReloadPriority=%s})" % (
            strCurrentUnitGuid, self.guid, isReloadPriority))

    def addReloadsToUnit(self, unitName, number, weapon_max):
        '''
        函数功能：将武器加入装具
        函数类型：推演函数
        unitName 装具所属单元的名称/GUID
        number 要添加的数量
        weapon_max 装载武器的最大容量
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_AddReloadsToUnit({unitname='%s', w_dbid=%s, number=%s, w_max=%s})" % (
        unitName, self.guid, number, weapon_max))
