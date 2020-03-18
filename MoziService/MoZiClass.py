#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Unit:
    def __init__(self):
        self.guid = ""
        self.name = ""


class ActiveUnit(Unit):
    def __init__(self):
        self.type = ""
        self.guid = ""
        self.subType = ""
        self.side = ""
        self.proficiency = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.heading = 0.0
        self.speed = 0
        self.throttle = ""
        self.autodetectable = False
        self.mounts = ""
        self.magazines = 0
        self.unitstate = 'Unassigned'
        self.fuelstate = 'None'
        self.weaponstate = 'None'
        self.destroy = 0

    def getGuid(self):
        return self.guid

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getSubType(self):
        return self.subType

    def getSide(self):
        return self.side

    def getSpeed(self):
        return self.speed

    def getProficiencyt(self):
        return self.proficiency

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getHeading(self):
        return self.heading

    def getThrottle(self):
        return self.throttle

    def getAutodetectable(self):
        return self.autodetectable

    def getMountsNumber(self):
        return self.mounts

    def getUnitState(self):
        return self.unitstate

    def getFuelState(self):
        return self.fuelstate

    def getWeaponState(self):
        return self.weaponstate


class Contact(Unit):
    def __init__(self):
        self.type = ""


class Side:
    def __init__(self):
        self.guid = ""
        self.name = ""
        self.units = []
        self.contacts = []

    class SideOption:
        def __init__(self):
            self.proficiency = ""
            self.side = ""
            self.awareness = ""
            self.guid = ""


class Mission():
    def __init__(self):
        self.guid = ""
        self.name = ""
        self.type = ""
        self.subType = ""
        self.isActive = True
        self.startTime = ""
        self.endTime = ""
        self.SISIH = False  # 鎺ㄦ紨鏂圭敱浜烘壆婕�
        self.aar = MissionTanker()  # 浠诲姟涓�┖绌哄姞娌归�椤圭殑鏁扮粍
        self.unitList = []


class MissionTanker():
    def __init__(self):
        self.Doctrine_UseReplenishment = ""
        self.MaxReceiversInQueuePerTanker_Airborne = 0
        self.TankerMaxDistance_Airborne = ""
        self.TankerUsage = ""
        self.FuelQtyToStartLookingForTanker_Airborne = 0


class ReferencePoint:
    def __init__(self):
        '''
        guid string 鍙傝�鐐圭殑 GUID
        side string 鍙��鍙傝�鐐圭殑闃佃惀
        name string 鍙傝�鐐瑰悕绉�
        latitude Latitude 鍙傝�鐐圭含搴�
        longitude Longitude 鍙傝�鐐圭粡搴�
        highlighted bool 鑻ュ弬鑰冪偣琚��鍒欏叾涓虹湡
        locked bool 鑻ュ弬鑰冪偣琚�攣鍒欏叾涓虹湡
        relativeto Unit 鍙傝�鐐圭浉鍏崇殑鍗曞厓
        bearingtype bearing 鎸囧悜绫诲瀷 Fixed (0) or Rotating (1)
        '''
        self.name = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.guid = ""
        self.side = None
        self.highlighted = False
        self.locked = False
        self.unit = None
        self.bearingtype = ""
