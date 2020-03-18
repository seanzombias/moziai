# -*- coding:utf-8 -*-
##########################################################################################################
# File name : facility.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CFacility(CActiveUnit):
    '''地面设施'''

    def __init__(self,side_guid):
        super().__init__()
        self.side_guid = side_guid
        # 方位类型
        self.m_BearingType = 0
        # 方位
        self.m_Bearing = 0.0
        # 距离（千米）
        self.m_Distance = 0.0
        # 是否高速交替航行
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
        # self.fAddForceSpeed = 0.0
        # 载艇按钮的文本描述
        self.strDockShip = ""
        self.m_CommandPost = ""
        # 加油队列明细
        self.m_ShowTanker = ""

    def fac_get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            "guid": self.guid,
            "DBID": self.iDBID,
            "subtype": str(self.m_Category),
            "facilityTypeID": "",
            "name": self.strName,
            "side": self.side_name,
            "proficiency": self.m_ProficiencyLevel,  # ?
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "altitude_asl": self.iAltitude_ASL,
            "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,  # ?
            "fuelstate": "",  # ?
            "weaponstate": -1,  # ?
            "mounts": self.get_mounts_info(),
            "targetedBy": self.get_target_by_info(),
            "type": "Facility",
            "fuel": 0,  # ?
            "damage": self.strDamageState,  # ?
            "sensors": self.get_sensors_info(),
            "weaponsValid": self.get_valid_weapons()
        }
        return info_dict

    def get_target_by_info(self):
        pass

    def fac_set_up_throttleI(self):
        '''
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
            return
        # super().set_throttle(throttle_str)
        return super().set_throttle(throttle_str)  # reuturn 返回lua信息

    def fac_set_down_throttleI(self):
        '''
        降油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == 1:
            throttle_str = "FullStop"
        elif self.m_CurrentThrottle == 2:
            throttle_str = "Loiter"
        elif self.m_CurrentThrottle == 3:
            throttle_str = "Full"
        elif self.m_CurrentThrottle == 4:
            throttle_str = "Flank"
        return super().set_throttle(throttle_str)

    def fac_set_rader_shutdown(self, on_off):
        '''
        设置雷达开关机
        guid : 要设置单元唯一标识（guid）
        '''
        return super().set_rader_shutdown(on_off)  # 参数是 ture 或者false， zzz能跑通lua

    def fac_set_OECM_shutdown(self, on_off):
        '''
        设置干扰开关机
        '''        
        return super().set_OECM_shutdown(on_off)

    def fac_set_desired_speed(self, desired_speed):
        """
        设置单元的期望速度
        :param desired_speed: float, 千米/小时
        :return: 所操作单元的完整描述子
        """
        return super().set_desired_speed(desired_speed)

    def fac_set_desired_height(self, desired_height):
        """
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        return super().set_desired_height(desired_height)

    def fac_set_unit_heading(self, heading):
        '''
        设置朝向
        heading 朝向        
        exampl
        set_unit_heading(30):
        '''
        return super().set_unit_heading(heading)

    def fac_plotted_course(self, course_list):
        """
        地面设施航线规划
        :param course_list: list, [(lat, lon)], 例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        return super().plotted_course(course_list)

    def fac_delete_coursed_point(self, point_index):
        """
        单元删除航路点
        :param point_index: list:删除多个航路点 [0, 1], or int：删除一个航路点，
        :param clear: bool, True:清空航路点
        :return:
        """
        return super().delete_coursed_point(point_index)

    def fac_assign_unitList_to_mission(self, mission_name):
        """
        分配加入到任务中
        :param mission_name: str, 任务名称
        :return: table 存放单元的名称或GUID
        """
        return super().assign_unitList_to_mission(mission_name)

    def fac_attack_auto(self, target_guid):
        """
        自动攻击目标
        :param target_guid: 目标guid
        :return:
        """

        # ret = self.mozi_server.sendAndRecv("ScenEdit_AttackContact ('%s', '%s', {mode=0})" % (guid, target_guid))
        # return ret

        return super().attack_auto(target_guid)

    def fac_manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        手动开火函数       
        fire_unit_guid:开火单元guid
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量
        return :
        lua执行成功/lua执行失败
        '''
        return super().manual_pick_war(target_guid, weapon_dbid, weapon_num)

    def fac_all_ocate_salvo_to_target(self, target, weaponDBID):
        """
        单元手动分配一次齐射攻击(打击情报目标), 或者纯方位攻击(打击一个位置)
        :param target:情报目标guid，例："fruo-fs24-2424jj" 或  坐标-tuple(lat, lon)，例:(40.90,30.0)
        :param weaponDBID:武器型号数据库id
        :return:
        """
        return super().all_ocate_salvo_to_target(target, weaponDBID)

    def fac_unit_obeys_EMCON(self, is_obey):
        """
        单元传感器面板， 单元是否遵循电磁管控条令
        :param is_obey: bool(True 或 False)
        :return: void
        """
        return super().unit_obeys_EMCON(is_obey)
