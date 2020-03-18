#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : mozi_unit.py
# Create date : 2019-12-05 20:11
# Modified date : 2019-12-05 20:43
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pylog

def show_mozi_unit(item):
    pylog.info("strGuid:%s" % item["strGuid"])
    pylog.info("ClassName:%s" % item["ClassName"])
    pylog.info("strUnitClass:%s" % item["strUnitClass"])
    pylog.info("strName:%s" % item["strName"])

    pylog.info("strDamageState:%s" % item["strDamageState"])
    pylog.info("m_Bearing:%s" % item["m_Bearing"])
    pylog.info("dLongitude:%s" % item["dLongitude"])
    pylog.info("dLatitude:%s" % item["dLatitude"])
    pylog.info("fCurrentAlt:%s" % item["fCurrentAlt"])
    pylog.info("fPitch:%s" % item["fPitch"])
    pylog.info("fCurrentHeading:%s" % item["fCurrentHeading"])
    pylog.info("fCurrentSpeed:%s" % item["fCurrentSpeed"])
    pylog.info("m_LoadoutGuid:%s" % item.get("m_LoadoutGuid", ""))
    pylog.info("m_Mounts:%s" % item.get("m_Mounts",""))
    pylog.info("iDBID:%s" % item["iDBID"])
    pylog.info("iFuelRecsMaxQuantity:%s" % item.get("iFuelRecsMaxQuantity",""))
    pylog.info("fFuelConsumptionCruise:%s" % item.get("fFuelConsumptionCruise",""))
    pylog.info("dFuelPercentage:%s" % item.get("dFuelPercentage",""))
    pylog.info("strActiveUnitStatus:%s" % item["strActiveUnitStatus"])

#   fDesiredAlt:6.1
#   fMinSpeed:350.0
#   m_Side:c5d7ea87-30d9-42a1-8293-6e0e5b4d0048
#   m_HostActiveUnit:f7e66a7e-c638-4f91-a9bd-3c01aa5824b0
#   m_ParentGroup:a3863db5-83c6-477e-a701-a7e5b62220f4
#   bTerrainFollowing:False
#   fFuelConsumptionCruise:0.491059035
#   dPBComponentsLightDamageWidth:0.0
#   fDesiredSpeed:350.0
#   m_DockFacilitiesComponent:
#   iAltitude_ASL:3
#   bIsCommsOnLine:True
#   m_DockAircrafts:
#   fPitch:0.0
#   m_Mounts:3c13aceb-39ba-480e-8913-7a95380946fb@f59a31a2-c5be-41d2-8599-ca70174454da
#   strActiveUnitStatus:状态: 正在执行任务 (正在滑行准备起飞)
#   iDBID:1402
#   fAddForceSpeed:650.0
#   strDamageState:0
#   fCruiseSpeed:480.0
#   dLatitude:40.5879918260103
#   m_NoneMCMSensors:17214f4e-5e9d-4c67-a180-c35098f1a09f@0c782ddc-91de-4789-bc48-7bfb886891fa@1e5e5626-f129-4f29-b1f8-38539af8c75b@09187db8-62f9-48a3-bda2-7e8a353e24b8@b280a2d9-73fe-4355-9f50-a5d88d4f725f@0299ec7d-bf4d-448a-b7bc-48ffe60baa53@
#   strCommonIcon:110450011
#   m_Category:2001
#   strDockAircraft:0/0
#   m_WayPoints:
#   iCurrentFuelQuantity:4820
#   m_Doctrine:cbb3d9e4-91dc-4ea6-b0d8-051efecca727
#   m_DockedUnits:
#   m_AITargets:
#   strUnitClass:米格-29型“支点 C”战斗机
#   iFireIntensityLevel:0
#   m_Bearing:0.0
#   dLongitude:49.54091554449273
#   fLowSpeed:350.0
#   fCurrentAlt:9.1
#   iDisturbState:-1
#   bQuickTurnaround_Enabled:False
#   m_MaxThrottle:4
#   m_CommDevices:dabb3899-e47d-482e-afe4-c00b28272a90$UHF/VHF无线电[不安全]$0$0$7001@b7b2af04-0dc8-4add-8309-ea78356c6260$HF无线电[安全]$0$0$7001
#   strQuickTurnAroundInfo:-
#   fMinAltitude:0.0
#   bObeysEMCON:True
#   m_MaintenanceLevel:0
#   strFinishPrepareTime:0
#   bDesiredAltitudeOverride:False
#   fCurrentAltitude_ASL:3.0
#   bIsOperating:False
#   bHoldPosition:False
#   bIsIsolatedPOVObject:False
#   fMilitarySpeed:580.0
#   m_ShowTanker:
#   strGuid:638b2d99-850b-4a6c-bc18-2f6bc5098b3b
#   dPBComponentsHeavyDamageWidth:0.0
#   bIsEscortRole:False
#   fDesiredAltitude:6.1
#   bSprintAndDrift:False
#   dFuelPercentage:100.0
#   m_Cargo:
#   iFuelRecsMaxQuantity:4820
#   m_AirFacilitiesComponent:
#   dPBComponentsDestroyedWidth:0.0
#   strAirOpsConditionString:2
#   m_CurrentHostUnit:f7e66a7e-c638-4f91-a9bd-3c01aa5824b0
#   strFuelState:4820公斤总油量, 1小时 42分, 1107.496公里
#   备燃油

#   30分, 979.708公里
#   04 公里

#   iMultipleMissionCount:1
#   strName:米格-29战斗机(C空军基地) #02
#   fMaxAltitude:13716.0
#   fCurrentHeading:0.0
#   fAbnTime:0.0
#   strIconType:101210001
#   m_bBoomRefuelling:False
#   iFloodingIntensityLevel:0
#   m_LoadoutGuid:c9584c73-6db5-4b50-b460-414cd0c047a4
#   ClassName:CAircraft
#   m_UnitWeapons:6x 通用箔条 齐射 [5x 弹药桶]$564@10x 通用红外干扰弹 齐射 [3x 弹药桶, 单光谱]$560@5x 30毫米 Gsh-30-1型航空机炮$1796@2x AA-10型“杨树A”空空导弹[R-27R, MR 半主动雷达导引]$1901@4x R-73型“射手”空空导弹[北约代号：AA-11]$1896
#   fCurrentSpeed:350.0
#   fAltitude_AGL:6.1
#   m_ProficiencyLevel:2
#   bIsRegroupNeeded:False
#   m_CommLink:
#   m_CurrentThrottle:1
#   fRoll:0.0
#   strShowTankerHeader:
#   iLoadoutDBID:5357
#   dPBComponentsOKWidth:250.0
#   m_bProbeRefuelling:False
#   fHoverSpeed:0.0
#   dPBComponentsMediumDamageWidth:0.0
#   m_Type:2002
#   m_Engines:2651fdb5-cb1f-4703-8de2-9c4b044ce6f9$RD-33型涡轮风扇发动机 #1$0$0@67b08b86-3f45-4c85-9fb4-a846a39e9f0b$RD-33型涡轮风扇发动机 #2$0$0
#   m_AITargetsCanFiretheTargetByWCSAndWeaponQty:
#   bIsAirRefuelingCapable:False
#   m_AssignedMission:0ce4e41f-8426-4ab8-b563-f3bce5877869
#   m_BearingType:0
#   bAutoDetectable:False
#   bDesiredSpeedOverride:False
#   m_Distance:0.0
#   m_MultipleMissionGUIDs:0ce4e41f-8426-4ab8-b563-f3bce5877869
#   fMaxSpeed:650.0
#   m_Sensors:17214f4e-5e9d-4c67-a180-c35098f1a09f@0c782ddc-91de-4789-bc48-7bfb886891fa@1e5e5626-f129-4f29-b1f8-38539af8c75b@09187db8-62f9-48a3-bda2-7e8a353e24b8@b280a2d9-73fe-4355-9f50-a5d88d4f725f@0299ec7d-bf4d-448a-b7bc-48ffe60baa53

