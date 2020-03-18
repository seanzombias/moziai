# -*- coding:utf-8 -*-
##########################################################################################################
# File name : activeunit.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CActiveUnit:
    """
    活动单元（飞机、地面兵力及设施、水面舰艇、潜艇、卫星、武器，不包含目标、传感器等）
    """

    def __init__(self):
        self.side_name = ''
        self.mozi_server = None
        # 活动单元传感器列表
        self.sensors = {}
        # 活动单元挂架
        self.mounts = {}
        # 活动单元弹药库
        self.magazines = {}
        # 航路点
        self.way_points = {}
        # 对象类名
        self.ClassName = ""
        # 名称
        self.strName = ""
        # Guid
        self.strGuid = ""
        # 地理高度
        self.fAltitude_AGL = 0.0
        # 海拔高度
        self.iAltitude_ASL = 0
        # 所在推演方ID
        self.m_Side = ""
        # 单元类别
        self.strUnitClass = ""
        # 当前纬度
        self.dLatitude = 0.0
        # 当前经度
        self.dLongitude = 0.0
        # 当前朝向
        self.fCurrentHeading = 0.0
        # 当前速度
        self.fCurrentSpeed = 0.0
        # 当前海拔高度
        self.fCurrentAltitude_ASL = 0.0
        # 倾斜角
        self.fPitch = 0.0
        # 翻转角
        self.fRoll = 0.0
        # 获取期望速度
        self.fDesiredSpeed = 0.0
        # 获取最大油门
        self.m_MaxThrottle = 0
        # 最大速度
        self.fMaxSpeed = 0.0
        # 最小速度
        self.fMinSpeed = 0.0
        # 当前高度
        self.fCurrentAlt = 0.0
        # 期望高度
        self.fDesiredAlt = 0.0
        # 最大高度
        self.fMaxAltitude = 0.0
        # 最小高度
        self.fMinAltitude = 0.0
        # 军标ID
        self.strIconType = ""
        # 普通军标
        self.strCommonIcon = ""
        # 数据库ID
        self.iDBID = 0
        # 是否可操作
        self.bIsOperating = False
        # 编组ID
        self.m_ParentGroup = ""
        # 停靠的设施的ID(关系)
        self.m_DockedUnits = ""
        # 单元的停靠设施(部件)
        self.m_DockFacilitiesComponent = ""
        # 停靠的飞机的ID(关系)
        self.m_DockAircrafts = ""
        # 单元的航空设施(部件)
        self.m_AirFacilitiesComponent = ""
        # 单元的通信设备及数据链(部件)
        self.m_CommDevices = ""
        # 单元的引擎(部件)
        self.m_Engines = ""
        # 传感器，需要构建对象类,所以只传ID
        self.m_Sensors = ""
        # 挂架
        self.m_Mounts = ""
        # 毁伤状态
        self.strDamageState = ""
        # 失火
        self.iFireIntensityLevel = 0
        # 进水
        self.iFloodingIntensityLevel = 0
        # 分配的任务
        self.m_AssignedMission = ""
        # 作战条令
        self.m_Doctrine = None
        # 系统右栏->对象信息->作战单元武器
        self.m_UnitWeapons = ""
        # 路径点
        self.m_WayPoints = ""
        # 训练水平
        self.m_ProficiencyLevel = 0
        # 是否是护卫角色
        self.bIsEscortRole = False
        # 当前油门
        self.m_CurrentThrottle = 0
        # 通讯设备是否断开
        self.bIsCommsOnLine = False
        self.bIsIsolatedPOVObject = False
        # 地形跟随
        self.bTerrainFollowing = False
        self.bIsRegroupNeeded = False
        # 保持阵位
        self.bHoldPosition = False
        # 是否可自动探测
        self.bAutoDetectable = False
        # 当前货物
        self.m_Cargo = ""
        # 燃油百分比，作战单元燃油栏第一个进度条的值
        self.dFuelPercentage = 0.0
        # 获取AI对象的目标集合# 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        self.m_AITargets = ""
        # 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        self.m_AITargetsCanFiretheTargetByWCSAndWeaponQty = ""
        # 获取单元的通讯链集合
        self.m_CommLink = ""
        # 获取传感器
        self.m_NoneMCMSensors = ""
        # 获取显示"干扰"或"被干扰"
        self.iDisturbState = 0
        # 单元所属多个任务数量
        self.iMultipleMissionCount = 0
        # 单元所属多个任务guid拼接
        self.m_MultipleMissionGUIDs = ""
        # 是否遵守电磁管控
        self.bObeysEMCON = False
        # 武器预设的打击航线
        self.m_strContactWeaponWayGuid = ""
        # 停靠参数是否包含码头
        self.bDockingOpsHasPier = False
        # 弹药库
        self.m_Magazines = ""
        # 被摧毁
        self.dPBComponentsDestroyedWidth = 0.0
        # 轻度
        self.dPBComponentsLightDamageWidth = 0.0
        # 中度
        self.dPBComponentsMediumDamageWidth = 0.0
        # 重度
        self.dPBComponentsHeavyDamageWidth = 0.0
        # 正常
        self.dPBComponentsOKWidth = 0.0
        # 配属基地
        self.m_HostActiveUnit = ""
        # 状态
        self.strActiveUnitStatus = ""

        # 精简
        self.doctrine = None

    # def get_information(self):
    # """
    # 获取本单元详细信息
    #:return:dict, 例：{"unitstate":"Unassigned","heading":0.0,"type":"Facility","fuelstate":"None","longitude":49.878556388303,"latitude":40.532345887538,
    # "altitude":18.0,"subtype":"3002","autodetectable":False,"side":"蓝方","proficiency":"Regular","name":"地空导弹营(SA-2f)","speed":0.0,
    # "weaponstate":"None","guid":"65e4a622-909e-47be-8b57-f49f5e580271"}
    # """
    # lua_arg = cf.get_lua_table2json() + cf.get_lua_unit_str() % self.strGuid
    # return self.get_server_json_data(lua_arg)

    def get_target_by_info(self):
        pass

    def get_mounts_info(self):
        """
        获取挂架信息
        :return:
        """
        info = []
        for guid, mount_obj in self.mounts.items():
            info.append({
                "mount_guid": guid,
                "mount_dbid": mount_obj.iDBID,
                "mount_name": mount_obj.strName
            })
        return info

    def scenedit_set_unit(self, guid, longitude, latitude, mozi_server):
        '''
        设置单元航路点
        :param strGuid:
        :param longitude:
        :param latitude:
        :param mozi_server:
        :return:
        '''
        lua_str = "ScenEdit_SetUnit({side= '红方', guid='%s', course={ { Description = ' ', TypeOf = 'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
            guid, longitude, latitude)
        mozi_server.sendAndRecv(lua_str)

    def plotted_course(self, course_list):
        """
        规划单元航线
        :param course_list: list, [(lat, lon)]
        例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        if not course_list:
            return
        course_para = "{ longitude=" + str(course_list[0][1]) + ",latitude=" + str(course_list[0][0]) + "}"
        for point in course_list[1:]:
            latitude = point[0]
            longitude = point[1]
            course_para = course_para + ",{ longitude=" + str(longitude) + ",latitude=" + str(latitude) + "}"
        cmd_str = "HS_LUA_SetUnit({side='" + self.m_Side + "', guid='" + self.strGuid + "', course={" + course_para + "}})"
        return self.mozi_server.sendAndRecv(cmd_str)

    def get_valid_weapons(self):
        """
        此函数需要重写
        获取有效的可用武器
        :return: dict
        """
        # valid_weapons = {}
        # for mount_ in self.mounts.values():
        #     if (mount_.strWeaponFireState == "就绪" or "秒" in mount_.strWeaponFireState) \
        #             and mount_.m_ComponentStatus <= 1:
        #         mount_weapons = cf.parse_weapons_record(mount_obj.m_LoadRatio)
        #         for w_record in mount_weapons:
        #             w_dbid = w_record['wpn_dbid']
        #             if db.check_weapon_attack(w_dbid):
        #                 if w_dbid in info:
        #                     valid_weapons[w_dbid] += w_record['wpn_current']
        #                 else:
        #                     valid_weapons[w_dbid] = w_record['wpn_current']
        # return valid_weapons
        pass

    def get_way_points_info(self):
        '''
        获取本单元航路点信息
        retutn : list
        '''
        way_points = []
        if self.m_WayPoints != "":
            guid_list = self.m_WayPoints.split("@")
            for guid in guid_list:
                point_obj = self.way_points[guid]
                way_points.append({
                    "latitude": point_obj.dLatitude,
                    "longitude": point_obj.dLongitude,
                    "Description": point_obj.strWayPointDescription
                })
        return way_points

    def get_sensors_info(self):
        '''
        获取本单元传感器信息
        retutn : list
        '''
        sensors = []
        # 遍历传感器，一个一个查找
        for guid, sensor_obj in self.sensors.items():
            sensors.append({
                "sensor_isactive": sensor_obj.bActive,
                "sensor_status": sensor_obj.strWorkStatus,
                "sensor_maxrange": sensor_obj.fMaxRange,
                "sensor_dbid": sensor_obj.iDBID,
                "sensor_role": 0 if sensor_obj.m_SensorRole == "" else int(sensor_obj.m_SensorRole),
                "sensor_name": sensor_obj.strName,
                "sensor_type": sensor_obj.m_SensorType,
                "sensor_guid": guid
            })
        return sensors

    def get_ai_targets(self):
        '''
        获取活动单元的Ai目标集合
        return : list
        '''
        if self.m_AITargets:
            return self.m_AITargets.split('@')
        else:
            return []

    def delete_sub_object(self):
        del_list = list(self.sensors.keys())
        del_list.extend(self.mounts.keys())
        del_list.extend(self.magazines.keys())
        del_list.extend(self.way_points.keys())

        if self.doctrine is not None:
            del_list.append(self.doctrine.guid)
            del self.doctrine

        for guid, point in self.way_points.items():
            del_list.extend(point.delete_sub_object())
        for guid, mount_instance in self.mounts.items():
            del_list.extend(mount_instance.delete_sub_object())

        del self.sensors
        del self.mounts
        del self.magazines
        del self.way_points
        return del_list

    # ---------------------传感器部面板设置------------------------
    def unit_obeys_EMCON(self, is_obey):
        """
        单元传感器面板， 单元是否遵循电磁管控条令
        :param is_obey: bool(True 或 False)
        :return: void
        """
        state = str(is_obey).lower()
        return self.mozi_server.sendAndRecv("Hs_UnitObeysEMCON('{}', {})".format(self.strGuid, state))

    # def set_unit_sensor_switch(self, switch_on):
    # """
    # 单元传感器面板， 单元雷达开关机
    #:param switch_on: bool(True 或 False)
    #:return: void
    # """
    # set_str = str(switch_on).lower()
    # return  self.mozi_server.sendAndRecv("Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s', rader = %s})"%(self.strGuid, set_str))

    # ---------------------选择单元，鼠标右键操作------------------------
    def get_valid_weapons_attack_target(self, contact_guid):
        """
        获取当前可打击目标的可用武器
        开火检测
        :param contact_guid:
        :return: dict
        """
        manual_info = self.attack_manual_info(contact_guid)
        if len(manual_info) == 1 and 'guid不存在' in list(manual_info.values())[0]:
            return {}
        else:
            valid_weapons = {}
            for w_info in manual_info:
                if w_info['IsFire'] == 1:
                    valid_weapons[w_info['dBID']] = w_info['number']
            return valid_weapons

    def manual_attack_contact(self, contact_guid, mount_num, weapon_num, qty_num):
        """
        函数功能：攻击一个接触作为武器部署后自动瞄准或手动瞄准的方式
        函数类型：推演函数
        :param contact_id: 目标guid
        :param mount_num: 攻击者的装具 DBID
        :param weapon_num: 攻击者的武器 DBID
        :param qty_num: 分配数量
            table =  {mode=1,mount=2231,weapon=2868,qty=2}
        :return:
        """
        lua_scrpt = "ScenEdit_AttackContact ('{}', '{}', {})".format(
            self.strGuid, contact_guid,
            "{mode=1,mount=" + str(mount_num) + ",weapon=" + str(weapon_num) + ",qty=" + str(qty_num) + "}")
        self.mozi_server.sendAndRecv(lua_scrpt)

    def all_ocate_weapon_to_target(self, target, weaponDBID, weapon_count):
        """
        单元手动攻击(打击情报目标), 或者纯方位攻击(打击一个位置)
        :param target: 情报目标guid 或  坐标-tuple(lat, lon)
        :param weaponDBID: int, 武器型号数据库id
        :param weapon_count: int, 分配数量
        :return:
        """
        if type(target) == str:
            table = "{TargetGUID ='" + target + "'}"
        elif type(target) == tuple:
            table = "{TargetLatitude =" + str(target[0]) + ", TargetLongitude = " + str(target[1]) + "}"
        else:
            raise Exception("target 参数错误")
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_AllocateWeaponToTarget('{}',{},{},{})".format(
            self.strGuid, table, str(weaponDBID), str(weapon_count)))

    def all_ocate_salvo_to_target(self, target, weaponDBID):
        """
        单元手动分配一次齐射攻击(打击情报目标), 或者纯方位攻击(打击一个位置)
        :param target:情报目标guid，例："fruo-fs24-2424jj" 或  坐标-tuple(lat, lon)，例:(40.90,30.0)
        :param weaponDBID:武器型号数据库id
        :return:
        """
        if type(target) == str:
            table = "{TargetGUID ='" + target + "'}"
        elif type(target) == tuple:
            table = "{TargetLatitude =" + str(target[0]) + ", TargetLongitude = " + str(target[1]) + "}"
        else:
            raise Exception("target 参数错误")
        lua_scrpt = "Hs_ScenEdit_AllocateSalvoToTarget('{}',{},{})".format(self.strGuid, table, str(weaponDBID))
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def unit_auto_detectable(self, isAutoDetectable):
        '''
        单元自动探测到
        isAutoDetectable：是否探测到 true?false complate
        '''
        unitAutoDetectable = "ScenEdit_SetUnit({guid='%s',autodetectable=%s})" % (self.strGuid, isAutoDetectable)
        return self.mozi_server.sendAndRecv(unitAutoDetectable)

    def unit_drop_target_contact(self, contact_guid):
        """
        函数功能：放弃对指定目标进行攻击。 
        参数说明： 
        1）ContactID：字符串。目标 GUID
        """
        lua_scrpt = "Hs_UnitDropTargetContact('{}','{}','{}')".format(self.strName, self.strGuid, contact_guid)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def unit_drop_target_all_contact(self):
        """
        函数功能：放弃对所有目标进行攻击，脱离交战状态。 
        参数说明： 
        1）UnitNameOrID：字符串。单元名称或 GUID
        """
        return self.mozi_server.sendAndRecv("Hs_UnitDropTargetAllContact('{}')".format(self.strGuid))

    def ignore_plotted_courseWhenAttacking(self, enum_ignore_plotted):
        """
        在攻击时是否忽略计划航线，是、否、与上级一致
        :param enum_ignore_plotted:IgnorePlottedCourseWhenAttacking
        :return:
        """
        if enum_ignore_plotted.value == 999:
            para_str = 'Inherited'
        else:
            para_str = enum_ignore_plotted
        return self.mozi_server.sendAndRecv(
            "Hs_LPCWAttackSUnit('{}','{}','{}')".format(self.strName, self.strGuid, para_str))

    def terrain_follow(self, is_fellow):
        """
        设置当前单元（飞机）的飞行高度跟随地形
        :param is_fellow:bool, True:跟随地形
        :return:
        """
        set_str = str(is_fellow).lower()
        lua_scrpt = "ScenEdit_SetUnit(guid='%s',  TEEEAINFOLLOWING = %s})" % (str(self.strGuid), set_str)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def delete_coursed_point(self, point_index=None, clear=False):
        """
        单元删除航路点
        :param point_index: list:删除多个航路点 [0, 1], or int：删除一个航路点，
        :param clear: bool, True:清空航路点
        :return:
        """
        lua_scrpt = ""
        if clear:
            if self.m_WayPoints != "":
                point_count = len(self.m_WayPoints.split("@"))
                for point in range(point_count - 1, -1, -1):
                    lua_scrpt += ('Hs_UnitOperateCourse("%s",%d,0.0,0.0,"Delete")' % (self.strGuid, point))
        else:
            if isinstance(point_index, list):
                if len(point_index) > 1 and point_index[-1] > point_index[0]:
                    point_index.reverse()
                for point in point_index:
                    lua_scrpt += ('Hs_UnitOperateCourse("%s",%d,0.0,0.0,"Delete")' % (self.strGuid, point))
            elif isinstance(point_index, int):
                lua_scrpt = "Hs_UnitOperateCourse('%s',%d,0.0,0.0,'Delete')" % (self.strGuid, point_index)
            #     lua_scrpt = "Hs_UnitOperateCourse('0ec5c4b7-7304-422a-a857-0d8f54f5fb5',0,0.0,0.0,'Delete')"
            # if lua_scrpt != "":
            #     lua_scrpt = "Hs_UnitOperateCourse('0ec5c4b7-7304-422a-a857-0d8f54f5fb5',0,0.0,0.0,'Delete')"
            return self.mozi_server.sendAndRecv(lua_scrpt)

    def return_to_base(self):
        """
        单元返航
        :return:
        """
        return self.mozi_server.sendAndRecv("HS_ReturnToBase('{}')".format(self.strGuid))

    def select_new_base(self, base_guid):
        """
        单元选择新基地/新港口
        :param base_guid: 新基地的guid
        :return:
        """
        lua_scrpt = "ScenEdit_SetUnit({unitname='%s',base='%s'})" % (self.strGuid, base_guid)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    # def refuel(self, refule_unit_guid):
    # """
    # 加油/补给
    #:param refule_unit_guid: 加油机或补给船的guid, 如果为空，则自动选择
    #:return:
    # """
    # pass

    def hold_positon_selected_unit(self, is_hold):
        """
        函数功能：命令面上指定单元设置是否保持阵位。
        参数说明：
        1）is_hold：布尔值。状态标识符（true：是，false：否）
        """
        bTrueOrFalse = str(is_hold).lower()
        return self.mozi_server.sendAndRecv("Hs_HoldPositonSelectedUnit('{}',{})".format(self.strGuid, bTrueOrFalse))

    # def quick_turnaround(self):
    # """
    # 快速出动
    #:return:
    # """
    # pass

    def assign_unitList_to_mission(self, mission_name):
        """
        分配加入到任务中
        :param mission_name: str, 任务名称
        """
        lua_scrpt = "ScenEdit_AssignUnitToMission('{}', '{}')".format(self.strGuid, mission_name)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def assign_unitList_to_missionEscort(self, mission_name):
        """
        将单元分配为某打击任务的护航任务
        :param mission_name: 任务名称
        :return: table 存放单元的名称或者GUID
        """
        lua_scrpt = "Hs_AssignUnitListToMission('{}', '{}',{})".format(self.strGuid, mission_name, 'true')
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def cancel_assign_unitList_to_mission(self):
        """
        将单元取消分配任务
        :return:
        """
        lua_scrpt = "ScenEdit_AssignUnitToMission('{}', 'none')".format(self.strGuid)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def set_fuelQty(self, remainingFuel):
        '''
        设置单元燃油量
        strRemainingFuel 油量
        '''
        return self.mozi_server.sendAndRecv("Hs_SetFuelQty('{}','{}')".format(self.strGuid, remainingFuel))

    def set_unit_heading(self, heading):
        '''
        设置朝向
        heading 朝向
        
        exampl
        set_unit_heading('016b72ba-2ab2-464a-a340-3cfbfb133ed1',30):
        '''

        lua_scrpt = "ScenEdit_SetUnit({guid =' %s' ,heading = %s})" % (self.strGuid, heading)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def attack_auto(self, contact_guid):
        """
        自动攻击目标
        :param contact_guid: 目标guid
        :return:
        """
        return self.mozi_server.autoAttackContact(self.strGuid, contact_guid)

    # def attack_manual_info(self, contact_guid):
    # """
    # 手动攻击信息
    #:param contact_guid: str, 目标guid
    #:return:
    # """
    # lua = cf.get_lua_common_str()
    # attack_info = 'message_info = Hs_PythonGetData({VERDICTWEAPONHIT=1,UNITGUID="%s",TARGETGUID="%s"})\n' % (self.strGuid, contact_guid)
    # attack_info += "json = table_to_json(message_info)\nprint(json)"
    # lua += attack_info
    # manual_info = self.get_server_json_data(lua)
    # weapon={}
    # for i in manual_info:
    # if i['message']=='OK'and i['number']>0:
    # weapon[i['dBID']]=i['number']

    # return weapon

    def set_desired_speed(self, desired_speed):
        """
        设置单元的期望速度
        :param desired_speed: float, 千米/小时
        :return: 所操作单元的完整描述子
        """
        if isinstance(desired_speed, int) or isinstance(desired_speed, float):
            lua_scrpt = "ScenEdit_SetUnit({guid='" + str(self.strGuid) + "', manualSpeed='" + str(
                desired_speed / 1.852) + "'})"
            return self.mozi_server.sendAndRecv(lua_scrpt)
        else:
            message = ""
            pass

    def set_throttle(self, enum_throttle):
        """
        设置单元油门
        :param enum_throttle: Throttle, 油门选择
        :return:
        """
        lua_scrpt = "ScenEdit_SetUnit({GUID='%s', THROTTLEPRESET='%s'})" % (self.strGuid, enum_throttle)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    # def set_throttle(self, enum_throttle):
    # """
    # 设置单元油门
    #:param enum_throttle: Throttle, 油门选择
    #:return:
    # """
    # throttle_str = ""
    # if enum_throttle == Throttle.Fullstop:
    # throttle_str = "FullStop"
    # if enum_throttle == Throttle.Loiter:
    # throttle_str = "Loiter"
    # if enum_throttle == Throttle.Full:
    # throttle_str = "Full"
    # if enum_throttle == Throttle.Flank:
    # throttle_str = "Flank"
    # if enum_throttle == Throttle.Cruise:
    # throttle_str = "Cruise"
    # if enum_throttle == Throttle.Unspecified:
    # throttle_str = "None"
    # lua_scrpt = "ScenEdit_SetUnit({GUID='%s', THROTTLEPRESET='%s'})" % (self.strGuid, throttle_str)
    # test = self.mozi_server.sendAndRecv(lua_scrpt)

    def set_desired_height(self, desired_height):
        """
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        if isinstance(desired_height, int) or isinstance(desired_height, float):
            lua_scrpt = "ScenEdit_SetUnit({guid='" + str(self.strGuid) + "',  altitude ='" + str(desired_height) + "'})"
            return self.mozi_server.sendAndRecv(lua_scrpt)
        else:
            pass

    def set_rader_shutdown(self, on_off):
        '''
        设置雷达开关机
		trunoff 开关机 true 开机  false 关机
        '''
        lua_scrpt = "Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s',rader = '%s'})" % (self.strGuid, on_off)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def set_sonar_shutdown(self, trun_off):
        '''
        设置声纳开关机
		trunoff 开关机 true 开机  false 关机
        '''
        lua_scrpt = "Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s',OECM = %s})" % (self.strGuid, trun_off)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def set_OECM_shutdown(self, trunoff):
        '''
        设置干扰开关机
	trunoff 开关机 true 开机  false 关机
        '''
        lua_scrpt = "Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s',OECM = %s})" % (self.strGuid, trunoff)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        手动开火函数
        作者：解洋
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量strWeaponInfo
        '''
        manual_lua = 'Hs_ScenEdit_AllocateWeaponToTarget(\'%s\',{TargetGUID=\'%s\'},%s,%s)' % (
            self.strGuid, target_guid, weapon_dbid, weapon_num)
        return self.mozi_server.sendAndRecv(manual_lua)

    def unitops_singleout(self, base_guid, unit_guid):
        '''

        设置在基地内单元出动
        base_guid : 单元所在机场的guid
        unit_guid : 单元的guid
        return :
        lua执行成功/lua执行失败
        '''
        lua_scrpt = "HS_LUA_AirOpsSingLeOut('%s',{'%s'})" % (base_guid, unit_guid)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def drop_active_sonobuoy(self, sideName, deepOrShallow):
        '''
        类别：推演所用函数
        投放主动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        lua_scrpt = "Hs_DropActiveSonobuoy('{}','{}','{}')".format(sideName, self.strGuid, deepOrShallow)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def drop_passive_sonobuoy(self, sideName, deepOrShallow):
        '''
        类别：推演所用函数
        投放被动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_DropPassiveSonobuoy('{}','{}','{}')".format(sideName, self.strGuid, deepOrShallow))

    def drop_sonobuoy(self, sideName, deepOrShallow, passiveOrActive):
        '''
        类别：推演所用函数
        投放声呐
        sidename 方的名称 
        deepOrShallow 深浅类型（'deep'：温跃层之下，'shallow'：温跃层之上）
	passiveOrActive  主被动类型（'active'：主动声呐，'passive'：被动声呐）
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_DropSonobuoy('{}','{}','{}','{}')".format(sideName, self.strGuid, deepOrShallow, passiveOrActive))

    def setUnitSide(self, oldside, newSide):
        '''
        类别：编辑所用函数
        改变单元所属阵营
        oldside 现在的方名称
        newSide 新的方名称
        案例：
        ScenEdit_SetUnitSide({side=' 红 方 ',name=' F-14E 型 “ 超 级 雄 猫 ” 战 斗 机',newside='蓝方'}
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetUnitSide({side='%s',name='%s',newside='%s'})" % (oldside, self.strName, newSide))

    def setLoadout(self, loadoutId, timeToReady_Minutes, ignoreMagazines, excludeOptionalWeapons):
        '''
        函数功能：将添加/改变的载荷
        UnitName string 要改变载荷的单元名称/GUID
        LoadoutID number 新载荷的 ID，0 = 使用当前载荷
        TimeToReady_Minutes number 载荷准备时间（分钟）
        IgnoreMagazines bool 新载荷是否依赖于已准备好武器的弹仓
        ExcludeOptionalWeapons bool 从载荷中排除可选武器（可选）
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetLoadout ({UnitName='%s',LoadoutID='%s',TimeToReady_Minutes='%s',IgnoreMagazines=%s,"
            "ExcludeOptionalWeapons=%s)" % (
                self.strName, loadoutId, timeToReady_Minutes, ignoreMagazines, excludeOptionalWeapons))

    def addReloadsToUnit(self, unitName, weaponDBID, number, weapon_max):
        '''
        将武器加入装具
        unitName 装具所属单元的名称/GUID
        weaponDBID 武器 DBID 
        number 要添加的数量
        weapon_max 装载武器的最大容量
        '''
        return self.mozi_server.sendAndRecv(
            "ScenEdit_AddReloadsToUnit({unitname='%s', w_dbid=%s, number=%s, w_max=%s})" % (
                unitName, weaponDBID, number, weapon_max))

    def addCargoToUnit(self, cargoDBID):
        '''
        函数功能：添加货物
        函数类型：推演类型
        cargoDBID 货物dbid    
        '''
        return self.mozi_server.sendAndRecv("Hs_AddCargoToUnit('{}',{})".format(self.strGuid, cargoDBID))

    def removeCargoToUnit(self, cargoDBID):
        '''
        删除货物
        unitId 单元ID
        cargoDBID 货物dbid  
        cargoDBID 货物dbid  
        '''
        return self.mozi_server.sendAndRecv("Hs_AddCargoToUnit('{}',{})".format(self.strGuid, cargoDBID))

    def removeCargoToUnit(self, cargoDBID):
        '''
        函数功能：删除货物
        函数类型：推演类型
        cargoDBID 货物dbid
        '''
        return self.mozi_server.sendAndRecv("Hs_RemoveCargoToUnit('{}',{})".format(self.strGuid, cargoDBID))

    def setMagazineWeaponCurrentLoad(self, guid, WPNREC_GUID, currentLoad):
        '''
        函数类别：编辑函数
        函数功能：设置弹药库武器数量
        Hs_ScenEdit_SetMagazineWeaponCurrentLoad({guid='%1',WPNREC_GUID='%2',currentLoad=%3})
        guid 单元
        WPNREC_GUID 武器guid
        currentLoad 当前挂载
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetMagazineWeaponCurrentLoad({guid='%s',WPNREC_GUID='%s',currentLoad=%s})" % (
                guid, WPNREC_GUID, currentLoad))

    def removeMagazine(self, guid, magazine_guid):
        '''
        删除弹药库
        Hs_ScenEdit_RemoveMagazine({guid='%1', magazine_guid='%2'})
        guid 单元
        magazine_guid 弹药库
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_RemoveMagazine({guid='%s', magazine_guid='%s'})" % (guid, magazine_guid))

    def setMagazineState(self, guid, magazine_guid, state):
        '''
        设置弹药库状态
        guid 单元
        magazine_guid 弹药库guid
        state  状态
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetMagazineState({guid='%s', magazine_guid='%s',state='%s'}" % (guid, magazine_guid, state))

    def setWeaponCurrentLoad(self, unitname, wpn_guid, number):
        '''
        设置武器数量
        unitname   单元名称
        wpn_guid   武器guid
        number     数量
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetWeaponCurrentLoad({unitname='%s',wpn_guid='%s',%s})" % (unitname, wpn_guid, number))

    def setWeaponReloadPriority(self, strCurrentUnitGuid, strWeaponRecord, isReloadPriority):
        '''
        设置武器重新装载优先级
        guid 单元guid
        WPNREC_GUID 弹药库guid
        isReloadPriority
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_SetWeaponReloadPriority({guid='%s',WPNREC_GUID='%s',IsReloadPriority=%s})" % (
                strCurrentUnitGuid, strWeaponRecord, isReloadPriority))

    def add_weapon_to_unit_magazine(self, side, guid, mag_guid, wpn_dbid, number):
        '''
       函数类别：编辑所用的函数
       功能说明：往弹药库内添加武器
        side 方
        guid 单元
        mag_guid 弹药库
        wpn_dbid 武器dbid
        number 数量
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_AddWeaponToUnitMagazine({side='%s',guid='%s',mag_guid='%s',wpn_dbid=%s,number=%s})" % (
                side, guid, mag_guid, wpn_dbid, number))

    def hs_scenEdit_air_refuel(self, guid, tanker_guid):
        '''
        函数功能：命令单元多种方式寻找加油机（自动寻找加油机、指定加油机、
        指定加油任务执行单元）进行加油。它与 ScenEdit_RefuelUnit 功能相同，只是它
        的参数是单元或任务的 GUID、后者的参数是单元或任务的名称。
        149
        北京华戍防务技术有限公司
        参数说明：
        1）table：表对象：
         guid：字符串。单元 GUID；
         tanker_guid：字符串。加油单元 GUID；
         mission_guid：字符串。加油任务 GUID。
        '''
        if tanker_guid == '':
            lua = "Hs_ScenEdit_AirRefuel({guid='%s'})" % (guid)
        else:
            lua = "Hs_ScenEdit_AirRefuel({guid='%s',tanker_guid = '%s'})" % (guid, tanker_guid)

    def scenEdit_set_unit_sensor_switch(self, rader='false', sonar='false', oecm='false'):
        '''
        函数功能：同时设置单元上多种类型传感器的开关状态。
        参数说明：
        1）table：表对象：
         RADER：布尔值。雷达开关状态标识符（true：开，false：关）；
         SONAR：布尔值。声呐开关状态标识符（true：开，false：关）；
         OECM：布尔值。攻击性电子对抗手段（即电子干扰）开关状态标识符（true：开，false：关）。
        '''
        lua = "Hs_ScenEdit_SetUnitSensorSwitch({name='%s', RADER=%s,SONAR=%s,OECM=%s})" % (
            self.strName, rader, sonar, oecm)
        return self.mozi_server.scenAndRecv(lua)

    def wcsf_contact_types_unit(self, holdTightFreeInherited):
        '''
        函数功能：控制指定单元对所有目标类型的攻击状态。 
        参数说明： 
        1）HoldTightFreeInherited：控制状态标识符（'Hold'：禁止，'Tight'：限制，
        'Free'：自由，'Inherited'：按上级条令执行）。 
        '''
        lua = "Hs_WCSFAContactTypesSUnit('%s','%s','%s')" % (self.m_Side, self.strGuid, holdTightFreeInherited)
        return self.sendAndRecv(lua)

    def scenedit_allocate_all_weapons_to_target(self, targetGuid, weaponDbid):
        '''
        函数功能：为手动交战分配同类型所有武器。 
        参数说明： 
        1）actriveUnitGuid：字符串。活动单元 GUID； 
        2）targetGuid：字符串。目标单元 GUID； 
        3）weaponDbid：数值型。武器数据库 GUID
        '''
        lua = "Hs_ScenEdit_AllocateAllWeaponsToTarget('%s','%s',%s)" % (self.strGuid, targetGuid, weaponDbid)
        self.mozi_server.scenAndRecv(lua)

    def scenEdit_removeWeapons_target(self, weaponSalvoGuid):
        '''
        函数功能：取消手动交战时齐射攻击目标。 
        参数说明：
        1）WeaponSalvoGUID：字符串。武器齐射 GUID。 
        '''
        lua = "Hs_ScenEdit_RemoveWeapons_Target('%s','%s')" % (self.strGuid, weaponSalvoGuid)
        self.mozi_server.scenAndRecv(lua)

    def scenEdit_set_salvo_timeout(self, b_isSalvoTimeout='false'):
        '''
        作者：解洋
        时间：2020-3-11
        类别：推演使用函数
        函数功能：控制手动交战是否设置齐射间隔。 
        参数说明： 
        1）b_isSalvoTimeout：是否设置齐射间隔的状态标识符（true：是，false：
        否）
        '''
        lua = "Hs_ScenEdit_SetSalvoTimeout(%s) " % b_isSalvoTimeout
        self.mozi_server.scenAndRecv(lua)

    def scenEdit_allocate_salvoTo_target(self, targetGuid, weaponDbid):
        '''
        作者：解洋
        时间：2020-3-11
        类别：推演使用函数
        函数功能：清空手动攻击时武器的航路点。 
        参数说明： 
        1）Ac tiveUnitGUID：单元 GUID； 
        2）WeaponSalvoGUID：武器齐射 GUID。 
        '''
        lua = "Hs_ScenEdit_AllocateSalvoToTarget('%s','%s',%s)" % (self.strGuid, targetGuid, weaponDbid)
        self.mozi_server.scenAndRecv(lua)

    def allo_cate_weapon_auto_targeted(self, target_guids, weapon_dbid, num):
        '''
        函数功能：为自动交战进行弹目匹配。此时自动交战意义在于不用指定对多
        个目标的攻击顺序。 
        参数说明： 
        1）actriveUnitGuid：字符串。活动单元 GUID； 
        2）{contactGuids}：表对象。目标单元 GUID 组成的表对象。 
        3）weaponDbid：数值型。武器数据库 GUID；
        4）Num：数值型。武器发射数量
        '''
        targets = None
        for target_guid in target_guids:
            if targets:
                targets += ",'%s'" % target_guid
            else:
                targets = "'%s'" % target_guid
        lua = "Hs_AllocateWeaponAutoTargeted(%s,{%s},%s,%s)" % (self.strGuid, targets, weapon_dbid, num)

    def Hs_AutoTargeted(self, contactGuids):
        '''
        函数功能：让单元自动进行弹目匹配并攻击目标。 
        参数说明： 
        1）actriveUnitGuid：字符串。活动单元 GUID； 
        2）{contactGuids}：表对象。目标单元 GUID 组成的表对象
        '''
        contacts = None
        for contact_guid in contactGuids:
            if contacts:
                contacts += ",'%s'" % contact_guid
            else:
                contacts = "'%s'" % contact_guid

        lua = "Hs_AutoTargeted('%s',{%s})" % (self.strGuid, contacts)
        return self.mozi_server.sendAndRecv(lua)

    def add_unit_host(self, base_guid):
        '''
       作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：将单元部署进基地
        @param base_guid:基地的guid
        @return:
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_HostUnitToParent('{}','{}')".format(self.strName, base_guid))

    def set_unit_attribute(self, **kwargs):
        '''
       作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：设置已有单元的属性
        @param kwargs: 不同的属性和属性值
        @return:表对象。单元属性的详细信息
        '''
        (key, value), = kwargs.items()
        return self.mozi_server.sendAndRecv("ScenEdit_SetUnit({%s,%s =%r})" % (self.strName, key, value))

    def set_unitcomponent_damage(self, **kwargs):
        '''
       作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：设置单元各组件的毁伤状态
        @param kwargs: 组件的名称和毁伤状态组成的字典
        @return:
        '''
        key, value = kwargs.items()
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetUnitDamage({%s, %s,  {{%s, %r}}})" % (self.m_Side, self.strName, key, value))

    def UpdateUnit(self, options):
        result = self.mozi_server.sendAndRecv(" ReturnObj(scenEdit_UpdateUnit({}))".format(options))
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

    def add_mount(self, **kwargs):
        """
       作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：为单元添加武器挂架
        @param kwargs:挂架
        @return:
        """
        for key, value in kwargs:
            self.mozi_server.sendAndRecv("Hs_ScenEdit_AddMount({{},m{},{}})".format(self.strName, key, value))

    def remove_mount(self, i):
        """
       作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：删除单元中指定的武器挂架
        @param i:武器挂架的索引值
        @return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_RemoveMount({'{}',{}})".format(self.strName, self.mounts[i].mount_guid))

    def addWeapon(self, guid, wpn_dbid, MOUNT_GUID):
        """
       函数类别：编辑所用的函数
       功能说明：给单元挂架或飞机当前挂载方案中添加武器
        @param guid:单元guid
        @param wpn_dbid:武器dbid
        @param MOUNT_GUID:挂架guid
        @return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_AddWeapon({guid='%s',wpn_dbid=%s,MOUNT_GUID = '%s',IsTenThousand=true})" % (
                guid, wpn_dbid, MOUNT_GUID))

    def removeWeapon(self, unitname, wpn_guid):
        """
       函数类别：编辑所用的函数
       功能说明：通过武器属性删除单元的武器
        @param unitname: 单元名称
        @param wpn_guid: 武器guid
        @return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_ScenEdit_RemoveWeapon({unitname='%s', wpn_guid='%s'})" % (unitname, wpn_guid))

    def setLoadout(self, unitName, loadoutId, timeToReady_Minutes, ignoreMagazines, excludeOptionalWeapons):

        '''
        将添加/改变的载荷
        UnitName string 要改变载荷的单元名称/GUID
        LoadoutID number 新载荷的 ID，0 = 使用当前载荷
        TimeToReady_Minutes number 载荷准备时间（分钟）
        IgnoreMagazines bool 新载荷是否依赖于已准备好武器的弹仓
        ExcludeOptionalWeapons bool 从载荷中排除可选武器（可选）
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetLoadout ({UnitName='%s',LoadoutID='%s',"
                                            "TimeToReady_Minutes='%s',IgnoreMagazines=%s, "
                                            "ExcludeOptionalWeapons=%s)" % (
                                                unitName, loadoutId, timeToReady_Minutes, ignoreMagazines,
                                                excludeOptionalWeapons))

    '''
    Hs_UpdateWayPoint 根据单元和航路点所在的数组中的位置修改航路点
    UnitNameOrID 单元
    WayPointLocation 航路点在数组中的位置
    latitude  纬度
    longitude 经度
    '''

    def update_way_point(self, wayPointLocation, lat, lon):
        """
        作者：赵俊义
        日期：2020-3-11
        函数功能：更新单元航路点的具体信息
        函数类别：推演函数
        :param wayPointLocation: 数值型。航路点在航路点序列（以 0 为起始序号）中的序号
        :param lat: 纬度
        :param lon: 经度
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "Hs_UpdateWayPoint('%s',%s,{latitude=%s,longitude=%s})" % (
                self.strGuid, wayPointLocation, lat, lon))

    '''
    Hs_UpdateWayPointSensorStatus 某单元第几个航路点修改电磁管控
    activeUnitGuid 单元guid
    WayPointIndex  航路点顺序
    sensor         传感器
    sensorStatus   传感器状态
    '''

    def set_way_point_sensor(self, wayPointIndex, sensor, sensorStatus):
        """
        函数功能：设置航路点传感器的开关状态
        函数类别：推演函数
        :param wayPointIndex:航路点顺序
        :param sensor:传感器
        :param sensorStatus:传感器状态
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "updateWayPointSensorStatus('{}',{},'{}','{}')".format(self.strGuid, wayPointIndex, sensor, sensorStatus))

    def set_unit_damage(self, overalldamage, comp_guid, level):
        """
        作者：赵俊义
        日期：2020-3-12
        函数功能：设置单元各组件的毁伤值
        函数类别：编辑函数
        :param overalldamage:数值型。总体毁伤
        :param comp_guid: 组件的guid
        :param level: 毁伤级别
        :return:
        """
        return self.mozi_server.sendAndRecv("HS_SetUnitDamage({guid={},OVERALLDEMAGE={},components={{},'{}'}})"
                                            .format(self.strGuid, overalldamage, comp_guid, level))

    def edit_magazine_weapon_number(self, mag_guid, wpn_dbid, number):
        """
        作者：赵俊义
        日期：2020-3-12
        函数功能：往单元的弹药库中添加指定数量的武器
        函数类别：编辑函数
        :param wpn_dbid:数值型。武器 GUID；
        :param number:数值型。武器数量。
        :return:
        """
        return self.mozi_server.sendAndRecv(
            "ScenEdit_AddWeaponToUnitMagazine({name={},mag_guid={},wpn_dbid={},number={}})".format(self.strGuid,
                                                                                                   mag_guid, wpn_dbid,
                                                                                                   number))
