#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : side.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################
from abc import ABCMeta, abstractmethod
import re
import logging

from ..entitys.mission import CMission
from ..entitys.activeunit import CActiveUnit


########################################################################
class CSide:
    '''方'''

    # ----------------------------------------------------------------------
    def __init__(self, side_guid, mozi_server):
        """Constructor"""
        self.mozi_server = mozi_server
        self.__zone_index_increment = 1  # 创建封锁区或禁航区的自增命名序号
        self.__reference_point_index_increment = 1  # 创建参考点的自增命名序号
        self.missions = {}  # key:key:mission name, value: Mission instance 
        #实体
        self.aircrafts = {}  # key:unit guid, value: Unit instance
        self.facilitys = {}  # key:unit guid, value: Unit instance
        self.ships = {}
        self.submarines = {}
        self.weapons = {}
        self.satellites = {}
        # 目标
        self.contacts = {}  # key:contact guid, value, contact instance
        # 编组
        self.groups = {}
        # 点
        self.acrionPoints = {}
        # 参考点
        self.referencePoints = {}
        # 条令
        self.doctrine = None
        # 天气
        self.weather = None
        # 消息
        self.logged_messages = {}
        self.current_point = 0  # 当前得分
        self.point_record = []  # 得分记录
        self.simulate_time = ""  # 当前推演时间
        self.last_step_missing = {}  # 当前决策步损失的单元（我方），丢掉或击毁的单元（敌方）
        self.last_step_new = {}  # 当前决策步新增的单元（我方），新增的情报单元（敌方）
        self.all_units = {}
        self.activeunit = {}
        self.strName = ""  # 名称
        self.strGuid = side_guid  # Guid
        self.m_PosturesDictionary = []  # 获取针对其它推演方的立场
        self.m_Doctrine = []  # 作战条令
        self.m_ProficiencyLevel = []
        self.m_AwarenessLevel = []
        self.m_PosturesDictionary = []
        self.iTotalScore = 0.0
        self.m_Expenditures = []  # 战损
        self.m_Losses = []  # 战耗
        self.iScoringDisaster = 0.0  # 完败阀值
        self.iScoringTriumph = 0.0  # 完胜阀值
        self.bCATC = False  # 自动跟踪非作战单元
        self.bCollectiveResponsibility = False  # 集体反应
        self.bAIOnly = False  # 只由计算机扮演
        self.strBriefing = ''  # 简要
        self.strCloseResult = ''  # 战斗结束后的结果
        self.fCamerAltitude = 0.0  # 中心点相机高度
        self.fCenterLatitude = 0.0  # 地图中心点纬度
        self.fCenterLongitude = 0.0  # 地图中心点经度
        self.strSideColorKey = ''  # 推演方颜色Key
        self.strFriendlyColorKey = ''  # 友方颜色Key
        self.strNeutralColorKey = ''  # 中立方颜色Key
        self.strUnfriendlyColorKey = ''  # 非友方颜色Key
        self.strHostileColorKey = ''  # 敌方颜色Key
        self.iSideStopCount = 0  # 推演方剩余停止次数
        self.m_ScoringLogs = []
        self.m_ContactList = []  # 所有的目标
        self.m_WarDamageOtherTotal = []  # 战损的其它统计，包含但不限于(统计损失单元带来的经济和人员损失)

    def get_all_unitinfo(self):
        '''
        获取本方所有实体的信息
        通过本方单元字典拼接而成
        update 去重合并
        '''
        all_unitinfo = {}
        all_unitinfo.update(self.aircrafts)
        all_unitinfo.update(self.ships)
        all_unitinfo.update(self.satellites)
        all_unitinfo.update(self.submarines)
        all_unitinfo.update(self.weapons)
        all_unitinfo.update(self.facilitys)
        return all_unitinfo

    def scen_edit_get_score(self, side_name, mozi_server):
        '''
        获取方的分数  
        param: 
        side_name ：要获取的方的分数
        mozi_server ：调用服务器的基础类
        return ：60(分数)
        
        '''
        lua_str = '''ret = ScenEdit_GetScore("%s")
                print(ret)
                ''' % (side_name)
        return float(self.mozi_server.sendAndRecv(lua_str))

    def scen_edit_set_score(self, score):
        '''
        设置指定阵营的分数
        '''
        return self.mozi_server.sendAndRecv("ReturnObj(ScenEdit_SetScore('{}',{}))".format(self.strName, score))

    def get_mission_by_name(self, mission_name):
        """
        通过任务名获取任务对象
        :return:
        """
        if mission_name in self.missions:
            return self.missions[mission_name]
        else:
            return None

    def get_unit_by_guid(self, guid):
        """
        获取实体
        :param guid: str, 实体guid/
        :return: Unit, 作战单元
        """

        if guid in self.aircrafts:
            return self.aircrafts[guid]
        if guid in self.facilitys:
            return self.facilitys[guid]
        if guid in self.weapons:
            return self.weapons[guid]
        if guid in self.ships:
            return self.ships[guid]
        if guid in self.satellites:
            return self.satellites[guid]
        if guid in self.submarines:
            return self.submarines[guid]
        return None

    def get_contact(self, contact_guid):
        """
        获取情报对象
        :param contact_guid:  情报对象guid, 非实际单元guid
        :return:
        """
        if contact_guid in self.contacts:
            return self.contacts[contact_guid]
        else:
            return None

    def get_contacts(self):
        """
        获取本方当前已知的所有情报实体
        :return: dict, {'guid':'name'}
        """
        lua_arg = "print(VP_GetSide({side = '%s'}).contacts)" % self.side_name
        return self.mozi_server.sendAndRecv(lua_arg)

    def get_elevation(self, coord_point):
        """
        获取某点（纬经度）
        :param coord_point: tuple, (float, float) (lat, lon)
        :return: int, 地形高程数据
        """
        lua_cmd = "ReturnObj(World_GetElevation ({latitude='%lf',longitude='%lf'}))" % (coord_point[0], coord_point[1])
        return int(self.mozi_server.sendAndRecv(lua_cmd))

    def reference_point_add(self, points):
        """
        添加一个或多个参考点
        :param points: tuple, 或list,  参考点列表,例:(40.2, 49.6) 或 [(40, 39.0), (41, 39.0)]，其中纬度值在前，经度值在后
                                                或者 (40.2, 49.6, 'RP002') 或 [(40, 39.0, 'RP1'), (41, 39.0, 'RP2')]，已传入参考点命名
        :return: ['point_name1','point_name2']点集名称
        """
        if not points:
            return None

        points_name = None
        if isinstance(points, tuple):
            # 判断参数是否元组
            if len(points) == 2:
                points_name = "RP_AUTO_CREATE%d" % self.__reference_point_index_increment
                self.__reference_point_index_increment += 1
                self.pointname2location[points_name] = points
            elif len(points) == 3:
                points_name = points[2]
                self.pointname2location[points_name] = points[0:2]
            else:
                return None
            self.mozi_server.addReferencePoint(side=self.side_name, pointName=points_name, lat=points[0], lon=points[1],
                                               highlighted='true')

        elif isinstance(points, list):
            # 判断参数是否参考点列表
            points_name = []
            for point in points:
                if isinstance(point, tuple):
                    p_name = self.reference_point_add(point)
                    if p_name is not None:
                        points_name.append(p_name)
        return points_name

    def set_reference_point(self, rp_name, new_coord):
        """
        设置参考点的位置
        :param rp_name: str, 参考点名称
        :param new_coord: tuple, 新的经纬度位置 (lat, lon)
        :return:
        """
        set_str = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(self.side_name, rp_name,
                                                                                               new_coord[0],
                                                                                               new_coord[1])
        self.pointname2location[rp_name] = new_coord
        return self.mozi_server.sendAndRecv(set_str)

    def delete_reference_point(self, rp_name):
        """
        删除参考点
        :param rp_name:  str, 参考点名称
        :return:
        """
        set_str = 'ScenEdit_DeleteReferencePoint({name="%s",side="%s"})' % (rp_name, self.side_name)
        return self.mozi_server.sendAndRecv(set_str)

    def scenEdit_addMission(self, side, missionName, model, detailed):
        '''
         #新建任务 complate
        '''
        add_mission = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(side, missionName, model, detailed)
        return self.mozi_server.sendAndRecv(add_mission)

    def scenEdit_addMission(self, missionName, model, detailed):
        """

        :param missionName:
        :param model:
        :param detailed:
        :return:
        """

        add_mission = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, missionName, model,
                                                                                 detailed)
        return self.mozi_server.sendAndRecv(add_mission)

    def add_prosecution_zone(self, mission_name, point_list):
        """
        增加巡逻任务的警戒区
        :param mission_name: str, 任务名
        :param point_list: list, list, 参考点列表,例:[(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)]，其中纬度值在前，经度值在后，(40, 39.0)中,latitude = 40, longitude = 39.0
                            或者[(40, 39.0, 'RP1'), (41, 39.0, 'RP2'), (41, 40.0, 'RP3'), (40, 40.0, 'RP4')]
                            或者['RP1', 'RP2'，'RP3'，'RP4']，传入参考点名称要求提前创建好参考点
        :return:
        """
        # self.mozi_server.setMission(self.side_name, mission_name,
        # '{' + self.__get_zone_str(point_list).replace('Zone', 'prosecutionZone') + '}')
        pass

    def create_strike_mission(self, name, mission_type):
        """
        创建打击任务
        :param name: str, 任务名
        :param mission_type: MissionStrikeType, 打击任务类型，对空打击，对地打击等
        :return: Mission, 任务实体
        """
        pass

    def create_support_mission(self, name, point_list):
        """
        创建支援任务, 例子：
            create_support_mission('空中支援', [(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)])
        :param name: str, 任务名
        :param point_list: list, 参考点列表,例:[(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)]，其中纬度值在前，经度值在后，(40, 39.0)中,latitude = 40, longitude = 39.0
                            或者[(40, 39.0, 'RP1'), (41, 39.0, 'RP2'), (41, 40.0, 'RP3'), (40, 40.0, 'RP4')]
                            或者['RP1', 'RP2'，'RP3'，'RP        4']，传入参考点名称要求提前创建好参考点
        :return: Mission, 任务实体
        """
        pass

    def __save_mission(self, mission_name, mission_return_str, mission_category):
        """
        保存任务到本方，方便以后调用
        :param mission_name: 任务名
        :param mission_return_str: 任务调用返回值
        :return: Mission, Mission实例
        """
        pass

    def delete_mission(self, mission_name):
        """
        删除任务
        :param mission_name: str, 任务名称
        :return:
        """
        lua = 'print(ScenEdit_DeleteMission("%s", "%s"))' % (self.side_name, mission_name)
        self.mozi_server.sendAndRecv(lua)
        del self.missions[mission_name]

    def zone_remove(self, zone_guid):
        """
        删除禁航区或封锁区域
        :param zone_guid: str, 区域的guid
        :return:
        """
        # return self.mozi_server.removeZone(self.side_name, zone_guid)
        pass

    def zone_add_no_navigate(self, reference_points, **kwargs):
        """
        定义禁航区
        :param reference_points:list, 参考点列表
        :param kwargs:  Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0=  'false' (只有禁航区才需要设置)
        :return:str, zone guid
        """
        point_names = self.reference_point_add(reference_points)
        point_count = len(point_names)
        if not point_count:
            return None

        area_description = 'Area={"'
        for name in point_names[: point_count - 1]:
            area_description += name + '","'
        name = point_names[-1]
        area_description += name + '"}'

        table_arg = '{'
        table_arg += ('Description="禁航区' + str(self.__zone_index_increment)) + '",' + area_description + '}'
        self.__zone_index_increment += 1
        zone_guid = self.mozi_server.addZone(self.side_name, '0', table_arg)
        if len(kwargs) > 0:
            self.zone_set(zone_guid, kwargs)
        else:
            self.zone_set(zone_guid, Isactive=1, Affects=0, Locked=0)
        return zone_guid

    def zone_add_exclusion(self, reference_points, **kwargs):
        """
        定义封锁区
        :param reference_points:list, 参考点列表
        :param kwargs:  Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0=  'false' (只有禁航区才需要设置)
        :return:str, zone guid
        """
        # point_names = self.reference_point_add(reference_points)
        # point_count = len(point_names)
        # if not point_count:
        # return None

        # area_description = 'Area={"'
        # for name in point_names[: point_count - 1]:
        # area_description += name+'","'
        # name = point_names[-1]
        # area_description += name+'"}'

        # table_arg = '{'
        # table_arg += ('Description="封锁区' + str(self.__zone_index_increment)) + '",' + area_description + '}'
        # self.__zone_index_increment += 1
        # zone_guid = self.mozi_server.addZone(self.side_name, '1', table_arg)
        # if len(kwargs) > 0:
        # self.zone_set(zone_guid, kwargs)
        # else:
        # self.zone_set(zone_guid, Isactive=1, Affects=0, Locked=0)
        # return zone_guid
        pass

    def zone_set(self, zone_guid, **kwargs):
        """
        修改禁航区和封锁区
        :param zone_guid: 禁航区和封锁区的guid
        :param kwargs:  Area：list 添加地图中选择的参考点(向区域列表中添加)(暂不支持,想要修改点请先删除再新建)
                        Description: string 名字
                        Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0='false' (只有禁航区才需要设置)
                        MarkAs： int 2=非友方，3=敌方（封锁区才有的设置）
                        RPVISIBLE: int 1=true 0=false
        :return:
        """
        # table = '{'
        # for key, value in kwargs.items():
        # if key == 'Isactive':
        # if value == 1:
        # table += ',Isactive=true'
        # elif value == 0:
        # table += ',Isactive=false'
        # if key == 'Affects':
        # if value == 0:
        # table += ',Affects={"Aircraft"}'
        # elif value == 1:
        # table += ', Affects={"Ship"}'
        # if key == 'MarkAs':
        # if value == 2:
        # table += ', MarkAs=2'
        # elif value == 3:
        # table += ', MarkAs=3'
        # if key == 'RPVISIBLE':
        # if value == 1:
        # table += ",RPVISIBLE=true"
        # elif value == 0:
        # table += ",RPVISIBLE=false"
        # if key == 'Locked':
        # if value == 1:
        # table += ', Locked=true'
        # elif value == 0:
        # table += ', Locked=false'
        # if table[1] == ',':
        # table = table.replace(',', '', 1)
        # table += '}'
        # return self.mozi_server.setZone(self.side_name, zone_guid, table)
        pass

    def group_add(self, list_unit_guid):
        """
        将多个单元作为一个编队
        :param list_unit_guid: list, 例：['2abc947e-8352-4639-9184-641706730018','640a7c08-a17a-4fba-b055        -07b568f22df5']
        :return:
        """
        list_unit_guid = str(list_unit_guid).replace('[', '{').replace(']', '}')
        return self.mozi_server.scenEdit_AddGroup(list_unit_guid)

    def group_add_unit(self, group_guid, unit_guid):
        """
        编队添加一个单元
        :param group_guid: 编队guid
        :param unit_guid: 作战单元guid
        :return:
        """
        table = '{guid="' + unit_guid + '",group="' + group_guid + '"}'
        lua_scrpt = "ScenEdit_SetUnit({})".format(table)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def air_group_out(self, air_guid_list):
        """
        编组出动
        :param air_guid_list:  list, 飞机的guid，  例子：['71136bf2-58ba-4013-92f5-2effc99d2wds','71136bf2-58ba-4013-92f5-2effc99d2fa0']
        :return:
        """
        table = str(air_guid_list).replace('[', '{').replace(']', '}')
        lua_scrpt = "Hs_LUA_AirOpsGroupOut('{}',{})".format(self.side_name, table)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def hold_position_all_unit(self, is_hold):
        """
        类别：推演所用函数
        保持所有单元阵位，所有单元停止机动，留在原地
        :param is_hold: bool
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_HoldPositonAllUnit('{}',{})".format(self.side_name, str(is_hold).lower()))

    def scenEdit_setEvent(self, eventName, model):
        '''
        #创建和设置事件 eventname为事件名称 
        #eventTableMode为{mode='add',IsActive = false, IsRepeatable=true, Probability =100,IsShown = false} 
        # mode 是类型 添加删除修改之类的 isactive 是否激活  IsRepeatable 是否重复 Probability概率 IsShown是否显示
        返回乱执行是否成功 （string）
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetEvent ('%s',{mode='%s'})" % (eventName, model))

    def scenEdit_setAction(self, actionTableMode):
        '''
        创建动作和设置动作
        actionTableMode 为{Description='想定结束',mode='add',type='endscenario'}
        Description 动作名称 mode 操作类型 类似有添加删除 type为类型 有想定结束单元移动等
        返回乱执行是否成功 （string）
        '''
        return self.mozi_server.sendAndRecv(" ScenEdit_SetAction({})".format(actionTableMode))

    def scenEditSetTrigger(self, triggerTableMode):
        '''
        创建和设置触发器
        triggerTableMode 为 {Description='航母被摧毁',mode='add',type= "unitdestroyed",TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"}}
        Description 触发器名称 mode 操作类型同上 type触发器类型 类似有单元被摧毁 单元被毁伤之类的 
        TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"} 是单元被毁伤和单元被摧毁的 TARGETSIDE为单元所在方  TARGETTYPE 为类型还有子类型参数
        返回乱执行是否成功 （string）
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetTrigger ({})".format(triggerTableMode))

    def set_condition(self, descrp, mode, type, observersideID, targetsideID, posture, NOT):
        """
        函数功能：编辑函数
        函数类型：以多种模式设置多种条件
        @param table:表对象，
        @return:
        """
        lua_scrpt = "ScenEdit_SetCondition ({'{}','{}','{}','{}','{}','{}',{}})".format(descrp, mode, type,
                                                                                        observersideID, targetsideID,
                                                                                        posture, NOT)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def scenEdit_setEventTrigger(self, eventName, mode, triggername, replacedby=None):
        '''
        为事件添加触发器
        eventName 事件名称
        triggername 触发器名称
        mode 操作类型
        返回乱执行是否成功 （string）
        '''
        if replacedby is None:
            lua_scrpt = "ScenEdit_SetEventTrigger('%s', {mode = '%s',name = '%s'})" % (eventName, mode, triggername)
        else:

            lua_scrpt = "ScenEdit_SetEventTrigger('%s', {mode = '%s',name = '%s' ,replacedby= ''})" %(
                eventName, mode,self.strName,replacedby)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def scenEditSetEventAction(self, eventName, mode, name):
        '''
        为事件添加动作
        eventName 事件名称
        actionName 动作器名称
        mode 操作类型
        返回乱执行是否成功 （string）
        '''
        lua_scrpt = "ScenEdit_SetEventAction('%s', {mode = '%s',name = '%s'})" % (eventName, mode, name)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def set_del_event_condition(self, eventname, mode, name):
        """
        作者：赵俊义
        日期：2020-3-12
        函数功能：删除事件的条件
        函数类别：编辑函数
        :param eventname:事件类型
        :param mode:操作类型
        :param name:事件名称
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_SetEventCondition('{}',{mode='{}',name='{}'})".format(eventname, mode, name))

    def set_edit_event_condition(self, eventname, mode, name, replaceby):
        """
        作者：赵俊义
        日期：2020-3-12
        函数功能：编辑事件的条件
        函数类别：编辑函数
        :param eventname:事件类型
        :param mode:操作类型
        :param name:事件名称
        :param replaceby:替换为某个事件
        :return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_SetEventCondition('{}',{mode='{}',name='{}', replacedby='{}'})"
                                            .format(eventname, mode, name, replaceby))


    def addUnit(self, type, name, dbid, latitude, longitude):
        ''' 
        添加单元 complate
        '''
        lua_scrpt = (
                "ReturnObj(ScenEdit_AddUnit({side = '%s', type = '%s', name = '%s', dbid = %s, latitude = %s, longitude = %s}))"
                % (self.strName, type, name, dbid, latitude, longitude))
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def addAircarft(self, Type, name, dbid, latitude, longitude, loadoutid, heading, altitude):
        '''
        添加飞机
        '''
        lua_scrpt = (
                "ReturnObj(ScenEdit_AddUnit({type = '%s', name = '%s', loadoutid = %s, heading = %s, dbid = %s, side = '%s', Latitude=%s,Longitude=%s, altitude=%s))"
                % (Type, name, loadoutid, heading, dbid, self.strName, latitude, longitude, altitude))
        # 发送lua脚本
        result = self.mozi_server.sendAndRecv(lua_scrpt)

    def addAirToFacility(self, type, name, dbid, loadoutid, baseUnitGuid):
        '''
        往机场，码头添加单元       
        '''
        self.mozi_server.sendAndRecv(
            "ReturnObj(ScenEdit_AddUnit({ type = '%s', unitname = '%s',side='%s', dbid = %s, loadoutid = %s, base = '%s'}))"
            % (type, name, self.strName, dbid, loadoutid, baseUnitGuid))

    def delete_allUnit(self):
        '''
        删除本方所有单元
        '''
        return self.mozi_server.sendAndRecv("Hs_DeleteAllUnits({})".format(self.strName))

    def setEMCON(self, objectType, objectName, emcon):
        '''
        设置选定对象的 EMCON
        objectType 对象类型 'Side' / 'Mission' / 'Group' / 'Unit'
        objectName 对象名称 'Side Name or ID' / 'Mission Name or ID' / 'Group Name or ID' / 'Unit Name or ID'
        emcon 传感器类型和传感器状态 'Radar/Sonar/OECM=Active/Passive;' / 'Inherit'
        例 ：
        ScenEdit_SetEMCON(['Side' / 'Mission' / 'Group' / 'Unit'], ['Side Name or ID' / 'Mission Name or ID' / 
        'Group Name or ID' / 'Unit Name or ID'], ['Radar/Sonar/OECM=Active/Passive;' / 'Inherit'])
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetEMCON('{}','{}','{}')".format(objectType, objectName, emcon))

    def addReferencePoint(self, pointName, lat, lon):
        '''
        添加参考点
        pointName 参考点名称
        lat 纬度
        lon 经度
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_AddReferencePoint({side='%s', name='%s', lat=%s, lon=%s, highlighted=%s})" % (
                self.strName, pointName, lat, lon))

    def deployMine(self, mineType, mineCount, area):
        '''
        给某一方添加雷
        mineType 类型
        mineCount 数量
        area table类型 布雷区域
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_DeployMine('{}','{}',{},{})".format(self.strName, mineType, mineCount, area))

    def addOn_flyZone(self, description, area):
        '''
        添加禁航区
        description 禁航区名称
        area 区域 area={"RP-112","RP-113","RP-114","RP-115"}
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_AddZone('%s', {Description = '%s', Area = %s})" % (self.strName, description, area))

    def cloneETAC(self, table):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：克隆指定事件
        函数类别：推演所用的函数
        函数功能：克隆指定事件（触发器、条件、动作）
        table  {CLONETRIGGER = '", triggerGuid, "'} { CLONEEVENT = '", eventGuid, "' }
        { CLONECONDITION = '", conditionGuid, "' }     { CLONEACTION = '", actionGuid, "' }
        '''
        return self.mozi_server.sendAndRecv("Hs_CloneETAC({})".format(table))

    def reset_doctrine(self, GUID, LeftMiddleRight, EnsembleWeaponEMCON):
        '''
        Hs_ResetDoctrine 重置条令
        GUID 为要设置的推演方、任务、单元、编组 GUID
        LeftMiddleRight Left：重置作战条令，Middle 重置关联的作战单元，Right 重置关联的使命任务
        EnsembleWeaponEMCON Ensemble：总体，EMCON 电磁管控设置，Weapon 武器使用规则
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ResetDoctrine('{}','{}','{}')".format(GUID, LeftMiddleRight, EnsembleWeaponEMCON))

    def reset_allSide_scores(self):
        '''
        重置所有推演方分数
        '''
        return self.mozi_server.sendAndRecv("Hs_ResetAllSideScores()")

    def set_new_sideNaem(self, sideNewIdOrName):
        '''
        推演方重命名
        sideNewIdOrName 新名称
        '''
        return self.mozi_server.sendAndRecv("setNewSideNaem('{}','{}')".format(self.strName, sideNewIdOrName))

    def set_mark_contact(self, contact, relation):
        '''
        设置目标对抗关系
        '''
        lua = "Hs_SetMarkContact('%s', '%s', '%s')" % (self.strName, contact, relation)
        self.mozi_server.sendAndRecv(lua)

    def add_mission(self, mission_name, mission_type, ctype):
        lua = "ScenEdit_AddMission('%s','%s','%s',{type='%s'})" % (self.strName, mission_name, mission_type, ctype)
        self.mozi_server.sendAndRecv(lua)

    def assignUnitAsTarget(self, contact, unit_name):
        '''
        
        '''
        lua = "ScenEdit_AssignUnitAsTarget({'%s'}, '%s')" % (contact, unit_name)
        self.mozi_server.sendAndRecv(lua)

    def scenEdit_setScore(self, sidename_or_id, score, reason_for_change):
        '''
        类别：编辑所用函数
        函数功能：设置指定推演方的总分及总分变化原因。
        参数说明：
        1）sidename_or_id：字符串。推演方名称或 GUID；
        2）score：数值型。总分；
        3）reason_for_change：字符串。总分变化原因。
        '''
        lua = "ScenEdit_SetScore('%s',%s,'%s')" % (sidename_or_id, score, reason_for_change)
        self.mozi_server.sendAndRecv(lua)

    def contact_drop_target(self, contact_guid):
        '''
        类别：编辑用函数
        放弃目标
        不再将所选目标列为探测对象。
        contact_guid 字符串。目标 GUID
        Hs_ContactDropTarget('红方','a5561d29-b136-448b-af5d-0bafaf218b3d')
        '''
        lua_scrpt = "Hs_ContactDropTarget('%s','%s')" % (self.strName, contact_guid)
        self.mozi_server.sendAndRecv(lua_scrpt)

    def wcsfa_contact_types_all_unit(self, HoldTightFreeInheri):
        '''
        函数功能：控制所有单元对所有目标类型的攻击状态。 
        参数说明：  
        1）HoldTightFreeInheri    
        ted：控制状态标识符（'Hold'：禁止，'Tight'：限制，'Free'：自由，'Inherited'：按上级条令执行）
        '''
        lua = "Hs_WCSFAContactTypesAllUnit('%s','%s')" % (self.strGuid, HoldTightFreeInheri)
        self.mozi_server.scenAndRecv(lua)

    def lpcw_attack_allUnit(self, yesNoOrInherited):
        '''
        函数功能：所有单元攻击时是否忽略计划航线。 
        参数说明：
        1）'YesNoOrInherited'：控制状态标识符（'Yes'：忽略，'No'：不忽略，'Inherited'：按上级条令执行）
        '''
        lua = "Hs_LPCWAttackAllUnit('{}','{}')".format(self.strGuid, yesNoOrInherited)
        return self.sendAndRecv(lua)

    def get_side_info(self, side):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：获取推演方信息
        函数类别：推演所用的函数
        '''
        return self.mozi_server.sendAndRecv("VP_GetSide('{}')".format(side))

    def set_side_options(self, awareness, proficiency, isAIOnly, isCollRespons):
        '''
        作者：赵俊义
        日期：2020-3-7
        函数类别：推演所用的函数
        功能说明：设置推演方的名称、GUID、认知能力、训练水平、AI 操控、集
        体反应、自动跟踪非作战单元等组成的属性集合
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetSideOptions({},{},{},{},{})".format(self.strName, awareness, proficiency, isAIOnly,
                                                             isCollRespons))

    def get_side_attribute(self):
        '''
        作者：赵俊义
        日期：2020-3-9
        函数类别：推演所用的函数
        功能说明：获取推演方的名称、GUID、认知能力、训练水平、计算机操控、
                 集体反应、自动跟踪非作战单元等组成的属性集合。
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_GetSideOptions('{}')".format(self.strName))

    def get_ishuman_attribute(self):
        '''
        作者：赵俊义
        日期：2020-3-9
        函数类别：推演所用的函数
        功能说明：获取推演方操控属性，以便判断该推演方是人操控还是计算机操控
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_GetSideIsHuman('{}')".format(self.strName))

    def get_unit_attribute(self, unit):
        '''
        LUA_ScenEdit_GetUnit
        unit 选择单元。基于阵营和名字、或 GUID，推荐使用后者。
        name string 选择的单元名
        side string 单元所属的阵营名
        guid string 单元的 guid
        '''
        result = self.mozi_server.sendAndRecv(" ReturnObj(scenEdit_GetUnit({}))".format(unit))
        activeUnit = CActiveUnit()
        if result[:4] == "unit":
            # 处理接收的数据
            result_split = result[6:-1].replace('\'', '')
            result_join = ""
            result_join = result_join.join([one for one in result_split.split('\n')])
            list = result_join.split(',')
            for keyValue in list:
                keyValue_list = keyValue.split('=')
                if len(keyValue_list) == 2:
                    attr = keyValue_list[0].strip()
                    value = keyValue_list[1].strip()
                    if attr == "name":
                        activeUnit.name = value
                    elif attr == "side":
                        activeUnit.side = value
                    elif attr == "type":
                        activeUnit.type = value
                    elif attr == "subtype":
                        activeUnit.subtype = value
                    elif attr == "guid":
                        activeUnit.guid = value
                    elif attr == "proficiency":
                        activeUnit.proficiency = value
                    elif attr == "latitude":
                        activeUnit.latitude = float(value)
                    elif attr == "longitude":
                        activeUnit.longitude = float(value)
                    elif attr == "altitude":
                        activeUnit.altitude = float(value)
                    elif attr == "heading":
                        activeUnit.heading = float(value)
                    elif attr == "speed":
                        activeUnit.speed = float(value)
                    elif attr == "throttle":
                        activeUnit.throttle = value
                    elif attr == "autodetectable":
                        activeUnit.autodetectable = bool(value)
                    elif attr == "mounts":
                        activeUnit.mounts = int(value)
                    elif attr == "magazines":
                        activeUnit.magazines = int(value)
                    elif attr == "unitstate":
                        activeUnit.unitstate = value
                    elif attr == "fuelstate":
                        activeUnit.fuelstate = value
                    elif attr == "weaponstate":
                        activeUnit.weaponstate = value
            code = "200"
        else:
            code = "500"
        return code, activeUnit

    # def get_unit_attribute(self, unit_name):
    #     '''
    #     作者：赵俊义
    #     日期：2020-3-9
    #     函数类别：推演所用的函数
    #     功能说明：获取当前想定中已有单元对象
    #     @param unit_name: 单元名称
    #     @return: 单元对象，即单元的属性字典
    #     '''
    #     return self.mozi_server.sendAndRecv("VP_GetUnit ('{}')".format(unit_name))

    def copy_unit(self, unit_name, lon, lat):
        '''
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明：将想定中当前推演方中的已有单元复制到指定经纬度处
        @param unit_name: 被复制的单元名称
        @param lon: 经度
        @param lat: 纬度
        @return:
        '''
        return self.mozi_server.sendAndRecv("Hs_CopyUnit('{}',{},{})".format(unit_name, lon, lat))

    def delete_unit(self, unit_name):
        """
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明：删除当前推演方中指定单元
        @param unit_name: 单元名
        @return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_DeleteUnit('{}')".format(unit_name))

    def kill_unit(self, unit_name):
        """
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明：一旦推演执行到此函数，就摧毁指定推演方的指定单元，并输出该摧毁事件的消息，并影响到战损
                统计，与 ScenEdit_DeleteUnit差别较大（ScenEdit_DeleteUnit 在编辑中立即执行、不会输出
                消息、被删除单元不计入战斗损失统计表）
        @param unit_name:单元名称
        @return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_KillUnit({'{}','{}'})".format(self.strName, unit_name))

    def dele_all_units(self):
        """
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明:删除指定推演方所有单元
        @return:
        """
        return self.mozi_server.sendAndRecv("Hs_DeleteAllUnits({})".format(self.strName))

    def add_satellite(self, satellite_id, orbital):
        """
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明: 向推定推演方添加卫星
        @param satellite_id: 卫星的数据库id，数值型
        @param orbital:  卫星的轨道， 数值型
        @return:
        """
        return self.mozi_server.sendAndRecv("Hs_AddSatellite('{}',{},{})".format(self.strName, satellite_id, orbital))

    def side_scoring(self, scoringDisaster, scoringTriumph):
        """
        作者：赵俊义
        日期：2020-3-10
        函数类别：编辑所用的函数
        功能说明: 为指定推演方设置完败、完胜分数线。
        @param sideNameOrID: 推演方
        @param scoringDisaster: 完胜值
        @param scoringTriumph: 完败值
        @return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_SideScoring('{}','{}','{}')".format(self.strGuid, scoringDisaster, scoringTriumph))

    def remove_zone(self, sideName, zoneGUID):
        """
        作者: 赵俊义
        日期：2020-3-10
        函数功能：删除指定推演方的指定禁航区或封锁区
        函数类型：推演函数
        :param sideName: 方的名称
        :param zoneGUID: 区域guid
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_RemoveZone('{}','{}')".format(sideName, zoneGUID))

    def add_plan_way(self, nType, strWayName):
        """
        作者: 赵俊义
        日期：2020-3-10
        函数功能：为指定推演方添加一预设航线（待指定航路点）。
        函数类型：推演函数
        :param nType: 航线类型（0 是单元，1 是武器）
        :param strWayName:航线名称
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_AddPlanWay('{}',{},'{}')".format(self.strName, nType, strWayName))

    def is_show_plan_way(self, strWayNameOrID, bIsShow):
        """
        作者: 赵俊义
        日期：2020-3-10
        函数功能：为控制预设航线的显示或隐藏
        函数类型：推演函数
        :param strWayNameOrID: 预设航线名称或者GUID
        :param bIsShow: 是否显示
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_PlanWayIsShow('{}','{}',{})".format(self.strGuid, strWayNameOrID, bIsShow))

    def rename_plan_way(self, strWayNameOrID, strNewName):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：修改预设航线的名称
        函数类型：推演函数
        :param strWayNameOrID:预设航线名称或者GUID
        :param strNewName:新名称
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_RenamePlanWay('{}','{}','{}')".format(self.strGuid, strWayNameOrID, strNewName))

    def add_plan_way_point(self, strWayNameOrID, dWayPointLongitude, dWayPointLatitude):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：为预设航线添加航路点
        函数类型：推演函数
        :param strWayNameOrID: 预设航线名称或者GUID
        :param dWayPointLongitude:航路点经度
        :param dWayPointLatitude:航路点纬度
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_AddPlanWayPoint('{}','{}',{},{})".format(self.strGuid, strWayNameOrID, dWayPointLongitude,
                                                         dWayPointLatitude))

    def update_plan_way_point(self, strWayNameOrID, strWayPointID, table):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：修改航路点信息
        函数类型：推演函数
        :param strWayNameOrID: 预设航线的名称或者GUID
        :param strWayPointID: 航路点的GUID
        :param table: 航路点的信息 {NAME='12',LONGITUDE = 12.01,LATITUDE=56.32,ALTITUDE=1(为0-7的数值)，THROTTLE = 1(为0-5
                      的数值)，RADAR= 1(为0-2的数值),SONAR=1(为0-2的数值) ,OECM=1(为0-2的数值)},可根据需要自己构造
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_UpDataPlanWayPoint('{}','{}','{}',{})".format(self.strGuid, strWayNameOrID, strWayPointID, table))

    def remove_plan_way_point(self, strWayNameOrID, strWayPointID):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：预设航线删除航路点
        函数类型：推演函数
        :param strWayNameOrID: 预设航线名称或者GUID
        :param strWayPointID: 航路点的ID
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_RemovePlanWayPoint('{}','{}','{}')".format(self.strGuid, strWayNameOrID, strWayPointID))

    def remove_plan_way(self, strWayNameOrID):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：删除预设航线
        函数类型：推演函数
        :param strWayNameOrID: 预设航线名称或者GUID
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_RemovePlanWay('{}','{}')".format(self.strGuid, strWayNameOrID))

    def add_plan_way_to_mission(self, strMissionNameOrID, Type, strWayNameOrID):
        """
        函数功能：为任务分配预设航线
        函数类型：推演函数
        :param strMissionNameOrID: 任务名称或ID
        :param Type: 单元还是武器的航线
        :param strWayNameOrID: 航路名称或id
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_AddPlanWayToMission('{}',{},'{}')".
                                            format(strMissionNameOrID, Type, strWayNameOrID))

    def add_plan_way_to_target(self, strMissionNameOrId, strWayNameOrID, strTargetNameOrID):
        """
        函数功能：为目标分配预设航线
        函数类型：推演函数
        :param strMissionNameOrId: 任务的名称或GUID
        :param strWayNameOrID: 预设航线的名称或GUID
        :param strTargetNameOrID: 打击目标的名称或GUID
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_AddPlanWayToMissionTarget('{}','{}','{}')".format(strMissionNameOrId, strWayNameOrID,
                                                                  strTargetNameOrID))

    def edit_brief(self, briefing):
        """
        作者：赵俊义
        日期：2020-3-12
        函数功能：修改指定推演方的任务简报
        函数类型：编辑函数
        :param briefing:简报文字
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_EditBriefing('{}','{}')".format(self.strGuid, briefing))
