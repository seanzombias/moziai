#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################################
'''
此类函数仅供参考使用，最初版本，主动获取态势，被推送态势所代替，故此文件不在维护，请谨慎使用。
'''
########################################################################################
import socket
import re
import time
import MoziService.MoZiClass as MoZiClass
import grpc
import MoziService.GRPCServerBase_pb2 as GRPCServerBase_pb2
import MoziService.GRPCServerBase_pb2_grpc as GRPCServerBase_pb2_grpc


def dealData(value):
    # 值不为空时处理
    if value != '':
        if value[-2:-1] == ',':
            value = value[2:-3]
        else:
            value = value[2:-2]
        attr_list = value.split(',')
        unit = MoZiClass.Unit()
        for keyValue in attr_list:
            keyValue_list = keyValue.split('=')
            if len(keyValue_list) == 2:
                attr = keyValue_list[0].strip().replace('\\', '')
                attr_value = keyValue_list[1].strip().replace('\\', '')
                if attr == "guid":
                    unit.guid = attr_value
                elif attr == "name":
                    unit.name = attr_value
        return unit


class MoZi:
    '''MoZi'''

    def __init__(self, _HOST, _PORT):
        '''
        初始化方法，初始gRPC
        _HOST grpc 服务端IP
        _PORT 接口
        '''
        conn = grpc.insecure_channel(_HOST + ':' + str(_PORT))
        self.client = GRPCServerBase_pb2_grpc.gRPCStub(channel=conn)
        self.exect_flag = True
        self.command_string = ""
        self.command_num = 0

    def start_packing(self):
        self.exect_flag = False
        self.command_string = ""

    def end_exceting(self):
        self.exect_flag = True
        str_re = None
        if self.command_string != "":
            str_re = self.sendAndRecv(name_=self.command_string)
        self.command_string = ""
        self.command_num = 0
        return str_re

    def sendAndRecv(self, name_):
        '''
        gRPC发送和接收服务端消息方法
        '''
        if self.exect_flag:
            response = self.client.GrpcConnect(GRPCServerBase_pb2.GrpcRequest(name=name_))
            length = response.length
            if len(response.message) == length:
                return response.message
            else:
                return "数据错误"
        else:
            self.command_num += 1
            self.command_string += name_ + '\n'

    def sendAndRecvStream(self):
        print('Demonstrating UNARY_STREAM')
        # This block performs the same UNARY_STREAM interaction as above
        # while showing more advanced stream control features.
        replies = self.client.GrpcConnectStream(GRPCServerBase_pb2.GrpcRequest(name='none'))
        # print('replies length:%d' % len(replies))
        i = 0
        for resp in replies:
            if i < 5:
                i += 1
                print("\r\n\r\n")
                print(resp.message)
            else:
                print('sendAndRecvStream break')
                return
        print('sendAndRecvStream end')

        # 创建想定 complate

    def createNewScenario(self):
        return self.sendAndRecv("Hs_ScenEdit_CreateNewScenario(true)")

    # 添加方 complate
    def addSide(self, sideName):
        return self.sendAndRecv("HS_LUA_AddSide({side='%s'})" % (sideName))

    # 移除推演方
    def removeSide(self, side):
        return self.sendAndRecv("ScenEdit_RemoveSide({side='%s'})" % (side))

    # 设置对抗关系 complate
    def setSidePosture(self, sideAName, sideBName, relation):
        return self.sendAndRecv("ScenEdit_SetSidePosture('{}','{}','{}')".format(sideAName, sideBName, relation))

    '''
    删除任务
    side:推演方名称或guid
    mission：任务名称或guid
    '''

    def deleteMission(self, side, mission):
        deleteMission = "ReturnObj(ScenEdit_DeleteMission ('{}','{}'))".format(side, mission)
        return self.sendAndRecv(deleteMission)

    '''
    获取任务细节
    side:推演方名称或guid
    mission：任务名称或guid
    return Mission对象
    '''

    def getMission(self, side, mission):
        getMission = "ReturnObj(ScenEdit_GetMission ('{}', '{}'))".format(side, mission)
        result = self.sendAndRecv(getMission)
        mission = MoZiClass.Mission()
        if result[:7] == "mission":
            # 处理接收的数据
            result_split = result[9:-1].replace('\'', '')
            result_join = ""
            result_join = result_join.join([one for one in result_split.split('\n')])
            list = result_join.split(',')
            for keyValue in list:
                keyValue_list = keyValue.split('=')
                if len(keyValue_list) == 2:
                    attr = keyValue_list[0].strip()
                    value = keyValue_list[1].strip()
                    if attr == "name":
                        mission.name = value
                    elif attr == "side":
                        mission.side = value
                    elif attr == "type":
                        mission.type = value
                    elif attr == "subtype":
                        mission.subtype = value
                    elif attr == "guid":
                        mission.guid = value
                    elif attr == "isactive":
                        mission.isActive = bool(value)
                    elif attr == "starttime":
                        mission.startTime = value
                    elif attr == "endtime":
                        mission.endTime = value
                    elif attr == "SISH":
                        mission.SISIH = bool(value)
                    elif attr == "aar":
                        missionTanker = MoZiClass.MissionTanker()
                        result = self.sendAndRecv("print(ScenEdit_GetMission ('{}', '{}').aar)".format(side, mission))
                        result_list = result[1:-2].split(',')
                        for keyValue in result_list:
                            keyValue_list = keyValue.split('=')
                            if len(keyValue_list) == 2:
                                attr = keyValue_list[0].strip()
                                value = keyValue_list[1].strip()
                                if attr == "Doctrine_UseReplenishment":
                                    missionTanker.Doctrine_UseReplenishment = value
                                elif attr == "MaxReceiversInQueuePerTanker_Airborne":
                                    missionTanker.MaxReceiversInQueuePerTanker_Airborne = int(value)
                                elif attr == "TankerMaxDistance_Airborne":
                                    missionTanker.TankerMaxDistance_Airborne = value
                                elif attr == "TankerUsage":
                                    missionTanker.TankerUsage = value
                                elif attr == "FuelQtyToStartLookingForTanker_Airborne":
                                    missionTanker.FuelQtyToStartLookingForTanker_Airborne = int(value)
                        mission.aar = missionTanker
                    elif attr == "unitlist":
                        result = self.sendAndRecv("ScenEdit_GetMission ('{}', '{}').unitlist)".format(side, mission))
                        deal_accept = re.sub(r'\[\d\] =', '', result[1:-2].strip())
                        mission.unitList = deal_accept.split(',')
            code = "200"
        else:
            code = "500"
        return code, mission

    # 给单元分配任务
    def assignUnitListToMission(self, unitGuid, missionName):
        assignUnitListToMission = "ScenEdit_AssignUnitToMission('{}', '{}')".format(unitGuid, missionName)
        return self.sendAndRecv(assignUnitListToMission)

    '''
    将单元单元分配到任务
    unitGuid  单元guid
    missionName 单元名称
    escort   true为护航任务       
    '''

    def assignUnitListToMissionEscort(self, unitGuid, missionName, escort):
        assignUnitListToMission = "Hs_AssignUnitListToMission('{}', '{}',{})".format(unitGuid, missionName, escort)
        return self.sendAndRecv(assignUnitListToMission)

    # 单元取消分配任务
    def cancelAssignUnitListToMission(self, unitGuid):
        assignUnitListToMission = "ScenEdit_AssignUnitToMission('{}', 'none')".format(unitGuid)
        return self.sendAndRecv(assignUnitListToMission)

    '''
    单元自动探测到
    unitGuido：单元guid,isAutoDetectable：是否探测到 true?false complate
    '''

    def unitAutoDetectable(self, unitGuid, isAutoDetectable):
        unitAutoDetectable = "ScenEdit_SetUnit({guid='%s',autodetectable=%s})" % (unitGuid, isAutoDetectable)
        return self.sendAndRecv(unitAutoDetectable)

    '''
    设置单元信息
    unitGuido：单元guid,isAutoDetectable：是否探测到 true?false complate
    '''

    def scenEdit_SetUnit(self, table):
        unitAutoDetectable = "ScenEdit_SetUnit({})".format(table)
        return self.sendAndRecv(unitAutoDetectable)

    '''
    武器距离目标多少公里后暂停
    type:类型
    side：推演方
    targetGuid：目标guid
    weaponDBID:武器的BDID
    distance:距离（公里） complate
    '''

    def unitTargetSimBreakOff(self, Type, side, targetGuid, unitGuid, distance):
        weaponTargetSimBreakOff = "Hs_WeaponTargetSimBreakOff('%s', {SIDE = '%s', CONTACTGUID = '%s', ACTIVEUNITGUID = '%s', DISTANCE = %s})" % (
        Type, side, targetGuid, unitGuid, distance)
        return self.sendAndRecv(weaponTargetSimBreakOff)

    '''
    #创建和设置事件 eventname为事件名称 
    #eventTableMode为{mode='add',IsActive = false, IsRepeatable=true, Probability =100,IsShown = false} 
    # mode 是类型 添加删除修改之类的 isactive 是否激活  IsRepeatable 是否重复 Probability概率 IsShown是否显示
    返回乱执行是否成功 （string）
    '''

    def scenEditSetEvent(self, eventName, model):
        return self.sendAndRecv("ScenEdit_SetEvent ('%s',{mode='%s'})" % (eventName, model))

    '''
    #创建和设置触发器
    #triggerTableMode 为 {Description='航母被摧毁',mode='add',type= "unitdestroyed",TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"}}
    #Description 触发器名称 mode 操作类型同上 type触发器类型 类似有单元被摧毁 单元被毁伤之类的 
    #TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"} 是单元被毁伤和单元被摧毁的 TARGETSIDE为单元所在方  TARGETTYPE 为类型还有子类型参数
    返回乱执行是否成功 （string）
    '''

    def scenEditSetTrigger(self, table):
        return self.sendAndRecv("ScenEdit_SetTrigger ({})".format(table))

    '''
    创建动作和设置动作
    actionTableMode 为{Description='想定结束',mode='add',type='endscenario'}
    Description 动作名称 mode 操作类型 类似有添加删除 type为类型 有想定结束单元移动等
    返回乱执行是否成功 （string）
    '''

    def scenEditSetAction(self, table):
        return self.sendAndRecv(" ScenEdit_SetAction ({})".format(table))

    '''
    为事件添加触发器
    eventName 事件名称
    triggername 触发器名称
    mode 操作类型
    返回乱执行是否成功 （string）
    '''

    def scenEditSetEventTrigger(self, eventName, table):
        return self.sendAndRecv("ScenEdit_SetEventTrigger('{}', {})".format(eventName, table))

    '''
    为事件添加动作
    eventName 事件名称
    actionName 动作器名称
    mode 操作类型
    返回乱执行是否成功 （string）
    '''

    def scenEditSetEventAction(self, eventName, table):
        return self.sendAndRecv("ScenEdit_SetEventAction('{}',{})".format(eventName, table))

    '''
    设置单元传感器开关机
    sensorTableMode 为{guid='6c984ecb-c6d2-4a9d-82de-46dc106f6e3a',OECM=true}
    guid为单元guid oecm为类型 true false为开关量
    '''

    def setUnitSensorSwitch(self, sensorTableMode):
        return self.sendAndRecv("Hs_ScenEdit_SetUnitSensorSwitch({})".format(sensorTableMode))


    '''
    获取推演方信息
    side:推演方 
    '''

    def getSideInfo(self, side):
        d = dict()
        code = ""
        side_obj = Mozi.MoZiClass.Side()
        lua = "print(ReturnObj(VP_GetSide({side='%s'})))" % (side)
        result = self.sendAndRecv(lua)
        if result[:4] == "side":
            # 处理接收的数据
            result_split = result[6:-1].replace('\'', '')
            result_join = ""
            result_join = result_join.join([one for one in result_split.split('\n')])
            list = result_join.split(',')
            for keyValue in list:
                keyValue_list = keyValue.split('=')
                if keyValue_list.__len__() == 2:
                    d[keyValue_list[0].strip()] = keyValue_list[1].strip()
                    attr = keyValue_list[0].strip()
                    value = keyValue_list[1].strip()
                    if attr == "guid":
                        side_obj.guid = value
                    elif attr == "name":
                        side_obj.name = value
                    elif attr == "units":
                        units = self.sendAndRecv("print(VP_GetSide({side='%s'}).units)" % (side))
                        deal_accept = re.split(r'\[\d\] =', units[1:-2].strip())
                        activeUnit_map = map(dealData, deal_accept)
                        activeUnit_list = []
                        for unit in activeUnit_map:
                            if unit != None:
                                activeUnit_list.append(unit)
                        side_obj.units = activeUnit_list
                    elif attr == "contacts":
                        contacts = self.sendAndRecv("print(VP_GetSide({side='%s'}).contacts)" % (side))
                        deal_accept = re.split(r'\[\d\] =', contacts[1:-2].strip())
                        contacts_map = map(dealData, deal_accept)
                        contacts_list = []
                        for contact in contacts_map:
                            if contact != None:
                                contacts_list.append(contact)
                        side_obj.contacts = contacts_list
            code = "200"
        else:
            code = "500"
        return code, side_obj

    def setSimMode(self, simModel):
        '''
        推演模式设置
        :param simModel: 是否是推演模式 bool false 是编辑模式 true 是推演模式
        :return:
        '''
        return self.sendAndRecv("Hs_SetSimMode({})".format(simModel))

    #
    # gouaddSide
    #
    # 添加单元 complate
    def addUnit(self, side, type, name, dbid, latitude, longitude):
        code = ""
        # lua = "ReturnObj(ScenEdit_AddUnit({side = '" + side + "', type = '" + type + "', "+"name = '" + name + "', dbid = " + dbid + ", latitude = '" + latitude + "', longitude = '" + longitude + "'}))"
        # 发送lua脚本
        result = self.sendAndRecv(
            "ReturnObj(ScenEdit_AddUnit({side = '%s', type = '%s', name = '%s', dbid = %s, latitude = %s, longitude = %s}))" % (
            side, type, name, dbid, latitude, longitude))
        activeUnit = Mozi.MoZiClass.ActiveUnit()
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

        #
        # 添加单元 complate

    '''
    添加飞机T
    '''

    def addAircarft(self, side, Type, name, dbid, latitude, longitude, loadoutid, heading, altitude):
        code = ""
        lua = "HS_LUA_AddUnit({type='%s' , unitname='%s' ,side='%s', dbid=%s , latitude=%s,longitude=%s,altitude=%s, loadoutid=%s})"% (
        Type, name, side, dbid, latitude,  longitude, altitude, loadoutid)
        #lua = "print(ReturnObj(ScenEdit_AddUnit({type = '%s', name = '%s', loadoutid = %s, heading = %s, dbid = %s, side = '%s', Latitude=%s,Longitude=%s, altitude=%s)))" % (
        #Type, name, loadoutid, heading, dbid, side, latitude, longitude, altitude)
        # 发送lua脚本
        result = self.sendAndRecv(lua)
        #activeUnit = Mozi.MoZiClass.ActiveUnit()
        #if result[:4] == "unit":
            ## 处理接收的数据
            #result_split = result[6:-1].replace('\'', '')
            #result_join = ""
            #result_join = result_join.join([one for one in result_split.split('\n')])
            #list = result_join.split(',')
            #for keyValue in list:
                #keyValue_list = keyValue.split('=')
                #if len(keyValue_list) == 2:
                    #attr = keyValue_list[0].strip()
                    #value = keyValue_list[1].strip()
                    #if attr == "name":
                        #activeUnit.name = value
                    #elif attr == "side":
                        #activeUnit.side = value
                    #elif attr == "type":
                        #activeUnit.type = value
                    #elif attr == "subtype":
                        #activeUnit.subtype = value
                    #elif attr == "guid":
                        #activeUnit.guid = value
                    #elif attr == "proficiency":
                        #activeUnit.proficiency = value
                    #elif attr == "latitude":
                        #activeUnit.latitude = float(value)
                    #elif attr == "longitude":
                        #activeUnit.longitude = float(value)
                    #elif attr == "altitude":
                        #activeUnit.altitude = float(value)
                    #elif attr == "heading":
                        #activeUnit.heading = float(value)
                    #elif attr == "speed":
                        #activeUnit.speed = float(value)
                    #elif attr == "throttle":
                        #activeUnit.throttle = value
                    #elif attr == "autodetectable":
                        #activeUnit.autodetectable = bool(value)
                    #elif attr == "mounts":
                        #activeUnit.mounts = int(value)
                    #elif attr == "magazines":
                        #activeUnit.magazines = int(value)
                    #elif attr == "unitstate":
                        #activeUnit.unitstate = value
                    #elif attr == "fuelstate":
                        #activeUnit.fuelstate = value
                    #elif attr == "weaponstate":
                        #activeUnit.weaponstate = value
            #code = "200"
        #else:
            #code = "500"
        return result

    '''
     往机场，码头添加单元
    
    '''

    def addAirToFacility(self, type, name, side, dbid, loadoutid, baseUnitGuid):
        code = ""
        # lua = "ReturnObj(ScenEdit_AddUnit({side = 'type = '" + type + "', "
        # "name = '" + name + "', dbid = " + dbid + ", latitude = '" + latitude + "', longitude = '" + longitude + "'}))"
        # 发送lua脚本
        # ({type = "air", unitname = '歼-10 测试', side = "H方", dbid = 2478, loadoutid = 17464, base = 'dbc7db68-b9de-4c89-89f6-b87249459e1b'})
        # strss = "ScenEdit_AddUnit({type = '" + type + "', name = '" + name + "', dbid = " + str(dbid) + ", loadoutid = "+str(loadoutid)+", base = "+guid+"})"
        result = self.sendAndRecv(
            "ReturnObj(ScenEdit_AddUnit({ type = '%s', unitname = '%s',side='%s', dbid = %s, loadoutid = %s, base = '%s'}))" % (
            type, name, side, dbid, loadoutid, baseUnitGuid))
        activeUnit = Mozi.MoZiClass.ActiveUnit()
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

    '''
       获取单元信息
       unitType:单元类型  weapon,ship complate
    '''

    def getUnitInfo(self, unitType):
        unitInfo_list = []
        unitInfo_dict = dict()
        result = self.sendAndRecv("ReturnObj(Hs_GetUnitsInfo('{}'))".format(unitType))
        return result

        # if result != "":
        #     if result.find('@') >= 0:
        #         unit = result.split('@')
        #     else:
        #         unit = result
        # for unitInfos in unit:
        #     unitInfo = unitInfos.split('$')
        #     activeUnit = Mozi.MoZiClass.ActiveUnit()
        #     if len(unitInfo) > 3:
        #         activeUnit.latitude = unitInfo[0]
        #         activeUnit.longitude = unitInfo[1]
        #         activeUnit.guid = unitInfo[2]
        #         activeUnit.name = unitInfo[3]
        #         if len(unitInfo)> 5:
        #             unitInfo_dict['destroy'] = unitInfo[4]
        #             activeUnit.destroy = int(float(unitInfo[4]))
        #         unitInfo_list.append(activeUnit)
        # return unitInfo_list

    '''
    设置单元位置
    side:推演方
    unitGuid:单元guid
    longitude:经度
    latitude:纬度
    '''

    def setUnitPosition(self, side, unitGuid, longitude, latitude):
        return self.sendAndRecv("ScenEdit_SetUnit({side='%s', guid='%s', longitude=%s, latitude=%s})" % (
        side, unitGuid, longitude, latitude))

    '''
    设置单元名称
    side：推演方
    unitName:单元旧名称
    newUnitName：单元新名称
    '''

    def setUnitName(self, side, unitName, newUnitName):
        return self.sendAndRecv(
            "ScenEdit_SetUnit({side = '%s', unitname = '%s', newname = '%s'})" % (side, unitName, newUnitName))

    '''
    删除本方所有单元
    side：推演方name或者guid
    '''

    def deleteAllUnit(self, side):
        return self.sendAndRecv("Hs_DeleteAllUnits({})".format(side))

    '''
    删除单元
    unitGuid:单元guid
    '''

    def deleteUnit(self, unitGuid):
        return self.sendAndRecv("ScenEdit_DeleteUnit('{}')".format(unitGuid))

    # 想定的操作
    '''获取当前想定时间'''

    def getCurrentTime(self):
        return self.sendAndRecv("ReturnObj(ScenEdit_CurrentTime())")

    '''
    ScenEdit_AddZone (sideName, zoneType, table)添加禁航区或封锁区
    sideName string 阵营名称/GUID
    zoneType string 区域类型：0 = 禁航区, 1 = 封锁区
    table { table }
    {Description='%2', Area={"%3"}, MarkAs=%4} 
    Description, Isactive, Area { of RPs }, Affects { of UnitTypes }, MarkAs (exc only), Locked (non only) 
    '''

    def addZone(self, sideName, zoneType, table):
        res = self.sendAndRecv("ReturnObj(ScenEdit_AddZone('{}', {},{}))".format(sideName, zoneType, table))
        return res.split('\r')[1].split('\n')[1].split('=')[1].split(',')[0].replace(',', '').replace('\'', '').replace(
            ' ', '')

    '''
        设置手动攻击
        attackerId 攻击方单元guid
        contactId 目标guid
        AttackOptions 攻击选项
        mode string 瞄准模式：自动瞄准用"AutoTargeted"|"0"，手动瞄准用"ManualWeaponAlloc"|"1"
        mount number 攻击者的装具 DBID 
        weapon number 攻击者的武器 DBID
        qty number 分配数量
        table =  {mode=1,mount=2231,weapon=2868,qty=2}
    '''

    def manualAttackContact(self, attackerId, contactId, table):
        return self.sendAndRecv("ScenEdit_AttackContact ('{}', '{}', {})".format(attackerId, contactId, table))

    '''
    给某一方添加雷
    sideName 方的名称
    mineType 类型
    mineCount 数量
    area table类型 布雷区域
    '''

    def deployMine(self, sideName, mineType, mineCount, area):
        return self.sendAndRecv("Hs_DeployMine('{}','{}',{},{})".format(sideName, mineType, mineCount, area))

    '''
    投放被动声呐
    sidename 方的名称
    unitNameOrId 单元名称或id
    deepOrShallow 投放深浅
    '''

    def dropPassiveSonobuoy(self, sideName, unitNameOrId, deepOrShallow):
        return self.sendAndRecv("Hs_DropActiveSonobuoy('{}','{}',{})".format(sideName, unitNameOrId, deepOrShallow))

    '''
    设置当前天气条件
    temperature number 当前基线温度（摄氏度），随纬度变化。
    rainfall number 降水量，0-50.
    undercloud number 云层覆盖度， 0.0-1.0
    seastate number 当前海况， 0-9.
    '''

    def setWeather(self, temperature, rainfall, undercloud, seastate):
        return self.sendAndRecv(
            "ScenEdit_SetWeather({},{},{},{})".format(temperature, rainfall, undercloud, seastate))

    '''
    得到当前天气条件
    返回：table 天气参数数组
    '''

    def getWeather(self):
        return self.sendAndRecv("ScenEdit_GetWeather()")

    #    erte''
    '''
    设置已有特殊动作的属性 
    参数：action_info table类型 
    含有（
    SpecialAction 特殊动作选择子
    GUID string 该特殊动作的 GUID（只读）
    ActionNameOrID string 特殊动作的名称或 ID
    IsActive bool 如果动作对玩家可见
    IsRepeatable bool 如果玩家能多次使用该动作
    NewName string 若有，则是已给动作指定了的新名称
    Description string 基有，则是动作的新描述
    ）
    '''

    def setSpecialAction(self, action_info):
        return self.sendAndRecv("ScenEdit_SetSpecialAction ({})".format(action_info))

    '''
    开始想定 complate
     '''

    def simRun(self):
        simRun = "ReturnObj(Hs_SimRun(true))"
        return self.sendAndRecv(simRun)


    def endScenario(self):
        return self.sendAndRecv("ScenEdit_EndScenario()")

    '''
    加快推演速度
    speed:加快的参数 complate
    '''

    def setSimCompression(self, speed):
        simCompression = "ReturnObj(Hs_SetSimCompression({}))".format(speed)
        return self.sendAndRecv(simCompression)

    '''
    获取探测目标信息
    guid:探测目标的guid
    '''

    def getContact(self, guid):
        getContact = "ReturnObj(VP_GetContact({guid='%s'}))" % (guid)
        result = self.sendAndRecv(getContact)
        contact = Mozi.MoZiClass.Contact()
        code = 500
        if result[:7] == "contact":
            # 处理接收的数据
            result_split = result[9:-1].replace('\'', '')
            result_join = ""
            result_join = result_join.join([one for one in result_split.split('\n')])
            list = result_join.split(',')
            for keyValue in list:
                keyValue_list = keyValue.split('=')
                if len(keyValue_list) == 2:
                    attr = keyValue_list[0].strip()
                    value = keyValue_list[1].strip()
                    if attr == "name":
                        contact.name = value
                    elif attr == "type":
                        contact.type = value
                    elif attr == "guid":
                        contact.guid = value
            code = "200"
        else:
            code = "500"
        return code, contact

    '''
    获取推演方的探测目标
    side:推演方的guid
    '''

    def getContacts(self, side):
        getContact = "ReturnObj(VP_GetContact({guid='%s'}))" % (guid)
        result = self.sendAndRecv(getContact)
        return result

    '''
        contact = Mozi.MoZiClass.Contact()
        code = 500
        result = re.split(r'\[\d\] =',result[1:-2].strip())
        for info in result:
            if info != '' and info[:8].strip() == "contact":
                if info.strip()[-1:] == ',':
                    info = info[10:-4]
                else:
                    info = info[10:-2]
            info.split(',')
            '''

    '''
    引爆指定地点的弹头
    warheadid:弹头id
    latitude:纬度
    longitude：经度
    altitude:纬度
    '''

    def addExplosion(self, warheadid, latitude, longitude, altitude=0):
        addExplosion = "ReturnObj(ScenEdit_AddExplosion ({warheadid='%s',lat=%s,lon=%s, altitude=%s})))" % (
        warheadid, latitude, longitude, altitude)
        return self.sendAndRecv(addExplosion)

    '''添加参考点'''

    def addReferencePoint(self, side, pointName, lat, lon, highlighted):
        return self.sendAndRecv("ScenEdit_AddReferencePoint({side='%s', name='%s', lat=%s, lon=%s, highlighted=%s})" % (
        side, pointName, lat, lon, highlighted))

    '''
    得到某点海拔高度
    location:坐标 {latitude='9.0145',longitude='33.6594'}
    return 海拔（米）
    '''

    def getElevation(self, location):
        return self.sendAndRecv("ReturnObj(World_GetElevation ({}))".format(location))

    '''
        设置雷达开关机 
        type 受影响的类型（方，单元等）
        name 受影响类型名称（方的名称）
        EMCON 传感器类型
        state 状态
    '''

    def unitObeysEMCON(self, guid, state):
        return self.sendAndRecv("Hs_UnitObeysEMCON('{}', {})".format(guid, state))

    def SetEMCON(self, type, name, EMCON, state):
        return self.sendAndRecv("ScenEdit_SetEMCON('{}, '{}', '{}={}')".format(type, name, EMCON, state))

    '''
        设置雷达开关机 
        type 受影响的类型（方，单元等）
        name 受影响类型名称（方的名称）
        EMCON 传感器类型
        state 状态
    '''

    def setUnitSensorSwitch(self, guid, state):
        return self.sendAndRecv("Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s', rader = %s})" % (guid, state))

    '''设置自动接战
    def AttackContact(self,unitGuid, targetGuid):
        return self.sendAndRecv("ScenEdit_AttackContact('"+unitGuid+"','"+targetGuid+"',{MODE=0})")
    '''
    '''
    设置单元的攻击条令（自动攻击(FREE)、限制开火(TIGHT)、不能开火 (HOLD)、与上级一致(INHERITED)）
    '''

    def wcsfAContactTypesSUnit(self, sidedName, unitGuid, HoldTightFreeInherited):
        return self.sendAndRecv(
            "Hs_WCSFAContactTypesSUnit('{}','{}','{}')".format(sidedName, unitGuid, HoldTightFreeInherited))

    '''
    多个重用
    Python调用内部代码
    '''

    def pythonGetData(self, table):
        result = self.sendAndRecv("ReturnObj(print(Hs_PythonGetData({})))".format(table))
        try:
            result = re.split(r'\[\d\] =', result[1:-2].strip())
        except:
            result = None
        # for infos in result:
        #     if infos == "":
        #         continue
        #     print(infos)
        #     infos= re.split(r',', infos[1:-1].strip())
        #     for info in infos:
        #         info = re.split(r'=', info.strip())
        #         if (info[1].find("weapon") != -1):
        #            print(info[2])
        return result

    '''
    多个重用
    Python调用内部代码

    def PythonGetData(self, table):
        result = ""
        try:
            result= self.sendAndRecv("ReturnObj(print(Hs_PythonGetData({" + table + "})))")
            airfare = Mozi.MoZiClass.Airfare()
            print(result);
            result = re.split(r'\[\d\] =', result[1:-2].strip())
            airfareList = []
            for infos in result:
                if infos == "":
                    continue
                infos = re.split(r',', infos[1:-1].strip())
                for info in infos:
                    if (info.find("=") <= 0):
                        continue
                    info = re.split(r'=', info.strip())
                    if (info[0].find("Weapon") != -1):
                        airfare.weaponList.append(str(info[1]))
                    # 期望速度(希望单元接下来要达到的速度)
                    if (info[0].find("DesiredSpeed") != -1):
                        airfare.desiredSpeed = str(info[1])
                        continue
                    if (info[0].find("Fuel") != -1):
                        airfare.fuel = str(info[1])
                        continue
                    # 翻滚角
                    if (info[0].find("Roll") != -1):
                        airfare.roll = str(info[1])
                        continue
                    if (info[0].find("Longitude") != -1):
                        airfare.longitude = str(info[1])
                        continue
                    if (info[0].find("Latitude") != -1):
                        airfare.latitude = str(info[1])
                        continue
                    if (info[0].find("Radar") != -1):
                        airfare.radar = str(info[1])
                        continue
                    # 海高(不跟随地形)
                    if (info[0].find("Altitude_ASL") != -1):
                        airfare.altitude_ASL = str(info[1])
                        continue
                    if (info[0].find("MissionName") != -1):
                        airfare.missionName = str(info[1])
                        continue
                    # 俯仰角
                    if (info[0].find("Pitch") != -1):
                        airfare.pitch = str(info[1])
                        continue
                    if (info[0].find("GUID") != -1):
                        airfare.guid = str(info[1])
                        continue
                    # 真高(跟随地形)
                    if (info[0].find("Altitude_AGL") != -1):
                        airfare.altitude_AGL = str(info[1])
                        continue
                    if (info[0].find("AircraftAirOps") != -1):
                        airfare.aircraftAirOps = str(info[1])
                        continue
                    if (info[0].find("MissionGUID") != -1):
                        airfare.missionGuid = str(info[1])
                        continue
                    if (info[0].find("Speed") != -1):
                        airfare.speed = str(info[1])
                        continue
                    if (info[0].find("Damage") != -1):
                        airfare.damage = str(info[1])
                        continue
                    if (info[0].find("Heading") != -1):
                        airfare.heading = str(info[1])
                        continue
                airfareList.append(airfare)
        except:
            result = ""

        # for infos in result:
        #     if infos == "":
        #         continue
        #     print(infos)
        #     infos= re.split(r',', infos[1:-1].strip())
        #     for info in infos:
        #         info = re.split(r'=', info.strip())
        #         if (info[1].find("weapon") != -1):
        #            print(info[2])
        return airfareList
        
    '''

    '''
    从文件中运行脚本
    文件目录必须是“推演系统根目录/Lua”，否则不能打开。可以指定子目录如 'library/cklib.lua' ，其形式为
    "推演系统根目录/Lua/子目录”，也可用 ScenEdit_UseAttachment 作为附件间接加载。
    script
    '''

    def runScript(self, script):
        return self.sendAndRecv("ScenEdit_RunScript('{}')".format(script))

    '''
    根据键设置永久性键值的值
    kye 键
    value 值
    '''

    def setKeyValue(self, key, value):
        return self.sendAndRecv("ScenEdit_SetKeyValue('{}','{}')".format(key, value))

    '''
    设置已有单元的属性
    unit 单元 Table类型 可拓展 
    用法
    ScenEdit_SetUnit({side="United States", unitname="USS Test", lat = 5})
    ScenEdit_SetUnit({side="United States", unitname="USS Test", lat = 5})
    ScenEdit_SetUnit({side="United States", unitname="USS Test", lat = 5, lon = "N50.20.10"})
    ScenEdit_SetUnit({side="United States", unitname="USS Test", newname="USS Barack Obama"})
    ScenEdit_SetUnit({side="United States", unitname="USS Test", heading=0, HoldPosition=1,
     HoldFire=1,Proficiency="Ace",Autodetectable="yes"})

    '''

    def setAlreadyExistUnit(self, unit):
        return self.sendAndRecv("ScenEdit_SetUnit({})".format(unit))

    '''
    改变单元所属阵营
    ScenEdit_SetUnitSide (sidedesc)改变单元的阵营
    参数：
    sidedesc SideDescription 如何更改单元阵营的描述。编组会改变附属的单元。
    '''

    def setUnitSide(self, side, sideName, newSide):
        return self.sendAndRecv("ScenEdit_SetUnitSide({side='%s',name='%s',newside='%s'})" % (side, sideName, newSide))

    '''
    获取参考点信息
    sideName 方的名称
    area 区域 Table 类型 area={"RP-112","RP-113","RP-114","RP-115"}
    '''

    def getReferencePoints(self, sideName, area):
        result = self.sendAndRecv("print(ScenEdit_GetReferencePoints({side='%s', area=%s}))" % (sideName, area))
        code = 500
        if result[-2:-1] == ',':
            result = result[2:-3]
        else:
            result = result[2:-2]
        attr_list = result.split(',')
        referencePoint = Mozi.MoZiReferencePoint.ReferencePoint
        referencePoints = []
        for keyValue in attr_list:
            keyValue_list = keyValue.split('=')
            if len(keyValue_list) == 7:
                attr = keyValue_list[0].strip().replace('\\', '')
                attr_value = keyValue_list[1].strip().replace('\\', '')
                if attr == "locked ":
                    referencePoint.locked = attr_value
                elif attr == "name":
                    referencePoint.name = attr_value
                elif attr == "longitude":
                    referencePoint.longitude = attr_value
                elif attr == "latitude":
                    referencePoint.latitude = attr_value
                elif attr == "side":
                    referencePoint.side = attr_value
                elif attr == "guid":
                    referencePoint.guid = attr_value
                referencePoints.append(referencePoint)
        return referencePoints

    '''
    灭掉一个单元并触发单元事件
    lua参数是 unit
    python 参数是
    side 方名称
    unitname 单元名称或guid
    '''

    def killUnit(self, side, unitName):
        return self.sendAndRecv("ScenEdit_KillUnit(({side='%s',unitname='%s'})" % (side, unitName))

    '''
    设置单元燃油量
    strUnitNameOrID 单元 id 或 名称
    strRemainingFuel 油量
    '''

    def setFuelQty(self, unitNameOrID, remainingFuel):
        return self.sendAndRecv("Hs_SetFuelQty('{}','{}')".format(unitNameOrID, remainingFuel))

    '''
    设置留空时间
    unitNameOrId 单元
    hour 小时
    minute 分钟
    scond 秒
    '''

    def setAirborneTime(self, unitNameOrId, hour, minute, scond):
        return self.sendAndRecv("Hs_SetAirborneTime('{}',{},{},{})".format(unitNameOrId, hour, minute, scond))

    '''
    空中飞行器快速出动
    unitNameOrID 单元
    trueOrFalse 是否
    nComboBox 选中的comboBox的值
    备注：此函数涉及界面,慎用
    '''

    def quickTurnaround(self, unitNameOrID, trueOrFalse, nComboBox):
        return self.sendAndRecv("Hs_QuickTurnaround('{}','{}','{}')".format(unitNameOrID, trueOrFalse, nComboBox))

    '''
    编辑编组内高低速交替航行
    unitNameOrID 单元
    trueOrFalse 是否
    '''

    def setUnitSprintAndDrift(self, unitNameOrID, trueOrFalse):
        return self.sendAndRecv("Hs_SetUnitSprintAndDrift('{}',{})".format(unitNameOrID, trueOrFalse))

    '''
    将单元移除编组
    unitId 单元ID
    '''

    def removeUnitFromGroup(self, unitId):
        return self.sendAndRecv("Hs_RemoveUnitFromGroup('{}')".format(unitId))

    '''
    将单元添加到新建的组
    unitGuidList：单元的 guid，guid 之间用逗号分隔
    用法：
    Hs_ScenEdit_AddGroup({'613f00e1-4fd9-4715-a672-7ec5c22486cb','431337a9-987e-46b6-8cb8-2f92b9b80335','0bc31a3c-096a-4b8e-a
    23d-46f7ba3b06b3'})
    '''

    def scenEdit_AddGroup(self, unitGuidList):
        res = self.sendAndRecv("ReturnObj(Hs_ScenEdit_AddGroup({}))".format(unitGuidList))
        return res.split('\r\n')[5].split('=')[1].split(',')[0].replace(',', '').replace('\'', '').replace(' ', '')

    '''
    编组设置队形
    table 编组队形参数 {"2","686b0f99-533a-432c-9c24-e31e92d69afd","45","5",true}
    '''

    def groupFormation(self, table):
        return self.sendAndRecv("Hs_GroupFormation({})".format(table))

    '''
    添加货物
    unitId 单元ID
    cargoDBID 货物dbid    
    '''

    def addCargoToUnit(self, unitId, cargoDBID):
        return self.sendAndRecv("Hs_AddCargoToUnit('{}',{})".format(unitId, cargoDBID))

    '''
    删除货物
    unitId 单元ID
    cargoDBID 货物dbid  
    cargoDBID 货物dbid  
    '''

    def removeCargoToUnit(self, unitId, cargoDBID):
        return self.sendAndRecv("Hs_RemoveCargoToUnit('{}',{})".format(unitId, cargoDBID))

    '''
    添加禁航区
    sideNameOrID 方ID或name
    description 禁航区名称
    area 区域 area={"RP-112","RP-113","RP-114","RP-115"}
    '''

    def addOn_FlyZone(self, sideNameOrID, description, area):
        return self.sendAndRecv(
            "Hs_AddZone('%s', {Description = '%s', Area = %s})" % (sideNameOrID, description, area))




    '''
    得到阵营选项 对于单元上的组件使用。（可选）
    sideName 方的名称
    '''

    def getSideOptions(self, sideName):
        result = self.sendAndRecv(" ScenEdit_GetSideOptions({side='%s'})" % (sideName))
        sideOption = Mozi.MoZiSide.SideOption
        value = result[2:-2]
        text = value.split(",")
        for key in text:
            value = key.split("=")
            if value[0].strip() == "proficiency":
                sideOption.proficiency = value[1]
            if value[0].strip() == "awareness":
                sideOption.awareness = value[1]
            if value[0].strip() == "side":
                sideOption.side = value[1]
            if value[0].strip() == "guid":
                sideOption.guid = value[1]
        return sideOption



    '''
    更新单元的项目
    LUA_ScenEdit_UpdateUnit
    ScenEdit_UpdateUnit({guid='2cd64757-1b66-4609-ad56-df41bee652e5',mode='remove_sensor',dbid=3352,sensorId='871aea14-d9
    63-4052-a7fc-ed36e97bb732'})
    
    UpdateUnit 更新单元
    更新单元传感器或装具的选择子。
    列出所需的最小域，Unit 的其他域可以包括在内。
    guid string 单元唯一 ID
    mode string 要实施的功能(add_sensor,remove_sensor,add_mount,remove_mount,update_sensor_arc,update_ mount_arc)
    dbid number 要添加的项目 DBID 号
    sensorid string 要移除的某传感器的 guid（需要在 remove_sensor 模式下）
    mountid string 要移除的某挂架的 guid（需要在 remove_mount 模式下）
    arc_detect { Arc } 某传感器要探测的有效弧（默认重载）（可选）
    arc_track { Arc} 某传感器要跟踪/照射的有效弧（默认重载）（可选）
    arc_mount { Arc } 某挂架的有效弧（可选）

    '''





    '''
    删除单元
    LUA_ScenEdit_DeleteUnit
    ScenEdit_DeleteUnit({side="United States", unitname="USS Abcd"})
    '''

    def scenEdit_DeleteUnit(self, unit):
        return self.sendAndRecv("ScenEdit_DeleteUnit({})".format(unit))

    '''
    根据新值更新参考点
    LUA_ScenEdit_SetReferencePoint
    ScenEdit_SetReferencePoint({side="United States", name="Downed Pilot", lat=0.5, lon="N50.50.50", highlighted = true})
    descriptor = {side="United States", name="Downed Pilot", lat=0.5, lon="N50.50.50", highlighted = true}
    '''

    def scenEdit_SetReferencePoint(self, descriptor):
        return self.sendAndRecv("ScenEdit_SetReferencePoint({})".format(descriptor))

    '''
    将单元交给特定主持
    LUA_ScenEdit_HostUnitToParent(host_info)
    (单元会从任意地点移开，包括飞行或在其他地方被控。)    
    '''

    def scenEdit_HostUnitToParent(self, hostedUnitNameOrID, selectedHostNameOrID):
        return self.sendAndRecv("ScenEdit_SetReferencePoint({HostedUnitNameOrID='%s',SelectedHostNameOrID='%s'})" % (
        hostedUnitNameOrID, selectedHostNameOrID))

    '''
    获取给定阵营的分数
    scenEdit_GetScore  (side)
    ScenEdit_GetScore("PlayerSide")
    '''

    def scenEdit_GetScore(self, sideName):
        return self.sendAndRecv("ReturnObj(ScenEdit_GetScore('{}'))".format(sideName))

    '''
    设置指定阵营的分数
    LUA_ScenEdit_SetScore  (side, score, reason)
    ScenEdit_GetScore("PlayerSide", 20)
    '''

    def scenEdit_SetScore(self, sideName, score):
        return self.sendAndRecv("ReturnObj(ScenEdit_SetScore('{}',{}))".format(sideName, score))

    # 设置任务 complate
    def setMission(self, side, missionName, detailed):
        '''
        side 方
        missionName :任务名称或者guid
        detailed 任务细节        
        '''
        createMission = "ReturnObj(ScenEdit_SetMission('{}','{}',{}))".format(side, missionName, detailed)
        return self.sendAndRecv(createMission)

    '''
    ScenEdit_RefuelUnit (unitOptions)让单元加油
    用法
    ScenEdit_RefuelUnit({side="United States", unitname="USS Test"})
    ScenEdit_RefuelUnit({side="United States", unitname="USS Test", tanker="Hose #1"})
    ScenEdit_RefuelUnit({side="United States", unitname="USS Test", missions={"Pitstop"}})
    unitSelector UnitSelector 常规单元选择子
    tanker string 用名称指定的加油机（设定与单元同阵营）或 GUID
    missions { mission }任务名称或 GUID 的数组
    '''

    def scenEdit_RefuelUnit(self, unitOptions):
        return self.sendAndRecv("ScenEdit_RefuelUnit({})".format(unitOptions))

    '''
    从打击任务中移除目标
    LUA_ScenEdit_RemoveUnitAsTarget (AUNameOrIDOrTable, MissionNameOrID)
    用法：
    （一个或多个）
    auNameOrIDOrTable = {'d68fd5ce-d5c8-47e6-bc2b-f3ccb4c003b6','068cb024-c434-433f-9296-13359f4830a0'}
    missionNameOrID = '打击'
    '''

    def scenEdit_RemoveUnitAsTarget(self, auNameOrIDOrTable, missionNameOrID):
        return self.sendAndRecv("ScenEdit_RemoveUnitAsTarget('{}','{}')".format(auNameOrIDOrTable, missionNameOrID))

    '''
    设置编组
    LUA_ScenEdit_SetFormation
    table 编组类型、队形
    '''

    def SetFormation(self, table):
        return self.sendAndRecv("ReturnObj(ScenEdit_SetFormation({}))".format(table))

    '''
    得到两点间里程
    Tool_Range('804816c1-86cd-4baf-8eb9-995b2baff541','60e0257c-1cd8-44fb-929a-7aba635ee888' )
    Tool_Range
    jumpingOffPoint ,endPoint 可以是单元/接触 GUID 或经纬度坐标点
    '''

    def getToolRange(self, jumpingOffPoint, endPoint):
        return self.sendAndRecv("ReturnObj(Tool_Range('{}','{}'))".format(jumpingOffPoint, endPoint))

    '''
    得到两点间方向
    Tool_Bearing
    '''

    def getToolBearing(self, jumpingOffPoint, endPoint):
        return self.sendAndRecv("ReturnObj(Tool_Bearing('{}','{}'))".format(jumpingOffPoint, endPoint))

    '''Hs_GetMission'''
    '''
    删除方的所有单元
    Hs_DeleteAllUnits
    sideNameAndGuid 方的名称或guid
    '''

    def deleteAllUnits(self, sideNameAndGuid):
        return self.sendAndRecv("Hs_DeleteAllUnits({})".format(sideNameAndGuid))

    '''Hs_DropActiveSonobuoy'''
    '''
    Hs_DropSonobuoy 投放声纳，返回所投声纳单元 

    '''

    '''
    Hs_GetMissionUnAllocationUnit
    未分配任务的单元
    Hs_GetMissionUnAllocationUnit(string SideNameOrID, string MissionID)
    '''

    def getMissionUnAllocationUnit(self, sideNameOrID, missionID):
        result = self.sendAndRecv("Hs_GetMissionUnAllocationUnit('{}','{}')".format(sideNameOrID, missionID))
        results = re.split(r'\[\d\] =', result[1:-2].strip())
        guidList = []
        for result in results:
            guidList.append(result)
        return guidList

    '''
    Hs_ScenEdit_RemoveMagazineWeapon 删除弹药库武器
    Hs_ScenEdit_RemoveMagazineWeapon({GUID='%1',WPNREC_GUID='%2'})
    guid  单元
    wpnrec_Guid 武器guid
    '''

    def removeMagazineWeapon(self, guid, wpnrec_Guid):
        return self.sendAndRecv("Hs_ScenEdit_RemoveMagazineWeapon({GUID='%s',WPNREC_GUID='%s'})" % (guid, wpnrec_Guid))

    '''
    Hs_ScenEdit_SetMagazineWeaponCurrentLoad 设置弹药库武器数量
    Hs_ScenEdit_SetMagazineWeaponCurrentLoad({guid='%1',WPNREC_GUID='%2',currentLoad=%3})
    guid 单元
    WPNREC_GUID 武器guid
    currentLoad 当前挂载
    '''

    def setMagazineWeaponCurrentLoad(self, guid, WPNREC_GUID, currentLoad):
        return self.sendAndRecv(
            "Hs_ScenEdit_SetMagazineWeaponCurrentLoad({guid='%s',WPNREC_GUID='%s',currentLoad=%s})" % (
            guid, WPNREC_GUID, currentLoad))

    '''
    Hs_ScenEdit_SetMagazineState 设置弹药库状态
    guid 单元
    magazine_guid 弹药库guid
    state  状态
    '''

    def setMagazineState(self, guid, magazine_guid, state):
        return self.sendAndRecv(
            "Hs_ScenEdit_SetMagazineState({guid='%s', magazine_guid='%s',state='%s'}" % (guid, magazine_guid, state))

    '''
    Hs_ScenEdit_AllocateWeaponToTarget 为目标分配武器
    activeUnitGUID 单元GUID
    table 目标信息 {TargetLatitude=%2,TargetLongitude=%3} 或 { TargetGUID = '%2' }
    weaponDBID 武器DBID
    '''

    def allocateWeaponToTarget(self, activeUnitGUID, table, weaponDBID, num):
        return self.sendAndRecv(
            "Hs_ScenEdit_AllocateWeaponToTarget('{}',{},{},{})".format(activeUnitGUID, table, weaponDBID, num))

    '''
    Hs_ScenEdit_AllocateSalvoToTarget 为目标分配一次齐射
    activeUnitGUID 单元GUID
    table 目标信息 {TargetLatitude=%2,TargetLongitude=%3} 或 { TargetGUID = '%2' }
    weaponDBID 武器DBID
    '''

    def allocateSalvoToTarget(self, activeUnitGUID, table, weaponDBID):
        return self.sendAndRecv(
            "Hs_ScenEdit_AllocateSalvoToTarget('{}',{},{})".format(activeUnitGUID, table, weaponDBID))

    '''
    Hs_ScenEdit_AllocateAllWeaponsToTarget 为目标分配本类型所有武器
    activeUnitGUID 单元GUID
    table 目标信息 {TargetLatitude=%2,TargetLongitude=%3} 或 { TargetGUID = '%2' }
    weaponDBID 武器DBID
    '''

    def allocateAllWeaponsToTarget(self, activeUnitGUID, table, weaponDBID):
        return self.sendAndRecv(
            "Hs_ScenEdit_AllocateAllWeaponsToTarget('{}',{},{})".format(activeUnitGUID, table, weaponDBID))

    '''
    Hs_ScenEdit_RemoveWeapons_Target 取消单元分配的目标
    activeUnitGUID 单元GUID
    targetGUID 武器齐射GUID
    '''

    def removeWeapons_Target(self, activeUnitGUID, targetGUID):
        return self.sendAndRecv("ScenEdit_RemoveWeapons_Target('{}','{}')".format(activeUnitGUID, targetGUID))

    '''
    Hs_ScenEdit_SetSalvoTimeout 设置齐射间隔
    isSalvoTimeout 是否
    '''

    def setSalvoTimeout(self, isSalvoTimeout):
        return self.sendAndRecv("Hs_ScenEdit_SetSalvoTimeout({})".format(isSalvoTimeout))

    '''
    Hs_ScenEdit_InitializeAllocateWeapon 初始化分配武器
    attackUnitGUID 武器GUID
    table 目标信息 {TargetLatitude=%2,TargetLongitude=%3} 或 { TargetGUID = '%2' }
    '''

    def initializeAllocateWeapon(self, arrackUnitGUID, table):
        return self.sendAndRecv("Hs_ScenEdit_InitializeAllocateWeapon('{}',{})".format(arrackUnitGUID, table))

    '''
    Hs_ScenEdit_DisposeAllocateWeapon 处理分配武器
    guid 分配武器属性GUID
    '''

    def disposeAllocateWeapon(self, guid):
        return self.sendAndRecv("Hs_ScenEdit_DisposeAllocateWeapon('{}')".format(guid))

    '''
    Hs_SetWeaponWay 手动打击目标 绘制航线     
    activeUnitGUID  单元
    weaponSalvoGUID  齐射
    ContactID  目标
    fLongitude  经度
    fLatitude  纬度
    '''

    def setWeaponWay(self, activeUnitGUID, weaponSalvoGUID, ContactID, fLongitude, fLatitude):
        return self.sendAndRecv(
            "Hs_SetWeaponWay('{}','{}','{}',{},{})".format(activeUnitGUID, weaponSalvoGUID, ContactID, fLongitude,
                                                           fLatitude))




    '''
    Hs_ScenEdit_SetWeaponCurrentLoad 设置武器数量
    unitname   单元名称
    wpn_guid   武器guid
    number     数量
    '''

    def setWeaponCurrentLoad(self, unitname, wpn_guid, number):
        return self.sendAndRecv(
            "Hs_ScenEdit_SetWeaponCurrentLoad({unitname='%s',wpn_guid='%s',%s})" % (unitname, wpn_guid, number))

    '''
    Hs_AddWeaponToUnitMagazine 往弹药库内添加武器
    side 方
    guid 单元
    mag_guid 弹药库
    wpn_dbid 武器dbid
    number 数量
    '''

    def addWeaponToUnitMagazine(self, side, guid, mag_guid, wpn_dbid, number):
        return self.sendAndRecv(
            "Hs_AddWeaponToUnitMagazine({side='%s',guid='%s',mag_guid='%s',wpn_dbid=%s,number=%s})" % (
            side, guid, mag_guid, wpn_dbid, number))

    '''
    Hs_CloneETAC 克隆事件、触发器、条件、动作
    table {CLONETRIGGER = '", triggerGuid, "'} { CLONEEVENT = '", eventGuid, "' } 
    { CLONECONDITION = '", conditionGuid, "' }     { CLONEACTION = '", actionGuid, "' }
    '''

    def cloneETAC(self, table):
        return self.sendAndRecv("Hs_CloneETAC({})".format(table))

    '''
    Hs_OKReadyMission 确认出动准备(自动添加武器) 涉及界面

    '''

    '''
    HS_ReturnToBase 返航
    UnitNameOrID  要返航单元的GUID或者名称
    '''

    def returnToBas(self, unitNameOrID):
        return self.sendAndRecv("HS_ReturnToBase('{}')".format(unitNameOrID))

    '''
    Hs_WCSFAContactTypesSUnit 针对所有目标类型的武器控制状态-所选单元
    SideNameOrID 推演方
    UnitNameOrID 单元
    HoldTightFreeInherited  Hold--禁止开火 Tight--限制开火 Free-- 自由开火 Inherited--与上级一致
    '''

    def wcsfContactTypesSUnit(self, sideNameOrID, unitNameOrID, holdTightFreeInherited):
        return self.sendAndRecv(-
                                "Hs_WCSFAContactTypesSUnit('{}','{}','{}')".format(sideNameOrID, unitNameOrID,
                                                                                   holdTightFreeInherited))

    '''
    Hs_WCSFAContactTypesAllUnit 针对所有目标类型的武器控制状态-所有单元
    SideNameOrID  推演方名称或Id
    HoldTightFreeInherited  Hold--禁止开火 Tight--限制开火 Free-- 自由开火 Inherited--与上级一致
    '''

    def wcsfContactTypesAllUnit(self, sideNameOrID, holdTightFreeInherited):
        return self.sendAndRecv("Hs_WCSFAContactTypesAllUnit('{}','{}')".format(sideNameOrID, holdTightFreeInherited))

    '''
    Hs_UnitOperateCourse 依据位置删除添加航路点
    UnitNameOrID：单元名称 Or Id
    Location 第几个点
    Latitude 纬度
    Logitude 经度
    deleteOrUpdate 
        Delete 删除航路点，序号从 0 开始，经纬度必须有 double 值
        Update 添加航路点第 Location 之后添加（不能添加到最前面了）
    '''

    def unitOperateCourse(self, unitNameOrID, location, latitude, logitude, deleteOrUpdate):
        return self.sendAndRecv(
            "Hs_UnitOperateCourse('{}',{},{},{},'{}')".format(unitNameOrID, location, latitude, logitude,
                                                              deleteOrUpdate))


    '''
    Hs_LPCWAttackSUnit 攻击时忽略计划航线-针对所选单元
    sideNameOrID  推演方
    unitNameOrID  单元
    yesNoOrInherited  是否忽略
    '''

    def lpcwAttackSUnit(self, sideNameOrID, unitNameOrID, yesNoOrInherited):
        return self.sendAndRecv(
            "Hs_LPCWAttackSUnit('{}','{}','{}')".format(sideNameOrID, unitNameOrID, yesNoOrInherited))

    '''
    Hs_LPCWAttackAllUnit 攻击时忽略计划航线-针对所有单元
    SideNameOrID   推演方
    YesNoOrInherited 是否
    '''

    def lpcwAttackAllUnit(self, sideNameOrID, yesNoOrInherited):
        return self.sendAndRecv("Hs_LPCWAttackAllUnit('{}','{}')".format(sideNameOrID, yesNoOrInherited))

    '''
    Hs_SetMarkContact 感知目标设置
    SideNameOrGuid  推演方名称
    UnitGuid  单元的Guid
    ContactType 设置告知目标的类型 H-敌方 U-非友方 N-中立 F-友方
    '''

    def setMarkContact(self, sideNameOrGuid, unitGuid, contactType):
        return self.sendAndRecv("Hs_SetMarkContact('{}','{}','{}')".format(sideNameOrGuid, unitGuid, contactType))

    '''
    Hs_ContactDropTarget 放弃目标
    SideNameOrGuid 推演方
    ContactGuid 目标的GUID
    '''

    def contactDropTarget(self, sideNameOrGuid, contactGuid):
        return self.sendAndRecv("Hs_ContactDropTarget('{}','{}')".format(sideNameOrGuid, contactGuid))

    '''
    Hs_ContactRename 修改感知目标名称
    SideNameOrGuid 推演方
    ContactGuid 感知目标GUID
    NewName 感知目标的新名字
    '''

    def contactRename(self, SideNameOrGuid, ContactGuid, NewName):
        return self.sendAndRecv("Hs_ContactRename('{}','{}','{}')".format(SideNameOrGuid, ContactGuid, NewName))

    '''
    Hs_UnitDropTargetContact 单元放弃目标
    sideNameOrID  方
    unitNameOrID  单元
    contactID     目标
    '''

    def unitDropTargetContact(self, sideNameOrID, unitNameOrID, contactID):
        return self.sendAndRecv(
            "Hs_UnitDropTargetContact('{}','{}','{}')".format(sideNameOrID, unitNameOrID, contactID))

    '''
    Hs_UnitDropTargetAllContact 放弃所有目标 或者 脱离交战
    UnitNameOrID 单元名称或guid
    '''

    def unitDropTargetAllContact(self, unitNameOrID):
        return self.sendAndRecv("Hs_UnitDropTargetAllContact('{}')".format(unitNameOrID))

    '''
    Hs_ResetAllLossesExpenditures 重置所有战损消耗
    '''

    def resetAllLossesExpenditures(self):
        return self.sendAndRecv("Hs_ResetAllLossesExpenditures()")

    '''
    Hs_ResetAllSideScores 重置所有推演方分数
    '''

    def resetAllSideScores(self):
        return self.sendAndRecv("Hs_ResetAllSideScores()")


    '''
    Hs_WeaponUsageRules 维护客户端需要显示的武器规则集合
    EMCONSubjectType 条令的类型
    strDoctrine 条令的GUID
    nWeaponDBID 武器DBID    
    '''

    def weaponUsageRules(self, EMCONSubjectType, strDoctrine, nWeaponDBID):
        return self.sendAndRecv("Hs_WeaponUsageRules('{}','{}',{})".format(EMCONSubjectType, strDoctrine, nWeaponDBID))

    '''
    Hs_UnitObeysEMCON 作战单元遵循电磁管控规则
    strUnitNameOrID 单元
    bTrueOrFalse 是否
    '''

    def unitObeysEMCON(self, strUnitNameOrID, bTrueOrFalse):
        return self.sendAndRecv("Hs_UnitObeysEMCON('{}',{})".format(strUnitNameOrID, bTrueOrFalse))

    '''
    Hs_HoldPositonSelectedUnit 保持阵位-所选单元
    strUnitNameOrID 单元
    bTrueOrFalse 是否
    '''

    def holdPositonSelectedUnit(self, strUnitNameOrID, bTrueOrFalse):
        return self.sendAndRecv("Hs_HoldPositonSelectedUnit('{}',{})".format(strUnitNameOrID, bTrueOrFalse))

    '''
    Hs_HoldPositonAllUnit 保持阵位-所有单元
    strSideNameOrID 推演方
    bTrueOrFalse 是否
    '''

    def holdPositonAllUnit(self, strSideNameOrID, bTrueOrFalse):
        return self.sendAndRecv("Hs_HoldPositonAllUnit('{}',{})".format(strSideNameOrID, bTrueOrFalse))


    '''
    Hs_AddPlanWayPointRow 添加航路点
    strSideNameOrID 推演方 
    strWayNameOrID 预设航线的名称或者GUIS 
    table 航路点信息   {NAME='12',LONGITUDE = 12.01,LATITUDE=56.32,ALTITUDE=1(为0-7的数值)，THROTTLE = 1(为0-5的数值)，
    RADAR= 1(为0-2的数值),SONAR=1(为0-2的数值) ,OECM=1(为0-2的数值)}
    '''

    def addPlanWayPointRow(self, strSideNameOrID, strWayNameOrID, table):
        return self.sendAndRecv("Hs_AddPlanWayPointRow('{}','{}',{})".format(strSideNameOrID, strWayNameOrID, table))


    '''
    Hs_ScenEdit_AirRefuel 加油
    table 为
    {guid='单元GUID'} 自动选择加油机
    {guid='单元GUID',tanker_guid='选择加油机GUID'} 手动选择加油机
    {guid='单元GUID',mission_guid='任务GUID'} 从任务选择加油机
    '''

    def airRefuel(self, table):
        return self.sendAndRecv("Hs_ScenEdit_AirRefuel({})".format(table))


    '''
    Hs_CopyUnit 复制单元
    unitNameOrGuid 单元名称或者GUID
    longitude 经度
    latitude 纬度
    '''

    def copyUnit(self, unitNameOrGuid, longitude, latitude):
        return self.sendAndRecv("Hs_CopyUnit('{}',{},{})".format(unitNameOrGuid, longitude, latitude))

    '''
    Hs_DeployDippingSonar 部署吊放声呐
    unitNameOrGuid 吊放声呐单元名称或guid    
    '''

    def deployDippingSonar(self, unitNameOrGuid):
        return self.sendAndRecv("Hs_DeployDippingSonar('{}')".format(unitNameOrGuid))

    '''
    Hs_GetMissionAllocationUnit 获取任务内已分配的单元的guid
    SideNameOrID 方的名称或id
    MissionID 任务名称或ID
    '''

    def getMissionAllocationUnit(self, sideIdOrName, missionId):
        result = self.sendAndRecv("Hs_GetMissionAllocationUnit('{}','{}')".format(sideIdOrName, missionId))
        results = re.split(r'\[\d\] =', result[1:-2].strip())
        guidList = []
        for result in results:
            guidList.append(result)
        return guidList

    '''
    Hs_SetSideName 推演方重命名
    sideIdOrName 旧名称
    sideNewIdOrName 新名称
    '''

    def setNewSideNaem(self, sideIdOrName, sideNewIdOrName):
        return self.sendAndRecv("Hs_SetSideName('{}','{}')".format(sideIdOrName, sideNewIdOrName))

    '''
    设置单元的攻击条令（自动攻击(FREE)、限制开火(TIGHT)、不能开火 (HOLD)、与上级一致(INHERITED)）
    用法
    # 武器控制状态，对空
    # 2
    # ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_air = "0"}) 0 - -自由开火
    # 1 - -谨慎开火
    # 2 - -限制开火
    # 武器控制状态，对海
    # 2
    # ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_surface = "2"}) 0 - -自由开火
    # 1 - -谨慎开火
    # 2 - -限制开火
    # 武器控制状态，对潜
    # 2
    # ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_subsurface = "0"}) 0 - -自由开火
    # 1 - -谨慎开火
    # 2 - -限制开火
    # 武器控制状态，对地
    # 2
    # ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_land = "2"}) 0 - -自由开火
    # 1 - -谨慎开火
    # 2 - -限制开火
    '''

    def SetDoctrineAir(self, sideName, fireState):
        return self.sendAndRecv(
            "ScenEdit_SetDoctrine({side ='%s' }, {weapon_control_status_air ='%s}'})" % (sideName, fireState))

    '''
    设置多长时间暂停一次推演
    '''

    def hs_OneTimeStop(self, state, time):
        return self.sendAndRecv("Hs_OneTimeStop('{}',{})".format(state, time))

    def setNetxWayPoint(self, UnitNameAndGuid, TrunType, azimuth, timeLong):
        '''
        设置下一个航路点
        :param UnitNameAndGuid: 单元
        :param TrunType: 向左，向右转向
        :param azimuth: 转向角度
        :param timeLong: 距离（单元是距离。武器是时间，通过时间和速度计算距离）
        :return:
        '''
        if timeLong == "0":
            timeLong = 5000
        return self.sendAndRecv(
            "Hs_SetNetxWayPoint('{}', '{}', {},{})".format(UnitNameAndGuid, TrunType, azimuth, timeLong))

    def loadScenario(self, path, model):
        '''
        path 想定文件的相对路径（仅支持XML文件）
        model 模式 "Edit"想定编辑模式 "Play"想定推演模式
        '''
        return self.sendAndRecv("Hs_PythonLoadScenario('{}', '{}')".format(path, model))

    def scenEditLoadScenario(self, scenPath, isDeduce):
        '''
        scenPath 想定文件的相对路径（仅支持.scen文件）
        isDeduce 模式 "false"想定编辑模式 "true"想定推演模式
        '''
        return self.sendAndRecv("Hs_ScenEdit_LoadScenario('{}', {})".format(scenPath, isDeduce))

    '''
    获取想定是否加载
    '''

    def getScenarioIsLoad(self):
        return self.sendAndRecv("print(Hs_GetScenarioIsLoad())")

    '''
    设置触发器
    table 设置触发器的参数 
    用法 :ScenEdit_SetTrigger({mode='remove',type='UnitEntersArea',name='Any AOE entering hot zone'})
    ScenEdit_SetTrigger({mode='add',type='UnitEntersArea',name='Sagami exiting hot zone', targetfilter={SPECIFICUNIT='AOE
    421 Sagami'},area={'rp-1126','rp-1127','rp-1128','rp-1129'},exitarea=true})

    '''

    def scenEditSetTrigger(self, table):
        return self.sendAndRecv(" ScenEdit_SetTrigger({})".format(table))

    '''
    设置动作
    tbale 参数
    用法: ScenEdit_SetAction({mode='add',type='Points',name='sideA loses some ..', SideId='sidea', PointChange=-10})
    '''

    def scenEditSetAction(self, table):
        return self.sendAndRecv(" ScenEdit_SetAction({})".format(table))

    def scenEditSetEventAction(self, eventName, table):
        '''
        动作添加到事件
        用法：
        添加：ScenEdit_SetEventAction('test event', {mode='add', name='test action points'})
        替换：ScenEdit_SetEventAction('test event', {mode='replace', name='test action message', replacedby='test action points'})
        :param eventName: 事件名称
        :param table: 事件参数 具体参考用法或Lua
        :return:
        '''
        return self.sendAndRecv(" ScenEdit_SetAction('{}',{})".format(eventName, table))

    def scenEditSetEvent(self, eventName, model):
        '''
        创建事件
        用法：ScenEdit_SetEvent('my new event', {mode='add'})
        :param eventName:事件名称
        :param mode: 类型 (添加、修改)
        :return:
        用法： Hs_SetEvent("测试", {
        IsActive=true,//事件启用
        IsRepeatable=true,//事件可重复
        IsShown=true,//事件显示于输出区
        Probability=50,//发生概率
        Mode="add",
        Trigger={'GUID','GUID'},//触发器
        Action={'GUID','GUID'},//动作
        Condition={'GUID','GUID'}})//条件
        '''
        return self.sendAndRecv(" ScenEdit_SetEvent('%s', {mode='%s'})" % (eventName, model))

    def scenEditSetEventTrigger(self, eventName, table):
        '''
        触发器添加到事件
        用法：
        添加：ScenEdit_SetEventTrigger('test event', {mode='add', name='test action points'})
        替换：ScenEdit_SetEventTrigger('test event', {mode='replace', name='test action message', replacedby='test action points'})
        :param eventName: 事件名称
        :param table: 事件参数 具体参考用法或Lua
        :return:
        '''
        return self.sendAndRecv("ScenEdit_SetEventTrigger('{}',{})".format(eventName, table))

