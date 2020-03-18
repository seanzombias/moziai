#!/usr/bin/python
# -*- coding: utf-8 -*-
# by aie
#
from behaviorTree.bt.nodes import *
from behaviorTree.bt.treeBT import BT

def initializeMerimackMonitorAI(env,sideName,lenAI,options):
    '''
    加载ai环境
    '''
    
    side_dic = env.scenario.situation.side_dic
    for key ,_side in side_dic.items():
        if _side.strName == sideName:
            side = _side            
    sideGuid = side.strGuid
    shortSideKey = "a"+str(lenAI + 1)
    attributes = options

    merimackSelector = BT()

    offensiveDoctrineSequence = BT()
    addAircraftBT = BT()

    offensiveDoctrineConditionalBT = BT()
    offensiveDoctrineSeletor = BT()

    attackDoctrineSelector = BT()

    attackDoctrineUpdateAirMissionBT = BT()
    attackDoctrineCreateAirMissionBT = BT()

    merimackSelector.addChild(offensiveDoctrineSequence)
    merimackSelector.addChild(addAircraftBT)
    offensiveDoctrineSequence.addChild(offensiveDoctrineConditionalBT)
    offensiveDoctrineSequence.addChild(offensiveDoctrineSeletor)
    offensiveDoctrineSeletor.addChild(attackDoctrineSelector)
    attackDoctrineSelector.addChild(attackDoctrineUpdateAirMissionBT)
    attackDoctrineSelector.addChild(attackDoctrineCreateAirMissionBT)

    merimackSelector.make(merimackSelector.select,sideGuid,shortSideKey,attributes)

    offensiveDoctrineSequence.make(offensiveDoctrineSequence.sequence,sideGuid,shortSideKey,attributes)
    addAircraftBT.make(addAircraftAction,sideGuid,shortSideKey,attributes)

    offensiveDoctrineConditionalBT.make(OffensiveConditionalCheck,sideGuid,shortSideKey,attributes)
    offensiveDoctrineSeletor.make(offensiveDoctrineSeletor.select,sideGuid,shortSideKey,attributes)

    attackDoctrineSelector.make(attackDoctrineSelector.select,sideGuid,shortSideKey,attributes)

    attackDoctrineUpdateAirMissionBT.make(attackMissionUpdateAction,sideGuid,shortSideKey,attributes)
    attackDoctrineCreateAirMissionBT.make(attackMissionCreateAction,sideGuid,shortSideKey,attributes)

    return merimackSelector

def updateAI(merimackSelector,mozi,env):
    return merimackSelector.run(mozi,env)


