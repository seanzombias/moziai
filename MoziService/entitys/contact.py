# -*- coding:utf-8 -*-
##########################################################################################################
# File name : contact.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################


class CContact():
    contact_type = {
        # 空中目标
        0: "Air",
        # 导弹
        1: "Missile",
        # 水面 / 地面
        2: "Surface",
        # 潜艇
        3: "Submarine",
        # 未确定的海军
        4: "UndeterminedNaval",
        # 瞄准点？？
        5: "Aimpoint",
        # 轨道目标
        6: "Orbital",
        # 固定设施
        7: "Facility_Fixed",
        # 移动设施
        8: "Facility_Mobile",
        # 鱼雷
        9: "Torpedo",
        # 水雷
        10: "Mine",
        # 爆炸
        11: "Explosion",
        # 不确定
        12: "Undetermined",
        # 空中诱饵
        13: "Decoy_Air",
        # 表面诱饵
        14: "Decoy_Surface",
        # 陆地诱饵
        15: "Decoy_Land",
        # 水下诱饵
        16: "Decoy_Sub",
        # 声纳浮标
        17: "Sonobuoy",
        # 军事设施
        18: "Installation",
        # 空军基地
        19: "AirBase",
        # 海军基地
        20: "NavalBase",
        # 移动集群
        21: "MobileGroup",
        # 激活点：瞄准点
        22: "ActivationPoint",
    }

    def __init__(self, guid, mozi_server):
        self.mozi_server = mozi_server
        # 对象类名
        self.ClassName = ""
        # 名称
        self.strName = ""
        # Guid
        self.strGuid = guid
        # 地理高度
        self.fAltitude_AGL = 0.0
        # 海拔高度
        self.iAltitude_ASL = 0
        # 所在推演方ID
        self.m_Side = ""
        # 实体类别
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
        # 是否在陆地上
        self.bIsOnLand = False
        # 可能匹配结果
        self.m_MatchingDBIDList = ""
        # 识别出的辐射平台
        self.strRadiantPoint = ""
        self.strIconType = ""
        self.strCommonIcon = ""
        # 目标类型
        self.m_ContactType = 0
        # 属方是否已知
        self.bSideIsKnown = False
        # 单元的识别状态
        self.m_IdentificationStatus = 0
        # 本身单元的GUID
        self.m_ActualUnit = ""
        # 探测到的推演方
        self.m_OriginalDetectorSide = ""
        # 其它推演方对本目标的立场姿态
        self.m_SidePostureStanceDictionary = ""
        # 速度是否已知
        self.bSpeedKnown = False
        # 朝向是否已知
        self.bHeadingKnown = False
        # 高度是否已知
        self.bAltitudeKnown = False
        # 电磁辐射Title
        self.strElectromagnetismEradiateTitle = ""
        # 电磁辐射集合
        self.strElectromagnetismEradiate = ""
        # 匹配结果标题
        self.strMatchingTitle = ""
        # 侦察记录
        self.m_DetectionRecord = ""
        # 不确定区域集合
        self.m_UncertaintyArea = ""
        # 目标持续时间
        self.strAge = ""
        # 取目标发射源容器中传感器的最大探测距离
        self.fMaxDetectRange = 0.0
        # 获取最大对海探测范围
        self.fMaxRange_DetectSurfaceAndFacility = 0.0
        # 获取最大对潜探测范围
        self.fMaxRange_DetectSubsurface = 0.0
        # 获取目标探测时间
        self.fTimeSinceDetection_Visual = 0.0
        # 获取瞄准目标的武器数量
        self.iWeaponsAimingAtMe = 0
        # 目标武器对空最大攻击距离
        self.fAirRangeMax = 0.0
        # 目标武器对海最大攻击距离
        self.fSurfaceRangeMax = 0.0
        # 目标武器对陆最大攻击距离
        self.fLandRangeMax = 0.0
        # 目标武器对潜最大攻击距离
        self.fSubsurfaceRangeMax = 0.0
        # 态势控制——目标电磁辐射显示信息
        self.strContactEmissions = ""
        self.m_OriginalDetectorSide = ''
        #那一方的目标
        self.contact_side = ''

    def get_contact_info(self):
        '''
        类别：编辑所用函数
        获取目标信息字典
        '''
        info_dict = {
            'type': self.get_type_description(),
            'typed': self.m_ContactType,
            'classificationlevel': self.m_IdentificationStatus,
            'name': self.strName,
            'guid': self.m_ActualUnit,
            'latitude': self.dLatitude,
            'longitude': self.dLongitude,
            'altitude': self.fCurrentAltitude_ASL,
            'heading': self.fCurrentHeading,
            'speed': self.fCurrentSpeed,
            'firingAt': [],
            'missile_defence': 0,
            'fromUnits': self.m_DetectionRecord,  # ?
            'fg': self.guid,
        }
        return info_dict
    
    def parse_area(cls, str_area):
        '''
        类别：编辑所用函数
        解析不明目标的区域
        str_area 区域点信息
        '''
        if str_area == "":
            return []
        else:
            areas = []
            points = str_area.split("@")
            for point_content in points:
                values = point_content.split("$")
                areas.append({
                    'latitude': float(values[1]),
                    'longitude': float(values[0]),
                    'altitude': float(values[2])
                })
            return areas  
    
    def set_mark_contact(self,contact_type):
        '''
        类别：编辑所用函数
        函数功能：标识目标立场。
        参数说明：
        1）SideNameOrGuid：字符串。推演方名称或 GUID； 
        2）UnitGuid：字符串。目标 GUID； 
        3）ContactType：字符串。目标立场类型（'F'：友方，'N'：中立，'U'：非友方，'H'：敌方）。
        '''
        lua_scrpt = "Hs_SetMarkContact('%s','%s','%s')"%(self.m_Side,self.strGuid,contact_type)
        self.mozi_server.sendAndRecv(lua_scrpt)
        
    def hs_contact_rename(self):
        '''
        放弃目标
        不再将所选目标列为探测对象。
        side_name 字符串。推演方名称或 GUID
        Hs_ContactDropTarget('红方','a5561d29-b136-448b-af5d-0bafaf218b3d')
        '''   
        lua_scrpt = "Hs_ContactDropTarget('%s','%s')"%(self.m_OriginalDetectorSide,self.strGuid)
        self.mozi_server.sendAndRecv(lua_scrpt)
    
    def set_mark_contact(self,new_name):
        '''
        类别：编辑所用函数
        函数功能：给目标重新命名。
        参数说明：
        1）new_name：字符串。新名称。
        '''
        lua = "Hs_ContactRename('%s','%s','%s')"%(self.m_OriginalDetectorSide,self.strGuid,new_name)
        self.mozi_server.scenAndRecv(lua)
