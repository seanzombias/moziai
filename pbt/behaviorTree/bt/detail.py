#!/usr/bin/python
# -*- coding: utf-8 -*-
# by aie

import behaviorTree.bt.basic as btBas

def GetGlobalConstant(mozi):
    globalConstant = mozi.getKeyValue("CONST_GLOBAL_VALUE")
    if globalConstant == "lua执行成功" :
        globalConstant = ""
    if globalConstant == "":
        globalConstant = "0"
    globalConstant = str(int(globalConstant) + 1)
    mozi.setKeyValue("CONST_GLOBAL_VALUE",globalConstant)
    return int(globalConstant)

def AddGUID(mozi,primaryKey,guid):
    guidString = mozi.getKeyValue(primaryKey)
    if guidString == "lua执行成功" :
        guidString == ""
    if guidString == "" :
        guidString = guid
    else:
        guidString = guidString+","+guid
    mozi.setKeyValue(primaryKey,guidString)


def GetGUID(mozi,primaryKey):
    guidString = mozi.getKeyValue(primaryKey)
    if guidString == "" :
        guidString = ""
    return guidString.split(",")

def RemoveAllGUID(mozi,primaryKey):
    mozi.setKeyValue(primaryKey,"")

def RemoveGUID(mozi,primaryKey,guid):
    table = GetGUID(mozi,primaryKey)
    guidString = None
    '''
    for k, v in table.items():
        if guid != v :
            if guidString is None:
                guidString = guidString+","+v
            else:
                guidString = v
    '''
    for v in table:
        if guid != v:
            if guidString is None:
                guidString = v
            else:
                guidString = guidString + "," + v
    mozi.setKeyValue(primaryKey,guidString)

def GUIDExists(mozi,primaryKey,guid):
    table = GetGUID(mozi,primaryKey)
    for v in table:
        if guid == v:
            return True
    return False

def SetTimeStampForGUID(mozi,primaryKey):
    time = mozi.getCurrentTime()
    mozi.setKeyValue(primaryKey,str(time))

def GetTimeStampForGUID(mozi,primaryKey):
    timeStamp = mozi.getKeyValue(primaryKey)
    if timeStamp=='lua执行成功':
        timeStamp=None
    '''
    if timeStamp == "" or timeStamp == None:
        mozi.setKeyValue(primaryKey,str(mozi.getCurrentTime()))
        timeStamp = mozi.getKeyValue(primaryKey)
    '''
    return float(timeStamp)


def FindBoundingBoxForGivenContacts(mozi,sideName,contacts,defaults,padding):
    #  Variables
    coordinates=[btBas.MakeLatLong(defaults[0]['latitude'], defaults[0]['longitude']),
     btBas.MakeLatLong(defaults[1]['latitude'], defaults[1]['longitude']),
     btBas.MakeLatLong(defaults[2]['latitude'], defaults[2]['longitude']),
     btBas.MakeLatLong(defaults[3]['latitude'], defaults[3]['longitude'])]
    contactBoundingBox = btBas.FindBoundingBoxForGivenLocations(coordinates,padding)
    contactCoordinates = []

    for k, v in contacts.items() :
        #contact = mozi.getContact(sideName, v['guid'])
        contact = mozi.getContactLatLon(sideName, v['guid'])
        contactCoordinates.append(btBas.MakeLatLong(contact['latitude'],contact['longitude']))
    
    # Get Hostile Contact Bounding Box
    if len(contactCoordinates) > 0 :
        contactBoundingBox = btBas.FindBoundingBoxForGivenLocations(contactCoordinates,padding)

    # Return Bounding Box
    return contactBoundingBox

def GetGroupLeadsAndIndividualsFromMission(mozi,sideName,missionName):
    codeM, mission = mozi.getMission(sideName,missionName)
    missionUnitList = mozi.getMissionUnitList(sideName,missionName)
    unitList = []
    #TODO: need to identify the group info and the leader .   by aie
    #unitKeyValue={}
    '''
    if mission :
        for k,v in mission.unitlist.items():
            codeU,unit = mozi.scenEdit_GetUnit(v)
            if unit.group:
                if unitKeyValue[unit.group.lead] == None:
                    unitList.append(unit.group.lead)
                    unitKeyValue[unit.group.lead] = ""
            else:
                if unitKeyValue[unit.guid] == None:
                    unitList.append(unit.guid)
                    unitKeyValue[unit.guid] = ""
    return unitList
    '''
    if mission :
        return missionUnitList
    else:
        return unitList

def DetermineRoleFromLoadOutDatabase(mozi,loudoutId,defaultRole):
    role = mozi.getKeyValue("lo_"+str(loudoutId))
    if role == None or role == "" :
        return defaultRole
    else:
        return role

def DetermineUnitRTB(mozi,unitGuid):
    code, unit = mozi.scenEdit_GetUnit(unitGuid)
    unitState = unit.getUnitState()
    if unit :
        return unitState.startswith("RTB")

'''
def DetermineThreatRangeByUnitDatabaseId(sideGuid,contactGuid)
    side = VP_GetSide({guid=sideGuid})
    contact = ScenEdit_GetContact({side=side.name, guid=contactGuid})		#得到具体目标信息。
    range = 0
    # Loop Through EM Matches And Get First
    for k,v in pairs(contact.potentialmatches) do								#这是要针对打开雷达的目标啊？
        foundRange = ScenEdit_GetKeyValue("thr_"..tostring(v.dbid))		#如：ct1=ScenEdit_GetContact({side='Red',
#		name='E-2C型"鹰眼"2000预警机 #1'})
#	  print(ct1.potentialmatches)
#输出：
#	{ [1] = { NAME = 'E-2C型"鹰眼"2000预警机',
 TYPE = AEW,
 SUBTYPE = 4002,
 CATEGORY = FixedWing_CarrierCapable,
 DBID = 694 } }
		#这里也可以看出，前面威胁库中单元的键号是其dbid.
        if foundRange ~= "" then
            range = tonumber(foundRange)
            break
        end
    end
    # If Range Is Zero Determine By Default Air Defence Values
    if range == 0 then
        # Create Exlusion Zone Based On Missile Defense
        if contact.missile_defence < 2 then				#目标的missile_defence决定了什么，对其建立禁航区的大小？
            range = 5
        elseif contact.missile_defence < 5 then
            range = 20
        elseif contact.missile_defence < 7 then
            range = 40
        elseif contact.missile_defence < 20 then
            range = 80
        else 
            range = 130
        end
    end
    # Return Range
    return range
end
'''

