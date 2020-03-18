# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : scenario.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.situation import CSituation
from ..entitys.side import CSide


class CScenario():
    '''想定'''
    def __init__(self, mozi_server):
        self.mozi_server = mozi_server
        # 类名
        self.ClassName = "CCurrentScenario"
        # GUID
        self.strGuid = ""
        # 标题
        self.strTitle = ""
        # 想定文件名
        self.strScenFileName = ""
        # 描述
        self.strDescription = ""
        # 当前时间
        self.m_Time = ""
        # 是否是夏令时
        self.bDaylightSavingTime = False
        # 当前想定第一次启动的开始时间
        self.m_FirstTimeRunDateTime = ""
        # 用不上
        self.m_FirstTimeLastProcessed = 0.0
        # 用不上
        self.m_grandTimeLastProcessed = 0.0
        # 夏令时开始时间（基本不用）
        self.strDaylightSavingTime_Start = 0.0
        # 夏令结束时间（基本不用）
        self.strDaylightSavingTime_End = 0.0
        # 想定开始时间
        self.m_StartTime = ""
        # 想定持续时间
        self.m_Duration = ""
        # 想定精细度
        self.sMeta_Complexity = 1
        # 想定困难度
        self.sMeta_Difficulty = 1
        # 想定发生地
        self.strMeta_ScenSetting = ""
        # 想定精细度的枚举类集合
        self.strDeclaredFeatures = ""
        # 想定的名称
        self.strCustomFileName = ""
        # 编辑模式剩余时间
        self.iEditCountDown = 0
        # 推演模式剩余时间
        self.iStartCountDown = 0
        # 暂停剩余时间
        self.iSuspendCountDown = 0
        # 获取推演的阶段模式
        self.m_CurrentStage = 0
        #推演方
        self.m_sides={}
        #态势
        self.situation = CSituation(mozi_server)

    #def get_side_byname(self, side_name):
        #'''
        #根据名称获取方
        #'''
        #self.is_side(side_name)
        #return self.m_sides[side_name]

    def lua_addSide(self, sideName):
        '''
        类别：编辑使用函数
        添加方 complate
        :param sideName:
        :return:
        '''
        return self.mozi_server.sendAndRecv("HS_LUA_AddSide({side='%s'})" % (sideName))

    def scenEdit_removeSide(self, side):
        '''
        类别：编辑使用函数
        移除推演方
        :param side:
        :return:
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_RemoveSide({side='%s'})" % (side))

    def scenEdit_setSidePosture(self, sideAName, sideBName, relation):
        '''
        类别：编辑使用函数
        设置对抗关系 complate
        :param sideAName:
        :param sideBName:
        :param relation:：字符串。立场编码（'F'-友好，'H'-敌对，'N'-中立，'U'-非友）
        :return:
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetSidePosture('{}','{}','{}')".format(sideAName, sideBName, relation))
   
    def reset_allSide_scores(self):
        '''
        类别：编辑使用函数
        重置所有推演方分数
        '''        
        return self.sendAndRecv("Hs_ResetAllSideScores()")
    

    def reset_all_LossesExpenditures(self):
        '''
        类别：编辑使用函数
        将各推演方所有战斗损失、战斗消耗、单元损伤等均清零。 
        '''
        return self.sendAndRecv("Hs_ResetAllLossesExpenditures()")

    def set_scenario_time(self, set_time):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：设置想定时间
        函数类别：推演所用的函数
        '''
        return self.mozi_server.sendAndRecv("Hs_SetScenarioTime('{}')".format(set_time))

    def get_current_time(self):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：获得当前想定时间
        函数类别：推演所用的函数
        '''
        lua = "ReturnObj(ScenEdit_CurrentTime())"
        ret_time = self.mozi_server.sendAndRecv(lua)
        return ret_time

    def add_side(self, side):
        '''

        作者：赵俊义
        日期：2020-3-7
        功能说明：添加推演方
        函数类别：推演所用的函数
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_AddSide('{}')".format(side))

    def get_player_name(self):
        '''
        作者：赵俊义
        日期：2020-3-7
        函数类别：获取当前推演方的名称
        功能说明：添加推演方
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_PlayerSide()")

    def set_side_posture(self, sideA, sideB, posture):
        '''
        作者：赵俊义
        日期：2020-3-9
        函数类别：编辑所用的函数
        功能说明：设置一方对另一方的立场
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetSidePosture('{}','{}')".format(sideA, sideB, posture))

    def get_side_posture(self, sideA, sideB):
        '''
       作者：赵俊义
       日期：2020-3-9
       函数类别：推演所用的函数
       功能说明：获取一方对另一方的立场
       :param sideA:一方的名称
       :param sideB:另一方的名称
       '''
        return self.mozi_server.sendAndRecv("ScenEdit_GetSidePosture('{}','{}')".format(sideA, sideB))

    def change_unit_side(self, sideA, sideB, strName):
        '''
        作者：赵俊义
       日期：2020-3-9
       函数类别：推演所用的函数
       功能说明：改变单元的方
        @param sideA: 单元所在的方
        @param sideB: 单元要改变的方
        @param strName: 单元名称
        @return:
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_GetSidePosture('{}','{}','{}')".format(sideA, strName, sideB))

    def remove_side(self, sideName):
        '''
        作者：赵俊义
       日期：2020-3-9
       函数类别：编辑所用的函数
       功能说明：移除某个推演方
        @param sideName: 方的名字
        @return:
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_RemoveSide('{}')".format(sideName))

    def importInstFile(self, side, filename):
        '''
        导入 inst 文件
        side string 导入 inst 文件的阵营
        filename string inst 文件名
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_ImportInst('{}','{}')".format(side, filename))

    def dump_rules(self):
        """
       作者：赵俊义
       日期：2020-3-10
       函数类别：推演所用的函数
       功能说明：向系统安装目录下想定默认文件夹以 xml 文件的方式导出事件、条件、触发器、动作、特殊动作。
        @return:由事件内容组成、以 xml 文件格式输出的字符串。
        """
        return self.mozi_server.sendAndRecv("Tool_DumpEvents()")

    def execute_event_action(self, eventGuid ):
        """
       作者：赵俊义
       日期：2020-3-10
       函数类别：推演所用的函数
       功能说明：执行某个 lua 类型的动作，会将动作中的 lua 脚本运行一次，可
                以查验动作中 lua 脚本效果
        @param eventGuid: 字符串。事件的描述或 GUID。
        @return:
        """
        return self.mozi_server.sendAndRecv("ScenEdit_ExecuteEventAction ('{}')".format(eventGuid))

    def update_event(self, eventGuid, newName, description, isActive, isShow, isReatable, prob):
        """
       作者：赵俊义
       日期：2020-3-10
       函数类别：推演所用的函数
       功能说明：更新事件的属性
        @param eventGuid: 要更新事件的guid
        @param newName:新事件名称
        @param description:事件说明
        @param isActive:是否启用
        @param isShow:是否显示
        @param isReatable:是否可重复
        @param prob:发生概率
        @return:
        """
        lua_scrpt = "ScenEdit_UpdateEvent('{}',{'{}', '{}',{},{},{},{}})".format(eventGuid, newName, description,
                                                                                 isActive, isShow, isReatable, prob)
        return self.mozi_server.sendAndRecv(lua_scrpt)
    
    
