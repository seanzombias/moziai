#!/usr/bin/python
# -*- coding: utf-8 -*-
# by aie

#upvalues: mozi, env
#need to use mozi
#need to use env
from behaviorTree.bt.basic import *
from behaviorTree.bt.detail import *

def OffensiveConditionalCheck(mozi,env):
    '''
    判断本方的目标和本方的单元那个数量更多
    目标为0 返回false
    目标小于单元数量返回true
    目标大于单元数量返回false
    '''
    side_dic = env.scenario.situation.side_dic
    for key ,_side in side_dic.items():
        if _side.strName == env.red_side_name:
            side = _side       
    contactstotal = len(side.contacts)
    unitstotal = len(side.get_all_unitinfo())
    if contactstotal == 0:
        return False
    if contactstotal <= unitstotal:
        return True
    else:
        return False

def addAircraftAction(mozi,env):
    side_dic = env.scenario.situation.side_dic
    for key ,_side in side_dic.items():
        if _side.strName == env.red_side_name:
            side = _side     
    contactstotal = len(side.contacts)
    if contactstotal == 0:
        return False
    mozi.addAircarft('红方', 'Aircraft', 'attack', '2579', '32.9', '45.4', '10010', '300.0', '3000.0')
    return True

def attackMissionCreateAction(mozi,env):
    #cs, side = mozi.getSideInfo(env.red_side_name)
    side_dic = env.scenario.situation.side_dic
    for key ,_side in side_dic.items():
        if _side.strName == env.red_side_name:
            side = _side 
    if len(side.contacts)==0 or len(side.units)==0 :
        return False
    for key,contact in side.contacts.items():
        break
    mozi.sendAndRecv("Hs_SetMarkContact('红方', '{}', 'U')".format(contact.strGuid))
    mozi.sendAndRecv("ScenEdit_AddMission('红方','strike2','strike',{type='land'})")
    mozi.sendAndRecv("ScenEdit_AssignUnitAsTarget({'%s'}, 'strike2')" %(contact.strGuid))


    side_units=side.get_all_unitinfo()    
    for k,unit in side_units.items():
        tmpstate = unit.strActiveUnitStatus
        if tmpstate != 'Tasked':
            mozi.sendAndRecv("ScenEdit_AssignUnitToMission('%s', 'strike2')"%(k))
            print(1)

    return True

def attackMissionUpdateAction(mozi,env):
    side_dic = env.scenario.situation.side_dic
    for key ,_side in side_dic.items():
        if _side.strName == env.red_side_name:
            side = _side       
    #cs, side = mozi.getSideInfo(env.red_side_name)
    side_units=side.get_all_unitinfo()
    n = 0
    for k,tmpstate in side_units.items():
        if tmpstate != 'Tasked':
            n = n+1
    if n == len(side_units):
        return False

    m = 0
    for k in side_units.items():
        dist = eval(mozi.getToolRange(eval(k.guid), eval(side.contacts[1].guid)))
        if dist < 20 :
            mozi.setEMCON('Unit',eval(k.guid),'Radar=Active')
        else:
            m = m+1

    if m == len(side.units):
        return False
    else:
        return True

