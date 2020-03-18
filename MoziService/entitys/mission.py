# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : mission.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################
from MoziService.entitys.commonfunction import get_lua_table2json, get_lua_mission_parser
from MoziService.entitys.global_util import throttle_description


class CMission():
    '''任务'''
    def __init__(self, guid, name, side_guid, mozi_server):
        self.mozi_server = mozi_server
        # 类名
        self.ClassName = ""
        # 任务guid
        self.strGuid = guid
        # 名称
        self.strName = name
        # 推演方
        self.m_Side = side_guid
        # 推演方名称
        self.side_name = ""
        # 任务类别
        self.m_Category = 0
        # 任务类型
        self.m_MissionClass = 0
        # 任务状态
        self.m_MissionStatus = 0
        # 飞机设置-编队规模
        self.m_FlightSize = 0
        # 空中加油任务设置-任务执行设置 -加油机遵循受油机的飞行计划是否选中
        self.bTankerFollowsReceivers = False
        # 任务描述
        self.strDescription = ""
        # 空中加油任务设置-任务规划设置 加油机没到位的情况下启动任务
        self.bLaunchMissionWithoutTankersInPlace = False
        # 水面舰艇/潜艇设置-水面舰艇/潜艇树低于编队规模要求,不能出击(根据基地编组)
        self.bUseGroupSizeHardLimit = False
        # 已分配单元的集合
        self.m_AssignedUnits = ""
        # 空中加油任务设置-任务执行设置 - 每架加油机允许加油队列最大长度
        self.strMaxReceiversInQueuePerTanker_Airborne = ""
        # 水面舰艇/潜艇设置-编队规模
        self.m_GroupSize = 0
        # 空中加油-  点击配置  显示如下两个选项： 返回选中的值1.使用优良充足的最近加油机加油2.使用已分配特定任务的加油机加油
        self.m_TankerUsage = 0
        # 条令
        self.m_Doctrine = ""
        # 空中加油任务设置-任务规划设置 阵位上加油机最小数量
        self.strTankerMinNumber_Station = ""
        # 未分配单元的集合
        self.m_UnassignedUnits = ""
        # 单元航线
        self.m_strSideWayGUID = ""
        # 空中加油任务设置-任务执行设置 -受油机寻找加油机的时机条件
        self.strFuelQtyToStartLookingForTanker_Airborne = ""
        # 空中加油选项是否与上级保持一致
        self.bUseRefuel = False
        # 飞机数低于编队规模要求,不能起飞
        self.bUseFlightSizeHardLimit = False
        # 飞机设置-空中加油
        self.m_UseRefuel = 0
        # 行动预案
        self.bUseActionPlan = False
        # 空中加油任务设置-任务规划设置 留空的加油机最小数量
        self.strTankerMinNumber_Airborne = ""
        # 空中加油任务设置-任务规划设置1.需要加油机的最小数量
        self.strTankerMinNumber_Total = ""

    def mission_isactive(self, is_active):
        """
        是否启用任务
        :param is_active: bool, 是否启用
        :return:
        """
        str_set = str(is_active).lower()
        lua = "print(ScenEdit_SetMission('%s','%s',{isactive='%s'}))" % (self.side_name, self.strName, str_set)
        return self.mozi_server.sendAndRecv(lua)

    def set_startTime(self, startTime):
        """
        设置、删除任务开始时间
        :param startTime: 开始时间
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "','" + self.strName + "',{starttime='" + startTime + "'})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def set_endTime(self, endTime):
        """
        设置任务：删除任务结束时间
        :param endTime:
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "','" + self.strName + "',{endtime='" + endTime + "'})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def set_oneThirdrule(self, set_oneThird):
        """
        三分之一规则，适用于任务：巡逻，支援，布雷和扫雷
        :param set_oneThird: bool, True,设置三分之一规则  False:不遵守三分之一规则
        :return:
        """
        lua = 'ScenEdit_SetMission("%s","%s", {oneThirdRule=%s})' % \
              (self.side_name, self.strName, str(set_oneThird).lower())
        return self.mozi_server.sendAndRecv(lua)

    def set_mission_switch_radar(self, switch_on):
        """
        设置任务雷达是否打开
        :param switch_on: bool, 雷达打开或者静默，True:打开
        :return:
        """
        if switch_on:
            set_str = 'Radar=Active'
        else:
            set_str = 'Radar=Passive'
        return self.mozi_server.setEMCON("Mission", self.strName, set_str)

    def assignUnitToMission(self, unitID, is_escort=False):
        """
        设置任务：将实体分配到任务中来
        :param unitID: str, 实体
        :param escort:bool,  是否护航任务
        :return: 
        """
        cmd_str = "ScenEdit_AssignUnitToMission('" + unitID + "', '" + self.strName + "', " + str(is_escort).lower() + ")"
        return self.mozi_server.sendAndRecv(cmd_str)

    def get_information(self):
        """
        返回任务详细信息, 巡逻，打击或支援任务共用
        :return:dict, 例子:{"isactive":true,"SISH":false,"endtime":"2019/8/8 91609","subtype":"AAW Patrol","starttime":"2019/8/26 91609"}
        """
        return get_lua_table2json() + (get_lua_mission_parser() % (self.side_name, self.strName))

    def get_units_assigned(self):
        """
        返回任务已分配的单元
        :return: list, 单元guid list
        """
        lua_scrpt = "print(ScenEdit_GetMission('%s', '%s').unitlist)" % (self.side_name, self.strName)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def get_mission_unAllocationUnit(self):
        """
        返回未分配任务的单元
        :return: list, 单元guid list
        Hs_GetMissionUnAllocationUnit('SideNameOrID','MissionNameOrID')
        """
        lua_scrpt = "print(Hs_GetMissionUnAllocationUnit('%s','%s'))" % (self.side_name, self.strName)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def is_valid_area(self):
        '''
        验证区域角点连线是否存在交叉现象
        返回值：验证结果状态标识（'Yes'：正常，'No'：异常）
        '''
        lua_scrpt = "print(Hs_IsValidArea('%s'))" % self.strName
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def scenEdit_delete_mission(self):
        """
        函数功能：删除指定推演方的指定任务
        函数类型：推演函数
        ScenEdit_DeleteMission('红方','空巡')
        """
        lua_scrpt = "print(ScenEdit_DeleteMission('%s','%s'))" % (self.side_name, self.strName)
        return self.mozi_server.sendAndRecv(lua_scrpt)
  
    def scenEdit_unAssignUnitFromMission(self,activeunit_name_guid):
        """
        单元从任务中移除
        activeunit_name_guid 字符串。单元名称或 GUID
        ScenEdit_UnAssignUnitFromMission ('飞机#2','空巡')
        """
        lua_scrpt = "print(ScenEdit_UnAssignUnitFromMission('%s','%s'))" % (activeunit_name_guid, self.strName)
        return self.mozi_server.sendAndRecv(lua_scrpt)
    
    #---------------------------------mission category:strike---------------------------------------

    def export_mission(self):
        """
        作者：赵俊义
        日期：2020-3-10
        函数功能：将相应的任务导出到 Defaults 文件夹中
        函数类型：推演函数
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_ExportMission('{}','{}')".format(self.m_Side, self.strGuid))

    def import_mission(self):
        """
        作者：赵俊义
        日期：2020-3-10
        函数功能：从 Defaults 文件夹中查找对应的任务，导入到想定中
        函数类型：推演函数
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_ExportMission('{}','{}')".format(self.m_Side, self.strGuid))
    # ---------------------------------mission category:strike---------------------------------------
    def strike_addTarget(self, targetList):
        """
        设置打击目标
        :param targetList: 目标列表
        :return: 
        """
        strTargetList = "{"
        for i in targetList:
            strTargetList += "'" + i + "',"
        strTargetList = strTargetList[:len(strTargetList) - 1]
        strTargetList += "}"
        cmd_str = "print(ScenEdit_AssignUnitAsTarget(" + strTargetList + ",'" + self.strName + "'))"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_removeTarget(self, targetList):
        """
        设置任务：删除打击任务目标
        :param targetList: 目标列表
        :return:
        """
        strTargetList = "{"
        for i in targetList:
            strTargetList += "'" + i + "',"
        strTargetList = strTargetList[:len(strTargetList) - 1]
        strTargetList += "}"
        cmd_str = "print(ScenEdit_RemoveUnitAsTarget(" + strTargetList + ",'" + self.strName + "'))"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_get_targets(self):
        """
        打击返回任务已目标单元
        :return: list, 单元guid list
        """
        unit_str = "print(ScenEdit_GetMission('%s', '%s').targetlist)" % (self.side_name, self.strName)
        return self.mozi_server.sendAndRecv(unit_str)

    def strike_setPreplan(self, bPreplan):
        """
        设置任务细节：是否仅考虑计划目标（在目标清单）
        :param bPreplan: bool, True:是仅考虑计划目标
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikePreplan = " + str(bPreplan).lower() + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setAttackCondition(self, enum_strikeMinimumTrigger):
        """
        设置打击任务触发条件
        :param enum_strikeMinimumTrigger:StrikeMinimumTrigger
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {StrikeMinimumTrigger = " + str(enum_strikeMinimumTrigger.value) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeMax(self, enum_strikeMax):
        """
        设置任务细节：任务允许出动的最大飞行批次
        :param strikeMax:StrikeFlyTimeMax
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikeMax = " + str(
            enum_strikeMax.value) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeFlightSize(self, flightSize):
        """
        设置打击任务编队规模
        :param flightSize:FlightSize, 编队规模
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikeFlightSize = " + str(
            flightSize.value) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeMinAircraftReq(self, minAircraft):
        """
        设置打击任务所需最少飞机数
        :param minAircraft:StrikeMinAircraftReq
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikeMinAircraftReq = " + str(
            minAircraft.value) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeRadarUsage(self, radarUsage):
        """
        设置打击任务雷达运用规则
        :param radarUsage:StrikeRadarUasge
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', { StrikeRadarUsage = " + str(
            radarUsage.value) + "} )"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeFuleAmmo(self, fuleAmmo):
        """
        设置打击任务燃油弹药规则
        :param fuleAmmo: StrikeFuleAmmo
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {StrikeFuleAmmo = " + str(
            fuleAmmo.value) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

        # 设置任务细节：最小打击半径

    def strike_setStrikeMinDist(self, minDist):
        """
        设置打击任务最小打击半径
        :param minDist:float, 公里
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {StrikeMinDist=" + str(
            minDist) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setMissionStrikeMaxDist(self, maxDist):
        """
        设置打击任务最大打击半径
        :param maxDist: float, 公里
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {StrikeMaxDist=" + str(
            maxDist) + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeUseFlightSize(self, bUseFlightSize):
        """
        设置打击任务是否飞机数低于编组规模数要求就不能起飞
        :param bUseFlightSize: bool, 是否飞机数低于编组规模数要求就不能起飞
        :return:
        """
        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikeUseFlightSize = " + str(
            bUseFlightSize).lower() + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeUseAutoPlanner(self, bUseAutoPlanner):
        """
        设置打击任务是否多扇面攻击（任务AI自动生成）
        :param bUseAutoPlanner: bool, 是否多扇面攻击
        :return:
        """

        cmd_str = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {StrikeUseAutoPlanner = " + str(
            bUseAutoPlanner).lower() + "})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def strike_setStrikeOneTimeOnly(self, bOneTimeOnly):
        """
        设置打击任务是否仅限一次
        :param bOneTimeOnly: bool, 是否仅一次
        :return:
        """
        cmd = "ScenEdit_SetMission('" + self.side_name + "', '" + self.strName + "', {strikeOneTimeOnly = " + str(
            bOneTimeOnly) + "})"
        return self.mozi_server.sendAndRecv(cmd)


    # ---------------------------------mission category:patrol---------------------------------------
    def patrol_set_maintainUnitNumber(self, unit_number):
        """
        巡逻任务阵位上每类平台保存作战单元数量
        :param unit_number: int, 阵位上每类平台保存单元数量
        :return:
        """
        cmd_str = 'ScenEdit_SetMission("%s","%s",{PatrolMaintainUnitNumber=%d})' % (
        self.side_name, self.strName, unit_number)
        return self.mozi_server.sendAndRecv(cmd_str)

    def patrol_set_OneThirdRule(self, isOneThirdRule):
        """
        设置任务是否遵循1/3原则
        :param isOneThirdRule: bool, True:遵守，False:不遵守
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "', '" + str(
            self.strGuid) + "', { oneThirdRule = " + str(isOneThirdRule) + "})"

        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_checkOPA(self, ischeckOPA):
        """
        设置任务是否对巡逻区外的探测目标进行分析
        :param ischeckOPA: bool, True:分析，False:不分析
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "', '" + str(
            self.strGuid) + "', { checkOPA = " + str(ischeckOPA).lower() + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_activeEMCON(self, isactiveEMCON):
        """
        设置任务是否仅在巡逻/警戒区内打开电磁辐射
        :param isactiveEMCON: bool, True:打开 False:不打开
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "', '" + str(
            self.strGuid) + "', { activeEMCON = " + str(isactiveEMCON).lower() + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_checkWWR(self, ischeckWWR):
        """
        设置任务是否对武器射程内探测目标进行分析
        :param ischeckWWR: bool, True遵守 或 False不遵守
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "', '" + str(
            self.strGuid) + "', { checkWWR = " + str(ischeckWWR).lower() + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_flight_size(self, enum_flight_size):
        """
        设置任务编队规模
        :param enum_flight_size:FlightSize, 编队规模
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "', '" + str(self.guid) + "', { flightSize = " + str(enum_flight_size.value) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)
    
    def patrol_useFlightSize(self, useFlightSize):
        """
        是否飞机数低于编队规模不允许起飞
        :param useFlightSize: bool, True:是
        :return:
        """

        return self.mozi_server.sendAndRecv('ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '", {'
                                        'useFlightSize =' + str(useFlightSize).lower() + '})')

    def patrol_set_throttle_transit(self, enum_throttle):
        """
        设置任务的出航油门
        :param enum_throttle:Throttle
        :return:
        """
        if enum_throttle not in throttle_description:
            return
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(self.strGuid) + "', { " \
            "transitThrottleAircraft = '" + enum_throttle + "'}) "
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_throttle_station(self, enum_throttle):
        """
        设置任务的阵位油门
        :param enum_throttle: Throttle
        :return:
        """
        if enum_throttle not in throttle_description:
            return
        set_str = throttle_description[enum_throttle]
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { stationThrottleAircraft = '" + set_str + "'})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_throttle_attack(self, enum_throttle):
        """
        设置任务的攻击油门
        :param enum_throttle: Throttle
        :return:
        """
        if enum_throttle not in throttle_description:
            return
        set_str = throttle_description[enum_throttle]

        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { attackThrottleAircraft = '" + set_str + "'})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_transitAltitude(self, transitAltitude):
        """
        设置任务的出航高度
        :param transitAltitude: float, 出航高度， 单位：米，最多6位字符，例：99999.9， 888888
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { transitAltitudeAircraft = " + str(transitAltitude) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_stationAltitude(self, stationAltitude):
        """
        设置任务的阵位高度
        :param stationAltitude: float, 阵位高度， 单位：米，最多6位字符
        :return:
        """

        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { StationAltitudeAircraft = " + str(stationAltitude) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_attackAltitude(self, attackAltitude):
        """
        设置任务的攻击高度
        :param stationAltitude: float, 攻击高度， 单位：米，最多6位字符
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { AttackAltitudeAircraft = " + str(attackAltitude) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def patrol_set_attack_distance(self, distance):
        """
        设置任务的攻击距离
        :param distance: float, 攻击距离，单位：公里
        :return:
        """

        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { attackDistanceAircraft = " + str(distance) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    # ---------------------------------mission category:support---------------------------------------
    def support_SupportMaintainUN(self, support_maintain_count):
        """
        阵位上每类平台保持几个
        :param support_maintain_count: int, 保持阵位的数量
        :return:
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '",{SupportMaintainUN=' + str(
                support_maintain_count) + '})')


    def support_oneTimeOnly(self, isoneTimeOnly):
        """
        仅一次
        :param isoneTimeOnly: bool, 是否仅一次
        :return:
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '", {oneTimeOnly=' + str(
                isoneTimeOnly).lower() + '})')

    def support_activeEMCON(self, isactiveEMCON):
        """
        仅在阵位上打开电磁辐射
        :param isactiveEMCON: bool, True:打开, False:不打开
        :return:
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '", {activeEMCON =' + str(
                isactiveEMCON).lower() + '})')

    def support_loopType(self, isloopType):
        """
        导航类型
        :param isloopType: bool, True-仅一次；False-连续循环
        :return: 
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '", {loopType =' + str(
                isloopType).lower() + '})')

    def support_flightSize(self, enum_flightSize):
        """
        编队规模
        :param enum_flightSize: FlightSize, 编队规模
        :return: 
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '",{flightSize=' + str(
                enum_flightSize.value) + '})')

    def support_useFlightSize(self, useFlightSize):
        """
        是否飞机数低于编队规模不允许起飞
        :param useFlightSize: bool, True:是
        :return:
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '", {useFlightSize =' + str(
                useFlightSize).lower() + '})')

    def support_set_throttle_transit(self, enum_throttle):
        """
        设置任务的出航油门
        :param enum_throttle:Throttle
        :return:
        """
        if enum_throttle not in throttle_description:
            return
        set_str = throttle_description[enum_throttle]
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { transitThrottleAircraft = '" + set_str + "'})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def support_set_throttle_station(self, enum_throttle):
        """
        设置任务的阵位油门
        :param enum_throttle: Throttle
        :return:
        """
        if enum_throttle not in throttle_description:
            return
        set_str = throttle_description[enum_throttle]
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { stationThrottleAircraft = '" + set_str + "'})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def support_set_transitAltitude(self, transitAltitude):
        """
        设置任务的出航高度
        :param transitAltitude: float, 出航高度， 单位：米，最多6位字符，例：99999.9， 888888
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { transitAltitudeAircraft = " + str(transitAltitude) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def support_set_stationAltitude(self, stationAltitude):
        """
        设置任务的阵位高度
        :param stationAltitude: float, 阵位高度， 单位：米，最多6位字符
        :return:
        """
        orderToChange = "ScenEdit_SetMission('" + str(self.side_name) + "','" + str(
            self.strGuid) + "', { StationAltitudeAircraft = " + str(stationAltitude) + "})"
        return self.mozi_server.sendAndRecv(orderToChange)

    def support_MaintainUnit(self, patrol_maintain_count):
        """
        阵位上每类平台保持几个
        :param patrol_maintain_count: int, 保持阵位的数量
        :return:
        """
        return self.mozi_server.sendAndRecv(
            'ScenEdit_SetMission("' + self.side_name + '","' + self.strName + '",{PatrolMaintainUnitNumber=' + str(
                patrol_maintain_count) + '})')

    def set_patrol_sonobuoys_cover(self, fSonobuoysCover, dropSonobuoysType):
        """
        函数功能：为反潜巡逻任务设置声呐浮标在巡逻区域内的覆盖密度和深浅类型。
        函数类型：推演函数
        :param fSonobuoysCover: 声呐与声呐之间的距离，按照投放声呐的探测圈范围
        :param dropSonobuoysType:声呐的深浅
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_SetPatrolSonobuoysCover('{}','{}','{}')".format(self.strGuid, fSonobuoysCover, dropSonobuoysType))

