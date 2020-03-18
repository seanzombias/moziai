# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : submarine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit

class Csubmarine(CActiveUnit):
    '''
    潜艇
    '''
    def __init__(self):
        '''飞机'''
        super().__init__()
        self.m_BearingType = {}  # 方位类型
        self.m_Bearing = {}  # 方位
        self.m_Distance = 0.0  # 距离（转换为千米）
        self.bSprintAndDrift = False  # 高低速交替航行
        self.m_AITargets = {}  # 获取AI对象的目标集合
        self.m_AITargetsCanFiretheTargetByWCSAndWeaponQty = {}  # 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        self.strDockAircraft = ''  # 载机按钮的文本描述
        self.strDockShip = ''  # 载艇按钮的文本描述
        # 以下为 CSubmarine 的属性
        self.m_Category = {}  # 类型类别
        self.m_CIC = {}  # 指挥部
        self.m_Rudder = {}  # 船舵
        self.m_PressureHull = {}  # 船身
        # 获取作战单元燃油信息
        self.strFuelState = ''  # 显示燃油状态
        # 柴油剩余百分比
        self.dPercentageDiesel = 0.0
        # 电池剩余百分比
        self.dPercentageBattery = 0.0
        # AIP剩余百分比
        self.dPercentageAIP = 0.0
        self.m_Type = {}
        self.strCavitation = ''
        self.fHoverSpeed = 0.0  # 悬停
        self.fLowSpeed = 0.0  # 低速
        self.fCruiseSpeed = 0.0  # 巡航
        self.fMilitarySpeed = 0.0  # 军力
        self.fAddForceSpeed = 0.0  # 加速
        self.iThermoclineUpDepth = 0.0  # 温跃层上
        self.iThermoclineDownDepth = 0.0  # 温跃层下
        # 载艇-信息
        self.strDamageInfo = ''  # 毁伤
        self.strWeaponInfo = ''  # 武器
        self.strMagazinesInfo = ''  # 弹药库
        self.strFuelInfo = ''  # 燃料
        self.strStatusInfo = ''  # 状态
        self.strTimeToReadyInfo = ''  # 就绪时间
        # 油门高度-航路点信息
        self.strWayPointName = ''  # 航路点名称

    def subm_manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        手动开火函数
        作者：解洋
        fire_unit_guid:开火单元guid
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量        
        return :
        lua执行成功/lua执行失败
        '''
        self.strGuid = self.guid
        return super().manual_pick_war(target_guid, weapon_dbid, weapon_num)

    def subm_attack_auto(self, contact_guid):
        """
        自动攻击目标
        :param contact_guid: 目标guid
        :return:
        """
        self.strGuid = self.guid
        return super().attack_auto(contact_guid)

    def subm_set_up_throttleI(self):
        '''
        升油门
        '''
        self.strGuid = self.guid
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

    def subm_set_down_throttleI(self):
        '''
        降油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == Throttle.Loiter:
            throttle_str = "FullStop"
        if self.m_CurrentThrottle == Throttle.Full:
            throttle_str = "Loiter"
        if self.m_CurrentThrottle == Throttle.Flank:
            throttle_str = "Full"
        if self.m_CurrentThrottle == Throttle.Cruise:
            throttle_str = "Flank"
        return super().set_throttle(throttle_str)

    def subm_ops_singleout(self, base_guid):
        '''
        设置在基地内单机出动
        base_guid : 飞机所在机场的guid
        return :
        lua执行成功/lua执行失败
        '''
        return super().unitops_singleout(base_guid, self.guid)

    def subm_set_rader_shutdown(self, trunoff):
        '''
        设置雷达开关机
        '''
        return super().set_rader_shutdown(trunoff)

    def subm_set_sonar_shutdown(self, trunoff):
        '''
        设置声纳开关机
        '''
        return super().set_sonar_shutdown(trunoff)

    def subm_set_OECM_shutdown(self, trunoff):
        '''
        设置干扰开关机
        '''
        return super().set_OECM_shutdown(trunoff)

    def subm_set_desired_height(self, desired_height):
        """
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        return super().set_desired_height(desired_height)

    def subm_return_to_base(self):
        '''
        返回基地
        '''
        self.strGuid = self.guid
        return super().return_to_base()

    def subm_plotted_course(self, course_list):
        """
        航线规划
        :param course_list: list, [(lat, lon)], 例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        self.strGuid = self.guid
        side_name = self.side_name
        return super().plotted_course(course_list)

    def subm_drop_active_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放主动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return super().drop_active_sonobuoy(sideName, deepOrShallow)

    def subm_drop_passive_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放被动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return super().drop_passive_sonobuoy(sideName, deepOrShallow)
