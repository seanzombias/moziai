# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : weapon.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CWeapon(CActiveUnit):
    '''武器'''
    def __init__(self):
        super().__init__()
        # 提供数据链的活动单元
        self.m_strDataLinkParentGuid = ""
        # 主要目标
        self.m_PrimaryTargetGuid = ""
        # 反潜模式使用时最小作用距离
        self.fRangeASWMin = 0.0
        # 反潜模式使用时最大作用距离
        self.fRangeASWMax = 0.0
        # 最小射程
        self.fRangeLandMin = 0.0
        # 最大射程
        self.fRangeLandMax = 0.0
        # 反舰模式使用时最小距离
        self.fRangeASUWMin = 0.0
        # 反舰模式使用时最大距离
        self.fRangeASUWMax = 0.0
        # 防空作战最小大作用距离
        self.fRangeAAWMin = 0.0
        # 防空作战最大作用距离
        self.fRangeAAWMax = 0.0
        # 武器类型
        self.m_WeaponType = 0
        # 打击的目标类型
        self.m_WeaponTargetType = ""
        # 是否是空射制导武器
        self.bIsOfAirLaunchedGuidedWeapon = False
        # 是否是主动声纳
        self.bSonobuoyActive = False
        # 发射单元GUID
        self.m_FiringUnitGuid = ""
        # 父挂架
        self.m_ParentMount = ""
        # 父弹药库
        self.m_ParentMagazine = ""
        # 声呐深度设置
        self.m_SonobuoyDepthSetting = 0
        # 如果是声纳浮标则发送它的剩余时间
        self.strSonobuoyRemainingTime = ""

    def delete_sub_object(self):
        """
        删除时删除子对象
        :return:
        """
        del_list = []
        if self.doctrine is not None:
            del_list.append(self.doctrine.guid)
            del self.doctrine

        del_list.extend(self.way_points.keys())
        del self.way_points
        del_list.extend(list(self.sensors.keys()))
        del self.sensors
        return del_list

    def get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            "guid": self.guid,
            "DBID": self.iDBID,
            "subtype": "0",
            "facilityTypeID": "",
            "name": self.strName,
            "side": self.side_name,
            "proficiency": "",  # ?
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,  # ?
            "fuelstate": "",
            "weaponstate": -1,  # ?
            "mounts": self.get_mounts_info(),
            "targetedBy": self.get_target_by_info(),
            "target": self.m_PrimaryTargetGuid,
            "shooter": self.m_FiringUnitGuid,
            "type": "Weapon",
            "fuel": -1,  # ?
            "damage": -1,  # ?
            "sensors": self.get_sensors_info(),
            "weaponsValid": self.get_valid_weapons()
        }
        return info_dict


    def weapon_auto_detectable(self,isAutoDetectable):
        '''
        单元自动探测到
        isAutoDetectable：是否探测到 true?false complate
        '''
        super().unit_auto_detectable(isAutoDetectable)
        

    def unitTargetSimBreakOff(self, Type, side, targetGuid, unitGuid, distance):
        '''
        武器距离目标多少公里后暂停
        type:类型
        side：推演方
        targetGuid：目标guid
        weaponDBID:武器的BDID
        distance:距离（公里） complate
        '''
        weaponTargetSimBreakOff = "Hs_WeaponTargetSimBreakOff('%s', {SIDE = '%s', CONTACTGUID = '%s', ACTIVEUNITGUID = '%s', DISTANCE = %s})"% (
            Type,side,targetGuid,self.strGuid,distance)
        return self.sendAndRecv(weaponTargetSimBreakOff) 
    
    def Hs_ClearWeaponWay(self,activeUnitGUID):
        '''
        函数功能：清空手动攻击时武器的航路点。 
        参数说明： 
        1）activeUnitGUID：单元 GUID；
        '''
        lua ="Hs_ClearWeaponWay('%s','%s')"%(activeUnitGUID,self.iDBID)
        self.mozi_server.scenAndRecv(lua)
        
    def set_weapon_way(self,activeUnitGUID,contactID,longitude,latitude) :
        '''
        作者：解洋
        时间：2020-3-11
        类别：推演使用函数
        函数功能：对可设置航路的武器在手动攻击时绘制武器的航线。 
        参数说明： 
        1）ActiveUnitGUID：字符串。单元 GUID； 
        2）ContactID：字符串。目标 GUID； s
        3）Longitude：数值型。经度； 
        4）Latitude：数值型。纬度。 
        '''
        lua = "Hs_SetWeaponWay('%s','%s','%s',%s,%s)"%(activeUnitGUID,self.strGuid,contactID,longitude,latitude)
        self.mozi_server.scenAndRecv(lua)
        
        
    def Hs_ScenEdit_SetSalvoTimeout(self, b_isSalvoTimeout = 'false') :
        '''
        作者：解洋
        时间：2020-3-11
        类别：推演使用函数
        函数功能：控制手动交战是否设置齐射间隔。 
        参数说明： 
        1）b_isSalvoTimeout：是否设置齐射间隔的状态标识符（true：是，false：
        否）
        '''
        lua = "Hs_ScenEdit_SetSalvoTimeout(%s) "%(b_isSalvoTimeout)
        self.mozi_server.scenAndRecv(lua)
        
    def hs_scenEdit_allocate_salvoTo_target(self,actriveUnitGuid,targetGuid,weaponDbid):
        '''
        作者：解洋
        时间：2020-3-11
        类别：推演使用函数
        函数功能：清空手动攻击时武器的航路点。 
        参数说明： 
        1）ActiveUnitGUID：单元 GUID； 
        2）WeaponSalvoGUID：武器齐射 GUID。 
        '''
        lua = "Hs_ClearWeaponWay('ActiveUnitGUID','WeaponSalvoGUID')"%()
        self.mozi_server.scenAndRecv(lua)