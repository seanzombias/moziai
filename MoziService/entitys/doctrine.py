# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : doctrine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
#########################################################################################################
class CDoctrine:
    def __init__(self, mozi_server):
        self.strGuid = ''
        self.strName = ''
        self.m_Side = ''
        self.category = None
        self.mozi_server = mozi_server
        # 条令的拥有者GUID（具体作用对象）
        self.m_DoctrineOwner = ""
        # 核武器使用规则
        self.m_Nukes = 0
        # 对空目标武器控制规则
        self.m_WCS_Air = 0
        # 对海目标武器控制规则C
        self.m_WCS_Surface = 0
        # 对潜目标武器控制规则
        self.m_WCS_Submarine = 0
        # 对地目标武器控制规则
        self.m_WCS_Land = 0
        # 进攻时是否忽略绘制航线规则
        self.m_IgnorePlottedCourseWhenAttacking = 0
        # 对不明目标的行为态度规则
        self.m_BehaviorTowardsAmbigousTarget = 0
        # 对临机目标进行射击规则
        self.m_ShootTourists = 0
        # 受攻击时是否考虑电磁管控规则
        self.m_IgnoreEMCONUnderAttack = 0
        # 鱼雷使用动力航程规则
        self.m_UseTorpedoesKinematicRange = 0
        # 是否自动规避目标规则
        self.m_AutomaticEvasion = 0
        # 是否可加油/补给规则
        self.m_UseRefuel = 0
        # 对所选单元加油/补给时加油机选择规则
        self.m_RefuelSelection = 0
        # 与盟军单元加油/补给规则
        self.m_RefuelAllies = 0
        # 空战节奏规则
        self.m_AirOpsTempo = 0
        # 快速出动规则
        self.m_QuickTurnAround = 0
        # 预先规划终止任务返回基地油量阈值规则
        self.m_BingoJoker = 0
        # 编组成员达到预先规划油量状态时编组或成员返回基地规则
        self.m_BingoJokerRTB = 0
        # 预先规划武器使用规则、武器状态与平台脱离战斗规则
        self.m_WeaponState = 0
        # 编组成员达到预先规划武器状态时，编组或成员返回基地规则
        self.m_WeaponStateRTB = 0
        # 航炮是否对地面目标扫射规则
        self.m_GunStrafeGroundTargets = 0
        # 受到攻击时是否抛弃弹药规则
        self.m_JettisonOrdnance = 0
        # 以反舰模式使用舰空导弹规则
        self.m_SAM_ASUW = 0
        # 与目标保持一定距离规则
        self.m_MaintainStandoff = 0
        # 尽可能规避目标规则
        self.m_AvoidContact = 0
        # 探测到威胁目标后下潜规则
        self.m_DiveWhenThreatsDetected = 0
        # 巡逻任务充电时电池剩余电量规则
        self.m_RechargePercentagePatrol = 0
        # 进攻战充电时电池剩余电量规则
        self.m_RechargePercentageAttack = 0
        # AIP推进技术使用规则
        self.m_AIPUsage = 0
        # 吊放声呐使用规则
        self.m_DippingSonar = 0
        # 毁伤达到阈值时应撤退规则
        self.m_WithdrawDamageThreshold = 0
        # 油量达到阈值时应撤退规则
        self.m_WithdrawFuelThreshold = 0
        # 进攻战武器数量达到阈值应撤退规则
        self.m_WithdrawAttackThreshold = 0
        # 防御战武器数量达到阈值应撤退规则
        self.m_WithdrawDefenceThreshold = 0
        # 毁伤达到阈值时应重新部署规则
        self.m_RedeployDamageThreshold = 0
        # 油量达到阈值时应重新部署规则
        self.m_RedeployFuelThreshold = 0
        # 进攻战武器数量达到阈值时应重新部署规则
        self.m_RedeployAttackDamageThreshold = 0
        # 防御战武器数量达到阈值时应重新部署规则
        self.m_RedeployDefenceDamageThreshold = 0
        # 电磁管控设置是否有值
        self.m_bEMCON_AccordingSuperior = False
        # 雷达管控规则设置模式
        self.m_EMCON_SettingsForRadar = 0
        # 声呐管控规则设置模式
        self.m_EMCON_SettingsForSonar = 0
        # 进攻型电子对抗措施（干扰机）管控规则设置模式
        self.m_EMCON_SettingsForOECM = 0
        # 武器使用规则的武器DBID
        self.m_WRA_WeaponRule_WeaponDBID = ""
        # 武器使用规则
        self.m_WRA_WeaponRule = ""
        # 使用核武器
        self.bchkUseNuclerWeapon = False
        # 武器控制状态对空是否允许用户编辑
        self.bchkWeaponStateAir = False
        # 武器控制状态对海是否允许用户编辑
        self.bchkWeaponStateSea = False
        # 武器控制状态对潜是否允许用户编辑
        self.bchkWeaponStateSeaLatent = False
        # 武器控制状态对地是否允许用户编辑
        self.bchkWeaponStateland = False
        # 受到攻击时忽略计划航线是否允许用户编辑
        self.bchkIgnoreRoutes = False
        # 接战模糊位置目标是否允许用户编辑
        self.bchkFuzzlocationOfTheReceIvingstation = False
        # 接战临机出现目标是否允许用户编辑
        self.bchkImminentTarget = False
        # 受攻击时忽略电磁管控是否允许用户编辑
        self.bchkIgnoreElectromagneticControl = False
        # 鱼雷使用动力航程是否允许用户编辑
        self.bchkTopedopower = False
        # 自动规避是否允许用户编辑
        self.bchkAutoAcoid = False
        # 加油/补给是否允许用户编辑
        self.bchkComeOn = False
        # 对所选单元进行加油/补给是否允许用户编辑
        self.bchkSelectUnitComeOn = False
        # 对盟军单元进行加油/补给是否允许用户编辑
        self.bchkAlliedUnitComeOn = False
        # 空战节奏是否允许用户编辑
        self.bchkAirOpsTempo_Player = False
        # 快速出动是否允许用户编辑
        self.bchkQTA_Player = False
        # 燃油状态，预先规划是否允许用户编辑
        self.bchkBingoJoker_Player = False
        # 燃油状态—返航是否允许用户编辑
        self.bchkBingoJokerRTB_Player = False
        # 武器状态, 预先规划是否允许用户编辑
        self.bchkWeaponStateFirast = False
        # 武器状态-返航是否允许用户编辑
        self.bchkWeaponStateReturn = False
        # 空对地扫射(航炮)是否允许用户编辑
        self.bchkAirToGroundUserEdit = False
        # 抛弃弹药是否允许用户编辑
        self.bchkAbandonedAmmunition = False
        # 以反舰模式使用舰空导弹规则是否允许用户编辑
        self.bchkSAM_ASUW_Player = False
        # 与目标保持一定距离规则是否允许用户编辑
        self.bchkKeepTargetDistance = False
        # 规避搜索规则是否允许用户编辑
        self.bchkToAvoidTheSearch = False
        # 探测到威胁进行下潜规则是否允许用户编辑
        self.bchkThreatWasDetectedAndDived = False
        # 电池充电 %, 出航/阵位是否允许用户编辑
        self.bchkSetSail = False
        # 电池充电%, 进攻/防御是否允许用户编辑
        self.bchkAttack = False
        # 使用AIP推进技术是否允许用户编辑
        self.bchkAPI = False
        # 吊放声纳是否允许用户编辑
        self.bchkDippingSonar = False
      
    def SetDoctrineAir(self,sideName,fireState):
        '''
        设置单元的攻击条令（自动攻击(FREE)、限制开火(TIGHT)、不能开火 (HOLD)、与上级一致(INHERITED)）
        用法
        武器控制状态，对空
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_air = "0"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对海
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_surface = "2"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对潜
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_subsurface = "0"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对地
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_land = "2"}) 
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetDoctrine({side ='%s' }, {weapon_control_status_air ='%s}'})" % (sideName, fireState))

    def doctrine_switch_radar(self, switch_on):
        """
        条令中，电磁管控设置，设置雷达
        :param switch_on: bool, 雷达打开或者静默，True:打开
        :return:
        """
        if switch_on:
            set_str = 'Radar=Active'
        else:
            set_str = 'Radar=Passive'

        if self.category == 'Side' or self.category == 'Mission':
            id_str = self.strName
        else:
            id_str = self.strGuid

        cmd_str = "ScenEdit_SetEMCON('%s', '%s', '%s')" % (self.category_str, id_str, set_str)
        self.mozi_server.sendAndRecv(cmd_str)

    def doctrine_SetEMCON_Inherit(self, bTrueOrFalse):
        """
        设置电磁管控是否与上级一致
        :param bTrueOrFalse: bool，是否与上级一致
        :return:
        """
        if bTrueOrFalse:
            bTrueOrFalse = 'yes'
        elif not bTrueOrFalse:
            bTrueOrFalse = 'no'
        else:
            print('Error：bTrueOrFalse参数输入错误！')
        cmd = "Hs_SetInLineWithSuperiors('{}','{}')".format(self.strGuid, bTrueOrFalse)
        return self.mozi_server.sendAndRecv(cmd)

    def doctrine_engaging_ambiguous_targets(self, towards_ambigous_target):
        """
        接战模糊位置目标
        :param towards_ambigous_target: BehaviorTowardsAmbigousTarget
        :return:
        """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{engaging_ambiguous_targets=' + str(
                                                                     towards_ambigous_target.value) + '}')
        elif self.category == 'Mission':
            if towards_ambigous_target.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
        else:
            if towards_ambigous_target.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{engaging_ambiguous_targets=' + str(
                                                                         towards_ambigous_target.value) + '}')

    def doctrine_ignore_plotted_course(self, ignore_plotted_courseEnum):
        """
        攻击时忽略计划航线设置
        :param ignore_plotted_courseEnum:IgnorePlottedCourseWhenAttacking，选择枚举
        :return:
        """
        if self.category == 'Side':
            if ignore_plotted_courseEnum == 0:

                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{ignore_plotted_course=' + 'true' + '}')
        elif self.category == 'Mission':
            if ignore_plotted_courseEnum.value == 0:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_plotted_course=' + 'false' + '}')
            if ignore_plotted_courseEnum.value == 1:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_plotted_course=' + 'true' + '}')
            if ignore_plotted_courseEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_plotted_course=\"inherit\"}')
        else:
            if ignore_plotted_courseEnum == 0:
                return self.mozi_server.sendAndRecv(
                    "ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=false})" % self.strGuid)
                # return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}','{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == 1:
                return self.mozi_server.sendAndRecv(
                    "ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=true})" % self.strGuid)
                # return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}','{ignore_plotted_course=' + 'true' + '}')
            elif ignore_plotted_courseEnum == 2:
                return self.mozi_server.sendAndRecv(
                    "ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=\"inherit\"})" % self.strGuid)

    def doctrine_engage_opportunity_targets(self, engage_opportunity_targetsEnum):
        """
            接战临机出现目标
            :param engage_opportunity_targetsEnum: EngageWithContactTarget, 枚举
            :return:
            """
        if self.category == 'Side':
            if engage_opportunity_targetsEnum == 'No_Only':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{engage_opportunity_targets=' + 'true' + '}')
        elif self.category == 'Mission':
            if engage_opportunity_targetsEnum == 'No_Only':
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{engage_opportunity_targets=' + 'true' + '}')
            elif engage_opportunity_targetsEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{engage_opportunity_targets=\"inherit\"}')
        else:
            if engage_opportunity_targetsEnum == 'No_Only':
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{engage_opportunity_targets=' + 'true' + '}')
            elif engage_opportunity_targetsEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{engage_opportunity_targets=\"inherit\"}')

    def doctrine_ignore_emcon_under_attack(self, ignore_emcon_while_under_attackEnum):
        """
            受到攻击忽略电磁管控
            :param ignore_emcon_while_under_attackEnum: IgnoreEMCONUnderAttack, 枚举
            :return:
            """
        if self.category == 'Side':
            if ignore_emcon_while_under_attackEnum == 0:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{ignore_emcon_while_under_attack=' + 'false' + '}')
            elif ignore_emcon_while_under_attackEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{ignore_emcon_while_under_attack=' + 'true' + '}')
        elif self.category == 'Mission':
            if ignore_emcon_while_under_attackEnum.value == 0:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_emcon_while_under_attack=' + 'false' + '}')
            if ignore_emcon_while_under_attackEnum.value == 1:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_emcon_while_under_attack=' + 'true' + '}')
            if ignore_emcon_while_under_attackEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{ignore_emcon_while_under_attack=\"inherit\"}')
        elif self.category == 'Unit':
            if ignore_emcon_while_under_attackEnum == 0:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{ignore_emcon_while_under_attack=' + 'false' + '}')
            elif ignore_emcon_while_under_attackEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{ignore_emcon_while_under_attack=' + 'true' + '}')
            elif ignore_emcon_while_under_attackEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{ignore_emcon_while_under_attack=\"inherit\"}')


    def doctrine_automatic_evasion(self, automatic_evasionEnum):
        """
            自动规避
            :param automatic_evasionEnum: AutomaticEvasion, 枚举
            :return:
            """
        if self.category == 'Side':
            if automatic_evasionEnum == 0:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{automatic_evasion=' + 'false' + '}')
            elif automatic_evasionEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{automatic_evasion=' + 'true' + '}')
        elif self.category == 'Mission':
            if automatic_evasionEnum.value == 0:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{automatic_evasion=' + 'false' + '}')
            if automatic_evasionEnum.value == 1:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{automatic_evasion=' + 'true' + '}')
            if automatic_evasionEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{automatic_evasion=\"inherit\"}')
        else:
            if automatic_evasionEnum == 0:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{automatic_evasion=' + 'false' + '}')
            elif automatic_evasionEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{automatic_evasion=' + 'true' + '}')
            elif automatic_evasionEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{automatic_evasion=\"inherit\"}')


    def doctrine_air_operations_tempo(self, air_operations_tempoEnum):
        """
            空战节奏
            :param air_operations_tempoEnum: AirOpsTempo, 枚举
            :return:
            """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{air_operations_tempo=' + str(
                                                                     air_operations_tempoEnum.value) + '}')
        elif self.category == 'Mission':
            if air_operations_tempoEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{air_operations_tempo=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{air_operations_tempo=' + str(air_operations_tempoEnum.value) + '}')
        else:
            if air_operations_tempoEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{air_operations_tempo=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                     '{air_operations_tempo=' + str(
                                                                         air_operations_tempoEnum.value) + '}')


    def doctrine_fuel_state_planned(self, fuel_state_plannedEnum):
        """
            燃油状态，预先规划
            :param fuel_state_plannedEnum: FuelState, 枚举
            :return:
            """

        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{fuel_state_planned=' + str(
                                                                     fuel_state_plannedEnum.value) + '}')
        elif self.category == 'Mission':
            if fuel_state_plannedEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{fuel_state_planned=\"inherit\"}')
            return self.mozi_server.setconIntendedTargetDoctrine(
                '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                '{fuel_state_planned=' + str(fuel_state_plannedEnum.value) + '}')
        else:
            if fuel_state_plannedEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{fuel_state_planned=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{fuel_state_planned=' + str(
                                                                         fuel_state_plannedEnum.value) + '}')


    def doctrine_fuel_state_rtb(self, fuel_state_rtbEnum):
        """
            燃油状态，返航
            :param fuel_state_rtbEnum: FuelStateRTB, 枚举
            :return:
            """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{fuel_state_rtb=' + str(
                                                                     fuel_state_rtbEnum.value) + '}')
        elif self.category == 'Mission':
            if fuel_state_rtbEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{fuel_state_rtb=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
        else:
            if fuel_state_rtbEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{fuel_state_rtb=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{fuel_state_rtb=' + str(
                                                                         fuel_state_rtbEnum.value) + '}')

    def doctrine_weapon_state_planned(self, weapon_state_plannedEnum):
        """
            武器状态，预先规划
            :param weapon_state_plannedEnum:WeaponStatePlanned, 枚举
            :return:
            """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{weapon_state_planned=' + str(
                                                                     weapon_state_plannedEnum.value) + '}')
        elif self.category == 'Mission':
            if weapon_state_plannedEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{weapon_state_planned=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                    '{weapon_state_planned=' + str(weapon_state_plannedEnum.value) + '}')
        else:
            if weapon_state_plannedEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{weapon_state_planned=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{weapon_state_planned=' + str(
                                                                         weapon_state_plannedEnum.value) + '}')

    def doctrine_weapon_state_rtb(self, weapon_state_rtbEnum):
        """
            武器状态-返航
            :param weapon_state_rtbEnum: WeaponStateRTB, 枚举
            :return:
            """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{weapon_state_rtb=' + str(
                                                                     weapon_state_rtbEnum.value) + '}')
        elif self.category == 'Mission':
            if weapon_state_rtbEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{weapon_state_rtb=\"inherit\"}')
            return self.mozi_server.setconIntendedTargetDoctrine(
                '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                '{weapon_state_rtb=' + str(weapon_state_rtbEnum.value) + '}')
        else:
            if weapon_state_rtbEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{weapon_state_rtb=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{weapon_state_rtb=' + str(
                                                                         weapon_state_rtbEnum.value) + '}')

    def doctrine_gun_strafing(self, gun_strafingEnum):
        """
        空对地扫射
        :param gun_strafingEnum: GunStrafeGroundTargets, 枚举
        :return:
        """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.m_Side + '"}',
                                                                 '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        elif self.category == 'Mission':
            if gun_strafingEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.m_Side + '",mission="' + self.strName + '"}', '{gun_strafing=\"inherit\"}')
            return self.mozi_server.setconIntendedTargetDoctrine(
                '{side="' + self.m_Side + '",mission="' + self.strName + '"}',
                '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        else:
            if gun_strafingEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                                     '{gun_strafing=\"inherit\"}')
            else:
                self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.strGuid + '"}',
                                                              '{gun_strafing=' + str(gun_strafingEnum.value) + '}')

  
    def withdraw_on_damage(self, select_type):
        """
        满足如下条件时撤退 - -毁伤程度大于
        :param select_type: DamageThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':

            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_damage={}}})'.format(self.m_Side,
                                                                                            select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def withdraw_on_fuel(self, select_type):
        """
        满足如下条件时撤退--燃油少于
        :param select_type: FuelQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_fuel={}}})'.format(self.m_Side, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def withdraw_on_attack(self, select_type):
        """
        满足如下条件时撤退--主要攻击攻击武器至少处于
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_attack={}}})'.format(self.m_Side,
                                                                                             select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_attack={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_attack={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def withdraw_on_defence(self, select_type):
        """
        满足如下条件时撤退--主要防御武器至少
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':

            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_defence={}}})'.format(self.m_Side,
                                                                                            select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_defence={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_defence={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def deploy_on_damage(self, select_type):
        """
        满足如下条件时重新部署--毁伤程度小于
        :param select_type: DamageThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_damage={}}})'.format(self.m_Side, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_damage={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_damage={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def deploy_on_fuel(self, select_type):
        """
        满足如下条件时重新部署--燃油至少处于
        :param select_type: FuelQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.m_Side, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.m_Side,
                                                                                                        self.strName,
                                                                                                        select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_fuel={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def deploy_on_attack(self, select_type):
        """
        满足如下条件时重新部署--主要攻击武器处于
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_attack={}}})'.format(self.m_Side, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_attack={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_attack={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def deploy_on_defence(self, select_type):
        """
        满足如下条件时重新部署--主要防御武器处于
        :param select_type        
        : WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_defence={}}})'.format(self.m_Side, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_defence={}}})'.format(
                self.m_Side, self.strName, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_defence={}}})'.format(self.strGuid, select_type)
            return self.mozi_server.sendAndRecv(table)

    def set_object_doctrine(self, select_object, doctrine):
        """
        函数功能：设置指定对象的条令
        函数类型：编辑函数
        用法：ScenEdit_SetDoctrine({side="美国"},{use_nuclear_weapons= "no", weapon_control_status_air="0"})
        :param select_object:(指定对象的属性组成的表对象) 指定的对象
        :param doctrine:条令属性组成的table对象，类似于{use_nuclear_weapons= false,weapon_control_status_air=1})
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_SetDoctrine({},{})".format(select_object, doctrine))

    def set_in_line_with_superiors(self, beTrue):
        """
        函数功能：设置单元条令电磁管控与上级的一致性
        函数类型：推演函数
        :param beTrue: bool值，一致性状态标识符（'yes'：一致，'no'：不一致），不能为空。
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_SetInLineWithSuperiors('{}',{})".format(self.strGuid, beTrue))

    def unit_obeys_EMCON(self, is_obey):
        """
        函数功能：设置单元是否遵循电磁管控
        函数类型：推演函数
        :param is_obey: bool(True 或 False)
        :return: void
        """
        state = str(is_obey).lower()
        return self.mozi_server.sendAndRecv("Hs_UnitObeysEMCON('{}', {})".format(self.strGuid, state))

    def setEMCON(self, objectType, objectName, emcon):
        """
        函数功能：设置指定对象的电磁管控
        函数类型：推演函数
        :param objectType: 字符串。电磁管控对象类别；
        :param objectName: 字符串。电磁管控对象名称或 GUID；
        :param emcon:传感器类型和传感器状态
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_SetEMCON('{}','{}','{}')".format(objectType, objectName, emcon))

    def setDoctrineWRA(self, object_table, rule_table):
        """
        函数功能：设置武器使用规则
        函数类型：推演函数
        :param object_table: 指定对象
        :param rule_table:指定对象武器使用规则
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_SetDoctrineWRA({},{})".format(object_table, rule_table))

    def resetDoctrine(self, guid, LeftMiddleRight, EnsembleWeaponEMCON):
        """
        函数功能：根据上级单位条令内容设置下级单位在相关条令上与上级一致
        函数类型：推演函数
        :param guid:推演方、任务、单元或编组的 GUID
        :param LeftMiddleRight: Left：重置作战条令，Middle 重置关联的作战单元，Right 重置关联的使命任务
        :param EnsembleWeaponEMCON: Ensemble：总体，EMCON 电磁管控设置，Weapon 武器使用规则
        :return:
        例子：local a=ScenEdit_GetUnit({name='飞机#3'})
              Hs_ResetDoctrine(a.guid,'Left','Ensemble')
        """
        return self.mozi_server.sendAndRecv("Hs_ResetDoctrine('{}','{}','{}')".format(guid, LeftMiddleRight, EnsembleWeaponEMCON))

