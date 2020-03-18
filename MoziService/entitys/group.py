# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : group.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CGroup(CActiveUnit):
    def __init__(self):
        self.m_GroupCenter = ""
        self.strDockAircraft = ""
        # 悬停速度
        self.fHoverSpeed = 0.0
        # 低速
        self.fLowSpeed = 0.0
        # 巡航
        self.fCruiseSpeed = 0.0
        # 军用/全速
        self.fMilitarySpeed = 0.0
        # 加速/最大
        self.fAddForceSpeed = 0.0
        # 期望高度
        self.fDesiredAltitude = 0.0
        # 是否在陆地上
        self.bIsOnLand = False
        # 航路点需要燃油数
        self.strWayPointFuel = ""
        # 编组领队
        self.m_GroupLead = ""
        # 编组类型
        self.m_GroupType = 0
        # 载艇按钮的文本描述
        self.strDockShip = ""
        # 编组所有单元GUID
        self.m_UnitsInGroup = ""
        # 航路点剩余航行距离
        self.strWayPointDTG = ""
        # 航路点描述
        self.strWayPointDescription = ""
        # 发送队形方案详情
        self.m_FormationFormula = ""
        # 航路点剩余航行时间
        self.strWayPointTTG = ""
        # 发送队形方案选择的索引
        self.iFormationSelectedIndex = 0
        # 航路点名称
        self.strWayPointName = ""
        # from dong
        # 编组中心点经度
        self.m_GroupCenterLongitude = ""
        # 编组中心点纬度
        self.m_GroupCenterLatitude = ""
        # 编组中心点高度
        self.m_GroupCenterAltitude_ASL = ""

    def delete_sub_object(self):
        """
        删除时删除子对象
        :return:
        """
        del_list = list(self.way_points.keys())
        for guid, point in self.way_points.items():
            del_list.extend(point.delete_sub_object())
        del self.way_points

        if self.doctrine is not None:
            del_list.append(self.doctrine.guid)
            del self.doctrine
        return del_list
        
    def removeUnitFromGroup(self, unitId):
        '''
        类别：编辑所用函数
        将单元移除编组
        unitId 单元ID
        '''
        return self.mozi_server.sendAndRecv("Hs_RemoveUnitFromGroup('{}')".format(unitId))
 
    def scenEdit_AddGroup(self, unitGuidList):
        '''
        类别：编辑所用函数
        函数功能：将同类型单元单元合并创建编队，暂不支持不同类型单元。
        参数说明：
        1）{unitGuidstoadd}：同类型单元 GUID 组成的表对象。
        2）返回参数：编队信息组成的表对象。
        用法：
        scenEdit_AddGroup({'613f00e1-4fd9-4715-a672-7ec5c22486cb','431337a9-987e-46b6-8cb8-2f92b9b80335','0bc3        1a3c-096a-4b8e-a
        23d-46f7ba3b06b3'})
        '''
        res =  self.mozi_server.sendAndRecv("ReturnObj(Hs_ScenEdit_AddGroup({}))".format(unitGuidList))
        return res.split('\r\n')[5].split('=')[1].split(',')[0].replace(',','').replace('\'','').replace(' ','').s  
 
   
    def group_formation(self, table):
        '''
        类别：推演所用函数
        函数功能：设置编队领队及队形。
        参数说明：
        1）table：编队成员队形信息组成的表对象：
         NAME：字符串。单元名称；
         SETTOGROUPLEAD：是否担当领队（'Yes'：是，'No'：否）；
         TYPE：与领队的空间相对关系的维持模式（'FIXED'：维持平动，'Rotating'：+ASD
        同步转动）；
         BEARING：数值型。与领队的相对方位；
         DISTANCE：数值型。与领队的距离。
        2）返回参数：编队队形信息组成的表对象
        '''     
        return self.mozi_server.sendAndRecv("Hs_GroupFormation({})".format(table))

    def setUnitSprintAndDrift(self, unitNameOrID, trueOrFalse):
        '''
        函数功能：控制编队内非领队单元相对于编队是否进行高低速交替航行。
        参数说明：
        1）UnitNameOrID：字符串。单元名称或 GUID； 
        2）TrueOrFalse：布尔值。是否交替航行的状态标识符（true：是，false：否）。
        '''
        return self.mozi_server.sendAndRecv("Hs_SetUnitSprintAndDrift('{}',{})".format(unitNameOrID, trueOrFalse))
