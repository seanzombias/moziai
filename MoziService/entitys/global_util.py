# -*- coding:utf-8 -*-

from enum import Enum


class OperationError(Exception):
    pass


class ElementType(Enum):
    """
    元素类型
    """
    # 推演方
    Side = 0
    # 打击任务
    StrikeMission = 11
    # 巡逻任务
    PatrolMission = 12
    # 支援任务
    SupportMission = 13
    # 编队
    Group = 20
    # 飞机
    Aircraft = 31
    # 设施
    Facility = 32
    # 舰船
    Ship = 33
    # 潜艇
    Submarine = 34
    # 卫星
    Satellite = 35
    # 传感器
    Sensor = 41
    # 武器
    Weapon = 42
    # 挂架
    Mount = 43
    # 飞机挂载
    Loadout = 44
    # 条令
    Doctrine = 45
    # 弹药库
    Magazine = 46
    # 航路点
    WayPoint = 47
    # 发现的非本方单元
    Contact = 61
    # 想定
    Scenario = 62
    # 推演
    Simulation = 63
    # 天气
    Weather = 64
    # 参考点
    ReferencePoint = 65
    # 空
    Empty = 66
    # 触发器--时间
    TriggerTime = 101
    # 触发器--实体损伤
    TriggerUnitDamaged = 102
    # 触发器--实体被摧毁
    TriggerUnitDestroyed = 103
    # 动作--终止推演
    ActionEndScenario = 151
    # 动作--得分
    ActionPoints = 152
    # 动作--消息
    ActionMessage = 153
    # 推演事件
    SimEvent = 199
    # 反馈
    Response = 201
    # 反馈消息
    LoggedMessage = 202
    # 删除
    Delete = 399


classname2element = {
    "CCurrentScenario": ElementType.Scenario,
    "CSimulation": ElementType.Simulation,
    "CSide": ElementType.Side,
    "CStrikeMission": ElementType.StrikeMission,
    "CPatrolMission": ElementType.PatrolMission,
    "CSupportMission": ElementType.SupportMission,
    "CGroup": ElementType.Group,
    "CAircraft": ElementType.Aircraft,
    "CFacility": ElementType.Facility,
    "CShip": ElementType.Ship,
    "CSubmarine": ElementType.Submarine,
    "CSatellite": ElementType.Satellite,
    "CMount": ElementType.Mount,
    "CWeapon": ElementType.Weapon,
    "CSensor": ElementType.Sensor,
    "CLoadout": ElementType.Loadout,
    "CMagazine": ElementType.Magazine,
    "CWayPoint": ElementType.WayPoint,
    "CDoctrine": ElementType.Doctrine,
    "CReferencePoint": ElementType.ReferencePoint,
    "CTriggerTime": ElementType.TriggerTime,
    "CTriggerUnitDamaged": ElementType.TriggerUnitDamaged,
    "CTriggerUnitDestroyed": ElementType.TriggerUnitDestroyed,
    "CActionEndScenario": ElementType.ActionEndScenario,
    "CActionMessage": ElementType.ActionMessage,
    "CActionPoints": ElementType.ActionPoints,
    "CSimEvent": ElementType.SimEvent,
    "CContact": ElementType.Contact,
    "CWeather": ElementType.Weather,
    "CResponse": ElementType.Response,
    "Delete": ElementType.Delete,
    "Empty": ElementType.Empty,
}


class SelectorCategory(Enum):
    """
    选择的元素类别, 可设置条令
    """
    # 推演方
    Side = 0
    # 任务
    Mission = 1
    # 编队
    Group = 2
    # 作战单元（飞机，导弹车等，不包含传感器、武器等作战单元的组件）
    Unit = 3
    # 武器
    Weapon = 4
    # 航路点
    WayPoint = 5


selector2str = {
    SelectorCategory.Side: 'side',
    SelectorCategory.Mission: 'mission',
    SelectorCategory.Group: 'group',
    SelectorCategory.Unit: 'unit',
    SelectorCategory.Weapon: 'weapon',
    SelectorCategory.WayPoint: 'WayPoint'
}


class MissionCategory(Enum):
    """
    任务类别
    """
    # 打击
    ATTACK = 0
    # 巡逻
    PATROL = 1
    # 支援
    SUPPORT = 2
    # 转场
    TRANSFOR = 3
    # 布雷
    MINE = 4
    # 扫雷
    SWEEP = 5
    # 投送
    DELIVER = 6


class MissionPatrolType(Enum):
    # 空空巡逻
    AIR = 6011
    ANTI_SHIP = 6012
    ANTI_LAND = 6013
    ANTI_MLP = 6014
    ANTI_SUBMARINE = 6015
    SEAD = 6016
    SEA_CONTROL = 6017


class MissionStrikeType(Enum):
    AIR = 6001
    LAND = 6002
    SHIP = 6003
    SUBMARINE = 6004


mission_patrol_type_dict = {
    MissionPatrolType.AIR: "AAW",
    MissionPatrolType.ANTI_SHIP: "SUR_SEA",
    MissionPatrolType.ANTI_LAND: "SUR_LAND",
    MissionPatrolType.ANTI_MLP: "SUR_MIXED",
    MissionPatrolType.ANTI_SUBMARINE: "SUB",
    MissionPatrolType.SEAD: "SEAD",
    MissionPatrolType.SEA_CONTROL: "SEA"
}

mission_strike_type_dict = {
    MissionStrikeType.AIR: "AIR",
    MissionStrikeType.LAND: "LAND",
    MissionStrikeType.SHIP: "SEA",
    MissionStrikeType.SUBMARINE: "SUB"
}


class ContactType(Enum):
    # 空中目标
    Air = 0
    # 导弹
    Missile = 1
    # 水面 / 地面
    Surface = 2
    # 潜艇
    Submarine = 3
    # 未确定的海军
    UndeterminedNaval = 4
    # 瞄准点？？
    Aimpoint = 5
    # 轨道目标
    Orbital = 6
    # 固定设施
    Facility_Fixed = 7
    # 移动设施
    Facility_Mobile = 8
    # 鱼雷
    Torpedo = 9
    # 水雷
    Mine = 10
    # 爆炸
    Explosion = 11
    # 不确定
    Undetermined = 12
    # 空中诱饵
    Decoy_Air = 13
    # 表面诱饵
    Decoy_Surface = 14
    # 陆地诱饵
    Decoy_Land = 15
    # 水下诱饵
    Decoy_Sub = 16
    # 声纳浮标
    Sonobuoy = 17
    # 军事设施
    Installation = 18
    # 空军基地
    AirBase = 19
    # 海军基地
    NavalBase = 20
    # 移动集群
    MobileGroup = 21
    # 激活点：瞄准点
    ActivationPoint = 22


class DoctrineItem(Enum):
    Nukes = 7002
    Nukes_Player = 7003
    WCS_Air = 7004
    WCS_Air_Player = 7005
    WCS_Surface = 7006
    WCS_Surface_Player = 7007
    WCS_Submarine = 7008
    WCS_Submarine_Player = 7009
    WCS_Land = 7010
    WCS_Player_Land = 7011
    IPCWA = 7012
    IPCWA_Player = 7013
    WinchesterShotgunRTB = 7014
    WinchesterShotgunRTB_Player = 7015
    BingoJokerRTB = 7016
    BingoJokerRTB_Player = 7017
    JettisonOrdnance = 7018
    JettisonOrdnance_Player = 7019
    BTAT = 7020
    BTAT_Player = 7021
    AE = 7022
    AE_Player = 7023
    MS = 7024
    MS_Player = 7025
    GS = 7026
    GS_Player = 7027
    UR = 7028
    UR_Player = 7029
    RS = 7030
    RS_Player = 7031
    ST = 7032
    ST_Player = 7033
    SAM_ASUW = 7034
    SAM_ASUW_Player = 7035
    E_Radar = 7036
    E_Sonar = 7037
    E_OECM = 7038
    QuickTurnAround = 7039
    QTA_Player = 7040
    AirOpsTempo = 7041
    AirOpsTempo_Player = 7042
    BingoJoker = 7043
    BingoJoker_Player = 7044
    WinchesterShotgun = 7045
    WinchesterShotgun_Player = 7046
    WithdrawDamageThreshold = 7047
    WithdrawFuelThreshold = 7048
    WithdrawAttackThreshold = 7049
    WithdrawDefenceThreshold = 7050
    RedeployDamageThreshold = 7051
    RedeployFuelThreshold = 7052
    RedeployAttackThreshold = 7053
    RedeployDefenceThreshold = 7054
    IgnoreEMCONUnderAttack = 7055
    IgnoreEMCONUnderAttack_Player = 7056
    UseTorpedoesKinematicRange = 7057
    UseTorpedoesKinematicRange_Player = 7058
    RefuelAllies = 7059
    RefuelAllies_Player = 7060
    AvoidContact = 7061
    AvoidContact_Player = 7062
    DiveWhenThreatsDetected = 7063
    DiveWhenThreatsDetected_Player = 7064
    RechargePercentagePatrol = 7065
    RechargePercentagePatrol_Player = 7066
    RechargePercentageAttack = 7067
    RechargePercentageAttack_Player = 7068
    AIPUsage = 7069
    AIPUsage_Player = 7070
    DippingSonar = 7071
    DippingSonar_Player = 7072
    WRA = 7073


class HeightCategory(Enum):
    """
    实体高度
    """
    Minimun = 0
    Low = 1
    Semi_Low = 2
    Medium = 3
    Semi_High = 4
    High = 5
    Maximun = 6


class Throttle(Enum):
    """
    实体油门
    """
    # 不确定
    Unspecified = 0
    # 停住
    Fullstop = 1
    # 低速
    Loiter = 2
    # 巡航
    Cruise = 3
    # 全速
    Full = 4
    # 加力
    Flank = 5


throttle_description = {
    Throttle.Unspecified: "Unspecified",
    Throttle.Fullstop: "FullStop",
    Throttle.Loiter: "Loiter",
    Throttle.Cruise: "Cruise",
    Throttle.Full: "Full",
    Throttle.Flank: "Flank"
}


class FlightSize(Enum):
    """
    编队规模
    """
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Six = 5


class StrikeMinAircraftReq(Enum):
    """
    启动任务所需最少就绪飞机数
    """
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    SIX = 6
    EIGHT = 8
    TWELVE = 12
    ALL = 13


class StrikeMinimumTrigger(Enum):
    """
    打击任务触发条件
    """
    Nil = 1
    NotFriendly = 2
    Hostile = 3
    Unknown = 4


class StrikeRadarUasge(Enum):
    """
    任务雷达运用规则
    """
    ALL_PLAN = 1
    START_WINCHESTER = 2
    ATTACK_START_WINCHESTER = 3


class UseNuclear(Enum):
    """
    使用核武器
    """
    Dont_Use_Nuclear_Weapons = 0
    Use_Nuclear_Weapons = 1
    Inherit = 999


class StrikeFuleAmmo(Enum):
    """
    燃油弹药规则
    """
    MOUNT_SET = 0
    FAR_DIST = 1
    CARRY_BACK = 2


class BehaviorTowardsAmbigousTarget(Enum):
    """
    接战模糊位置目标
    """
    # 忽略
    Ignore = 0
    # 乐观
    Optimistic = 1
    # 悲观
    Pessimistic = 2
    # 继承，和上级一致
    Inherit = 999


class EngageWithContactTarget(Enum):
    """
    接战临机出现目标
    """
    # 否 只与任务相关目标交战
    No_Only = 0
    # 否 只与任务相关目标交战
    Yes_AnyTarget = 1
    # 继承，和上级一致
    Inherit = 999


class WeaponControlStatus(Enum):
    """
    武器控制状态
    """
    # 自由开火
    Free = 0
    # 谨慎开火
    Tight = 1
    # 限制开火
    Hold = 2
    # 和上级一致
    Inherit = 999


class QuickTurnAround(Enum):
    """
    快速出动
    """
    Yes = 0
    Yes_FighterAndASWLoadoutOnly = 1
    No = 2
    Inherit = 999


class AirOpsTempo(Enum):
    """
    空战节奏
    """
    # 一般强度出动
    Sustained = 0
    # 快速出动
    Surge = 1
    # 和上级一致
    Inherit = 999


class FuelState(Enum):
    """
    燃油状态
    """
    Bingo = 0
    Joker10Percent = 1
    Joker20Percent = 2
    Joker25Percent = 3
    Joker30Percent = 4
    Joker40Percent = 5
    Joker50Percent = 6
    Joker60Percent = 7
    Joker70Percent = 8
    Joker75Percent = 9
    Joker80Percent = 10
    Joker90Percent = 11
    Inherit = 999


class UseTorpedoesKinematicRange(Enum):
    """
    鱼雷使用动力航程
    """
    KinematicRangeWhenAutomaticOrManualLaunch = 0
    KinematicRangeOnlyManualLaunch = 1
    PraticalRange = 2
    Inherit = 999


class RefuelSelection(Enum):
    """
    对所选单元进行加油/补给
    """
    ClosestTanker = 0
    TankerLocateBetweenMeAndTarget = 1
    TankerLocateBetweenMeAndTarget_CantReturnBack = 2
    Inherit = 999


class UseSAMsInASuWMode(Enum):
    """
    反舰模式使用舰空导弹
    """
    No = 0
    Yes = 1
    Inherit = 999


class IgnoreEMCONUnderAttack(Enum):
    """
    受到攻击时忽略电磁管控
    """
    No = 0
    Ignore_EMCON_While_Under_Attack = 1
    Inherit = 999


class AutomaticEvasion(Enum):
    """
    自动规避
    """
    No = 0
    Yes = 1
    Inherit = 999


class MaintainStandoff(Enum):
    """
    与目标保持距离
    """
    No = 0
    Yes = 1
    Inherit = 999


class GunStrafeGroundTargets(Enum):
    """
    空对地扫射
    """
    No = 0
    Yes = 1
    Inherit = 999


class IgnorePlottedCourseWhenAttacking(Enum):
    """
    受到攻击时忽略计划航线
    """
    No = 0
    Yes = 1
    Inherit = 999


class WeaponStatePlanned(Enum):
    """
    武器状态，预先规划
    """
    # 没有值：
    NoneValue = 1001
    # 使用挂载设置：
    LoadSet = 0
    # 任务武器已耗光，立即脱离战斗：
    WinchesterDisengage = 2001
    # 任务武器已耗光.允许使用航炮对临机目标进行打击（推荐）：
    WinchesterUseAirGuns = 2002
    # 所有超视距与防区外打击武器已经耗光.立即脱离战斗：
    ShotgunBVRExpendedDisengage = 3001
    # 所有超视距与防区外打击武器已经耗光.允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击.不使用航炮：
    ShotgunBVRExpendedNoGuns = 3002
    # 所有超视距与防区外打击武器已经耗光.允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击：
    ShotgunBVRExpendedGuns = 3003
    # 25 % 相关武器已经耗光.立即脱离战斗
    Shotgun25Disengage = 4001
    # 25%相关武器已经耗光. 允许与临机出现目标交战，包括航炮
    Shotgun25Airguns = 4002
    # 50%相关武器已经耗光. 立即脱离战斗
    Shotgun50Disengage = 4011
    # 50%相关武器已经耗光. 允许与临机出现目标交战，包括航炮
    Shotgun50Airguns = 4012
    # 75%相关武器已经耗光. 立即脱离战斗
    Shotgun75Disengage = 4021
    # 75%相关武器已经耗光. 允许与临机出现目标交战，包括航炮
    Shotgun75Airguns = 4022
    # 使用超视距或防区外打击武器进行一次交战.立即脱离战斗
    ShotgunOneEngageOutDisengage = 5001
    # 使用超视距或防区外打击武器进行一次交战.允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击.不使用航炮
    ShotgunOneEngageNoAirguns = 5002
    # 使用超视距或防区外打击武器进行一次交战.允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击
    ShotgunOneEngageInAirguns = 5003
    # 同时使用超视距 / 视距内或防区外 / 防区内打击武器进行一次交战.不使用航炮
    ShotgunOneEngageStrikeNoAirguns = 5005
    # 同时使用超视距 / 视距内或防区外 / 防区内打击武器进行一次交战.允许使用航炮对较易攻击的临机出现目标进行攻击
    ShotgunOneEngageOutStrikeAirguns = 5006
    # 使用视距内或防区内打击武器进行一次交战.立即脱离战斗
    ShotgunOneEngageInDisengage = 5011
    # 使用视距内或防区内打击武器进行一次交战. 允许使用航炮与临机出现目标格斗
    ShotgunOneEngageInStrikeAirguns = 5012
    # 使用航炮进行一次交战
    ShotgunOneEngageAirguns = 5021
    # 和上级一致
    Inherit = 999


class WeaponStateRTB(Enum):
    """
    武器状态-返航
    """
    No = 0
    YesLastUnit = 1
    YesFirstUnit = 2
    YesLeaveGroup = 3
    Inherit = 999


class FuelStateRTB(Enum):
    """
    燃油状态-返航
    """
    No = 0
    YesLastUnit = 1
    YesFirstUnit = 2
    YesLeaveGroup = 3
    Inherit = 999


class JettisonOrdnance(Enum):
    """
    抛弃弹药
    """
    No = 0
    Yes = 1
    Inherit = 999


class RefuelAlliedUnits(Enum):
    """
    对盟军单元进行加油
    """
    Yes = 0
    Yes_ReceiveOnly = 1
    Yes_DeliverOnly = 2
    No = 3
    Inherit = 999


class AvoidContactWhenPossible(Enum):
    """
    规避搜索
    """
    No = 0
    Yes_ExceptSelfDefence = 1
    Yes_Always = 2
    Inherit = 999


class DiveOnContact(Enum):
    """
    探测到威胁进行下潜
    """
    Yes = 0
    Yes_ESM_Only = 1
    Yes_Ships20nm_Aircraft30nm = 2
    No = 3
    Inherit = 999


class UseAIP(Enum):
    """
    使用API技术
    """
    No = 0
    Yes_AttackOnly = 1
    Yes_Always = 2
    Inherit = 999


class UseDippingSonar(Enum):
    """
    调放声呐
    """
    Automatically_HoverAnd150ft = 0
    ManualAndMissionOnly = 1
    Inherit = 999


class DamageThreshold(Enum):
    """
    毁伤程度小于，则重新部署
    """
    Ignore = 0
    Percent5 = 1
    Percent25 = 2
    Percent50 = 3
    Percent75 = 4
    Inherit = 999


class FuelQuantityThreshold(Enum):
    """
    燃油状态重新部署
    """
    Ignore = 0
    Bingo = 1
    Percent25 = 2
    Percent50 = 3
    Percent75 = 4
    Percent100 = 5
    Inherit = 999


class WeaponQuantityThreshold(Enum):
    """
    武器状态重新部署
    """
    Ignore = 0
    Exhausted = 1
    Percent25 = 2
    Percent50 = 3
    Percent75 = 4
    Percent100 = 5
    LoadFullWeapons = 6
    Inherit = 999


class EMCON_SettingsMode(Enum):
    """
    电磁管控设置
    """
    Passive = 0
    Active = 1
    Inherit = 999


class WRA_WeaponTargetType(Enum):
    """
    武器打击目标代码
    """
    # None
    NoneValue = 1001
    # decoy
    Decoy = 1002
    # Air Contact - Unknown Type
    Air_Contact_Unknown_Type = 1999
    # Aircraft - Unspecified
    Aircraft_Unspecified = 2000
    # Aircraft - 5th Generation Fighter/Attack [Agility/Gen: 5.0+] (F-22, Eurofighter, Rafale)
    Aircraft_5th_Generation = 2001
    # Aircraft - 4th Generation Fighter/Attack [Agility/Gen: 4.0-4.9] (F-14, F-15, F-16, MiG-29, Su-27)
    Aircraft_4th_Generation = 2002
    # Aircraft - 3rd Generation Fighter/Attack [Agility/Gen: 3.0-3.9] (F-4, F-5, MiG-21, MiG-23)
    Aircraft_3rd_Generation = 2003
    # Aircraft - Less Capable Fighter/Attack [Agility: 2.0-2.9] (F-111, Lightning, Su-7, MiG-17)
    Aircraft_Less_Capable = 2004
    # Aircraft - High-performance Bombers [Agility: 2.0+] (B-1B, B-2A, Tu-22M
    Aircraft_High_Perf_Bombers = 2011
    # Aircraft - Medium-performance Bombers [Agility: 1.5-1.9] (B-52, Vulcan, Tu-16)
    Aircraft_Medium_Perf_Bombers = 2012
    # Aircraft - Low-performance Bombers [Agility: 1.0-1.4] (B-24, Canberra, Tu-95, Bison)
    Aircraft_Low_Perf_Bombers = 2013
    # Aircraft - High-Performance Reconnaissance and Electronic Warfare [Agility: 4.0+]
    Aircraft_High_Perf_Recon_EW = 2021
    # Aircraft - Medium-Performance Reconnaissance and Electronic Warfare [Agility: 3.0-3.9]
    Aircraft_Medium_Perf_Recon_EW = 2022
    # Aircraft - Low-Performance Reconnaissance and Electronic Warfare [Agility: 2.0-2.9]
    Aircraft_Low_Perf_Recon_EW = 2023
    # Aircraft - Airborne Early Warning and Control
    Aircraft_AEW = 2031
    # Helicopter - Unspecified
    Helicopter_Unspecified = 2100
    # Guided Weapon - Unspecified
    Guided_Weapon_Unspecified = 2200
    # Guided Weapon - Supersonic Sea-Skimming
    Guided_Weapon_Supersonic_Sea_Skimming = 2201
    # Guided Weapon - Subsonic Sea-Skimming
    Guided_Weapon_Subsonic_Sea_Skimming = 2202
    # Guided Weapon - Supersonic
    Guided_Weapon_Supersonic = 2203
    # Guided Weapon - Subsonic
    Guided_Weapon_Subsonic = 2204
    # Guided Weapon - Ballistic
    Guided_Weapon_Ballistic = 2211
    # Satellite - Unspecified
    Satellite_Unspecified = 2300
    # Surface Contact - Unknown Type
    Surface_Contact_Unknown_Type = 2999
    # Ship - Unspecified
    Ship_Unspecified = 3000
    # Ship - Carrier, 0-25000 tons
    Ship_Carrier_0_25000_tons = 3001
    # Ship - Carrier, 25001-45000 tons
    Ship_Carrier_25001_45000_tons = 3002
    # Ship - Carrier, 45001-95000 tons
    Ship_Carrier_45001_95000_tons = 3003
    # Ship - Carrier, 95000+ tons
    Ship_Carrier_95000_tons = 3004
    # Ship - Surface Combatant, 0-500 tons
    Ship_Surface_Combatant_0_500_tons = 3101
    # Ship - Surface Combatant, 501-1500 tons, plus Missile Boats with smaller displacement
    Ship_Surface_Combatant_501_1500_tons = 3102
    # Ship - Surface Combatant, 1501-5000 tons, plus Frigates and Corvettes with smaller displacement
    Ship_Surface_Combatant_1501_5000_tons = 3103
    # Ship - Surface Combatant, 5001-10000 tons, plus Destroyers with smaller displacement
    Ship_Surface_Combatant_5001_10000_tons = 3104
    # Ship - Surface Combatant, 10001-25000 tons, plus Cruisers with smaller displacement
    Ship_Surface_Combatant_10001_25000_tons = 3105
    # Ship - Surface Combatant, 25001-45000 tons
    Ship_Surface_Combatant_25001_45000_tons = 3106
    # Ship - Surface Combatant, 45001-95000 tons
    Ship_Surface_Combatant_45001_95000_tons = 3107
    # Ship - Surface Combatant, 95000+ tons
    Ship_Surface_Combatant_95000_tons = 3108
    # Ship - Amphibious, 0-500 tons
    Ship_Amphibious_0_500_tons = 3201
    # Ship - Amphibious, 501-1500 tons
    Ship_Amphibious_501_1500_tons = 3202
    # Ship - Amphibious, 1501-5000 tons
    Ship_Amphibious_1501_5000_tons = 3203
    # Ship - Amphibious, 5001-10000 tons
    Ship_Amphibious_5001_10000_tons = 3204
    # Ship - Amphibious, 10001-25000 tons
    Ship_Amphibious_10001_25000_tons = 3205
    # Ship - Amphibious, 25001-45000 tons
    Ship_Amphibious_25001_45000_tons = 3206
    # Ship - Amphibious, 45001-95000 tons
    Ship_Amphibious_45001_95000_tons = 3207
    # Ship - Amphibious, 95000+ tons
    Ship_Amphibious_95000_tons = 3208
    # Ship - Auxiliary, 0-500 tons
    Ship_Auxiliary_0_500_tons = 3301
    # Ship - Auxiliary, 501-1500 tons
    Ship_Auxiliary_501_1500_tons = 3302
    # Ship - Auxiliary, 1501-5000 tons
    Ship_Auxiliary_1501_5000_tons = 3303
    # Ship - Auxiliary, 5001-10000 tons
    Ship_Auxiliary_5001_10000_tons = 3304
    # Ship - Auxiliary, 10001-25000 tons
    Ship_Auxiliary_10001_25000_tons = 3305
    # Ship - Auxiliary, 25001-45000 tons
    Ship_Auxiliary_25001_45000_tons = 3306
    # Ship - Auxiliary, 45001-95000 tons
    Ship_Auxiliary_45001_95000_tons = 3307
    # Ship - Auxiliary, 95000+ tons
    Ship_Auxiliary_95000_tons = 3308
    # Ship - Merchant / Civilian, 0-500 tons
    Ship_Merchant_Civilian_0_500_tons = 3401
    # Ship - Merchant / Civilian, 501-1500 tons
    Ship_Merchant_Civilian_501_1500_tons = 3402
    # Ship - Merchant / Civilian, 1501-5000 tons
    Ship_Merchant_Civilian_1501_5000_tons = 3403
    # Ship - Merchant / Civilian, 5001-10000 tons
    Ship_Merchant_Civilian_5001_10000_tons = 3404
    # Ship - Merchant / Civilian, 10001-25000 tons
    Ship_Merchant_Civilian_10001_25000_tons = 3405
    # Ship - Merchant / Civilian, 25001-45000 tons
    Ship_Merchant_Civilian_25001_45000_tons = 3406
    # Ship - Merchant / Civilian, 45001-95000 tons
    Ship_Merchant_Civilian_45001_95000_tons = 3407
    # Ship - Merchant / Civilian, 95000+ tons
    Ship_Merchant_Civilian_95000_tons = 3408
    # Ship - Surfaced Submarine
    Submarine_Surfaced = 3501
    # Sub-Surface Contact - Unknown Type
    Subsurface_Contact_Unknown_Type = 3999
    # Submarine - Unspecified
    Submarine_Unspecified = 4000
    # Land Contact - Unknown Type
    Land_Contact_Unknown_Type = 4999
    # Land Structure - Soft - Unspecified
    Land_Structure_Soft_Unspecified = 5000
    # Land Structure - Soft - Building (Surface)
    Land_Structure_Soft_Building_Surface = 5001
    # Land Structure - Soft - Building (Reveted)
    Land_Structure_Soft_Building_Reveted = 5002
    # Land Structure - Soft - Structure (Open)
    Land_Structure_Soft_Structure_Open = 5005
    # Land Structure - Soft - Structure (Reveted)
    Land_Structure_Soft_Structure_Reveted = 5006
    # Land Structure - Soft - Aerostat Moring
    Land_Structure_Soft_Aerostat_Moring = 5011
    # Land Structure - Hardened - Unspecified
    Land_Structure_Hardened_Unspecified = 5100
    # Land Structure - Hardened - Building (Surface)
    Land_Structure_Hardened_Building_Surface = 5101
    # Land Structure - Hardened - Building (Reveted)
    Land_Structure_Hardened_Building_Reveted = 5102
    # Land Structure - Hardened - Building (Bunker)
    Land_Structure_Hardened_Building_Bunker = 5103
    # Land Structure - Hardened - Building (Underground)
    Land_Structure_Hardened_Building_Underground = 5104
    # Land Structure - Hardened - Structure (Open)
    Land_Structure_Hardened_Structure_Open = 5105
    # Land Structure - Hardened - Structure (Reveted)
    Land_Structure_Hardened_Structure_Reveted = 5106
    # Runway Facility - Unspecified
    Runway_Facility_Unspecified = 5200
    # Runway
    Runway = 5201
    # Runway-Grade Taxiway
    Runway_Grade_Taxiway = 5202
    # Runway Access Point
    Runway_Access_Point = 5203
    # Radar - Unspecified
    Radar_Unspecified = 5300
    # Mobile Target - Soft - Unspecified
    Mobile_Target_Soft_Unspecified = 5400
    # Mobile Target - Soft - Mobile Vehicle(s)
    Mobile_Target_Soft_Mobile_Vehicle = 5401
    # Mobile Target - Soft - Mobile Personnel
    Mobile_Target_Soft_Mobile_Personnel = 5402
    # Mobile Target - Hardened - Unspecified
    Mobile_Target_Hardened_Unspecified = 5500
    # Mobile Target - Hardened - Mobile Vehicle(s)
    Mobile_Target_Hardened_Mobile_Vehicle = 5501
    # Underwater Structure
    Underwater_Structure = 5601
    # Air Base (Single-Unit Airfield)
    Air_Base_Single_Unit_Airfield = 5801


class WRAWeaponQty(Enum):
    """
    齐射武器数
    """
    # 不使用
    NotUse = 0
    # 系统缺省 或 未配置
    Default = -99
    # 导弹防御值的1/4
    MissileDefence25Percent = -6
    MissileDefence50Percent = -5
    MissileDefence400Percent = -4
    MissileDefence200Percent = -3
    # 导弹防御值
    MissileDefence = -2
    Rnd1 = 1
    Rnds2 = 2
    Rnds3 = 3
    Rnds4 = 4
    Rnds5 = 5
    Rnds6 = 6
    Rnds7 = 7
    Rnds8 = 8
    Rnd10 = 10
    Rnds12 = 12
    Rnds14 = 14
    Rnds16 = 16
    Rnds18 = 18
    Rnds20 = 20
    Rnds22 = 22
    Rnds24 = 24
    Rnds26 = 26
    Rnds28 = 28
    Rnds30 = 30
    AllWeapon = 99
    Inherit = 999


class WRAShooterQty(Enum):
    """
    武器发射架数
    """
    # 系统缺省 或 未配置
    Default = -99
    # 开火的作战单元数满足武器的齐射要求数
    FellowWeaponQty = -1
    # 一个作战单元
    One = 1
    # 两个作战单元
    Two = 2
    # 四个作战单元
    Four = 4
    # 与上级一致
    Inherit = 999


class WRASelfAttackRange(Enum):
    """
    自动开火距离
    """
    # 系统缺省 或 未配置
    Default = -99
    # 最大射程
    MaximumRange = 99
    # 不自动开火
    NoUseWeaponDefence = 0
    TwoNm = 2
    FiveNm = 5
    TenNm = 10
    FifteenNm = 15
    TwentyNm = 20
    TwentyFiveNm = 25
    # 30海里
    ThirtyNm = 30
    ThirtyFiveNm = 35
    FortyNm = 40
    FortyFiveNm = 45
    FiftyNm = 50
    SixtyNm = 60
    SeventyNm = 70
    EightyNm = 80
    NinetyNm = 90
    # 100海里
    OneHundred = 100
    OneHundred25 = 125
    OneHundred50 = 150
    OneHundred70 = 170
    TwoHundred = 200
    # 250海里
    TwoHundred50 = 250
    ThreeHundred = 300
    FiveHundred = 500
    SevenHundred50 = 750
    # 1000海里
    OneThousand = 1000
    OneThonsand500 = 1500
    TwoThonsand = 2000
    Inherit = 999


class WRASelfDefenceRange(Enum):
    """
    武器自防御距离
    """
    # 系统缺省 或 未配置
    Default = -99
    # 最大防御距离
    MaximumRange = -9
    # 武器不用自防御
    NoUseWeaponDefence = 0
    # 1海里
    OneNm = 1
    # 2海里
    TwoNm = 2
    ThreeNm = 3
    FourNm = 4
    FiveNm = 5
    SixNm = 6
    SevenNm = 7
    EightNm = 8
    NineNm = 9
    TenNm = 10
    FifteenNm = 15
    Inherit = 999


class WayPointType(Enum):
    """
    航路点类型
    """
    ManualPlottedCourseWaypoint = 0
    PatrolStation = 1


waypointtype2str = {
    0: "ManualPlottedCourseWaypoint",
    1: "PatrolStation",
    2: "WeaponTerminalPoint",
    3: "LocalizationRun",
    4: "PathfindingPoint",
    5: "Assemble",
    6: "TurningPoint",
    7: "InitialPoint",
    8: "Split",
    9: "Formate",
    10: "Target",
    11: "LandingMarshal",
    12: "StrikeIngress",
    13: "StrikeEgress",
    14: "Refuel",
    11: "TakeOff",
    12: "Marshal",
    13: "WeaponLaunch",
    14: "Land",
    11: "WeaponTarget",
    12: "TrackPoint",
    13: "RoadFinder",
    14: "SetRoute"
}


# aircraft
class BearingType(Enum):
    # 固定的，不随领队朝向变化而变化
    Fixed = 0
    # 旋转的，随领队朝向改变旋转
    Rotating = 1


class AircraftCategory(Enum):
    # 未知
    NoneValue = 1001
    # 固定翼
    FixedWing = 2001
    # 固定翼舰载机
    FixedWing_CarrierCapable = 2002
    # 直升机
    Helicopter = 2003
    # 倾转旋翼机
    Tiltrotor = 2004
    const_5 = 2005
    # 飞艇
    Airship = 2006
    # 水上飞机
    Seaplane = 2007
    # 两栖飞机
    Amphibian = 2008


class AircraftType(Enum):
    # 其他
    NoneValue = 1001
    # 战斗机
    Fighter = 2001
    # 多用途飞机
    Multirole = 2002
    # 反卫星飞机
    ASAT = 2101
    # 空中激光平台
    AirborneLaserPlatform = 2102
    # 攻击机
    Attack = 3001
    # 野鼬鼠 （防空压制）
    WildWeasel = 3002
    # 轰炸机
    Bomber = 3101
    # 战场空中拦截（BAI/ CAS）
    CAS = 3401
    # 电子战飞机
    OECM = 4001
    # 预警机
    AEW = 4002
    # 指挥机 （ACP）
    AirborneCP = 4003
    # 救援飞机
    SAR = 4101
    # 反水雷飞机
    MCM = 4201
    # 反潜作战飞机
    ASW = 6001
    # 海上巡逻机
    MPA = 6002
    # 前进观察员
    ForwardObserver = 7001
    # 区域监视
    AreaSurveillance = 7002
    # 侦察机
    Recon = 7003
    # 电子情报收集飞机
    ELINT = 7004
    # 信号情报收集飞机
    SIGINT = 7005
    # 运输机
    Transport = 7101
    # 货机
    Cargo = 7201
    # 商业飞机
    Commercial = 7301
    # 民用
    Civilian = 7302
    # 通用直升机
    Utility = 7401
    # 海军通用直升机
    Utility_Naval = 7402
    # 空中加油机
    Tanker = 8001
    # 教练机
    Trainer = 8101
    # 牵引机
    TargetTowing = 8102
    # 靶机
    TargetDrone = 8103
    # 无人机
    UAV = 8201
    # 无人作战飞行器
    UCAV = 8202
    # 飞艇
    AirShip = 8901
    # 航空器
    Aerostat = 8902
    IMGSAT = 9001
    RORSAT = 9002
    EORSAT = 9003


class AirOpsCondition(Enum):
    # 空中
    Airborne = 0
    # 停泊
    Parked = 1
    # 正在滑行准备起飞
    TaxyingToTakeOff = 2
    # 正在滑行到停机位
    TaxyingToPark = 3
    # 正在起飞过程中
    TakingOff = 4
    # 最终进场
    Landing_PreTouchdown = 5
    # 正在完成降落
    Landing_PostTouchdown = 6
    # 正在进行出动准备
    Readying = 7
    # 等待可用的滑行道/升降机
    HoldingForAvailableTransit = 8
    # 等待跑道空闲
    HoldingForAvailableRunway = 9
    # 处于降落队列中
    HoldingOnLandingQueue = 10
    # 返回基地
    RTB = 11
    # 准备出动
    PreparingToLaunch = 12
    # 机动到加油阵位
    ManoeuveringToRefuel = 13
    # 正在加油
    Refuelling = 14
    # 卸载燃油
    OffloadingFuel = 15
    # 准备部署吊放式声纳，尚未到达部署点
    DeployingDippingSonar = 16
    # 紧急着陆
    EmergencyLanding = 17
    # 到飞行甲板
    TaxyingToFlightDeck = 18
    # 正在执行超视距攻击任务
    BVRAttack = 19
    # 超视距攻击往复运动？远距离攻击往复运动？
    BVRCrank = 20
    # 近距空中格斗
    Dogfight = 21
    # 投送货物
    DeployingCargo = 22
    # 滑行至加油区
    TaxiToRefuelingArea = 23
    # 滑行
    Taxiing = 24
    # 通过跑道滑行降落（用于演示功能）
    TaxiToLanding = 25
    # 通过跑道滑行起飞（用于演示功能）
    TaxiToTakeOff = 26


class AirValidStatus(Enum):
    validToFly = 0
    InAir = 1
    InAirRTB = 2
    WaitReady = 3


class MaintenanceLevel(Enum):
    # 可用，准备就绪
    const_0 = 0
    # 武器状态已知，且考虑连发机关枪
    const_1 = 1
    # 不可用
    Unavailable = 2
    # 备用挂载方案？
    ReserveLoadout = 3
    # 没有挂载方案
    const_4 = 4


class IdentificationStatus(Enum):
    # 未知
    Unknown = 0
    # 已知空域（如空中、地面）
    KnownDomain = 1
    # 已知类型（如飞机、导弹）
    KnownType = 2
    # 已知级别
    KnownClass = 3
    # 确认对象
    PreciseID = 4


# ficility
class FicilityCategory(Enum):
    NoneValue = 1001
    # 跑道
    Runway = 2001
    # 滑行道
    RunwayGrade_Taxiway = 2002
    # 跑道入口
    RunwayAccessPoint = 2003
    # 建筑物（地表）
    Building_Surface = 3001
    # 建筑物（混凝土）
    Building_Reveted = 3002
    # 建筑物（地堡）
    Building_Bunker = 3003
    # 建筑物（地下）
    Building_Underground = 3004
    # 建筑结构（开放）
    Structure_Open = 3005
    # 建筑结构（混凝土）
    Structure_Reveted = 3006
    # 水下
    Underwater = 4001
    # 移动车辆
    Mobile_Vehicle = 5001
    # 移动人员
    Mobile_Personnel = 5002
    # 航空器系泊设备
    AerostatMooring = 6001
    # 空军基地
    AirBase = 9001


class FacilityType(Enum):
    # 陆军分队
    LandForce = 5001
    # 火箭军导弹分队
    MissileForce = 5002
    # 地防导弹分队
    LandAntiAir = 5003
    # 雷达分队
    RadarForce = 5004
    # 空军基地
    AirBase = 9001


# group
class GroupType(Enum):
    # 飞机编组，或此枚举还要充当没有成员变量的枚举
    AirGroup = 0
    # 水面舰艇编组
    SurfaceGroup = 1
    # 潜艇编组
    SubGroup = 2
    # 设施编组
    Installation = 3
    # 车辆编组
    MobileGroup = 4
    # 空军基地
    AirBase = 5
    # 海军基地
    NavalBase = 6


# loadout
class CargoType(Enum):
    # 不可以编辑货物
    NoCargo = 0
    # 人员
    Personnel = 1000
    # 小型货物
    SmallCargo = 2000
    # 中型货物
    MediumCargo = 3000
    # 大型货物
    LargeCargo = 4000
    # 超大型货物
    VeryLargeCargo = 5000


# loggenMessage
class MessageType(Enum):
    # 其他
    NoneValue = 0
    # 发现新目标
    NewContact = 1
    # 目标状态变更
    ContactChange = 2
    # 武器末段计算
    WeaponEndgame = 3
    # 武器毁伤
    WeaponDamage = 4
    # 空中行动
    AirOps = 5
    # 作战单元损失
    UnitLost = 6
    # 作战单元毁伤
    UnitDamage = 7
    # 点防御
    PointDefence = 8
    # 用户界面
    UI = 9
    # 武器逻辑
    WeaponLogic = 10
    # 作战单元AI
    UnitAI = 11
    # 事件引擎
    EventEngine = 13
    # 新武器感知
    NewWeaponContact = 14
    # 停靠行动
    DockingOps = 15
    # 特殊消息
    SpecialMessage = 16
    # 发现新鱼雷目标
    NewMineContact = 17
    # 通信隔离消息
    CommsIsolatedMessage = 18
    # 发现新空中目标
    NewAirContact = 19
    # 发现新水面目标
    NewSurfaceContact = 20
    # 发现新水下目标
    NewUnderwaterContact = 21
    # 发现新地面目标
    NewGroundContact = 22
    # 非制导武器精度修正
    UnguidedWeaponModifiers = 23
    # 武器发射
    WeaponFiring = 24
    # 输出弹框内容
    InputMessage = 25


# Magazine
class ComponentStatus(Enum):
    # 正常工作
    Operational = 0
    # 受到毁伤
    Damaged = 1
    # 已被摧毁
    Destroyed = 2


class DamageSeverity(Enum):
    # 轻
    Light = 0
    # 中
    Medium = 1
    # 重
    Heavy = 2


# Mission
class MissionClass(Enum):
    # 未知
    NoneValue = 0
    # 打击/截击
    Strike = 1
    # 巡逻
    Patrol = 2
    # 支援
    Support = 3
    # 转场
    Ferry = 4
    # 布雷
    Mining = 5
    # 扫雷
    MineClearing = 6
    # 护航
    Escort = 7
    # 投送选项
    Cargo = 8


class FlightSizeNum(Enum):
    # 无，对应于没有编队大小限制
    NoneValue = 0
    # 单机
    SingleAircraft = 1
    # 2机编队
    TwoAircraft = 2
    # 3机编队
    ThreeAircraft = 3
    # 4机编队
    FourAircraft = 4
    # 6机编队
    SixAircraft = 6


# side
class ProficiencyLevel(Enum):
    # 新手
    Novice = 0
    # 实习
    Cadet = 1
    # 普通
    Regular = 2
    # 老手
    Veteran = 3
    # 顶级
    Ace = 4


class AwarenessLevel(Enum):
    # 一无所知
    Blind = -1
    # 普通水平
    Normal = 0
    # 知其属方
    AutoSideID = 1
    # 知其属方及单元
    AutoSideAndUnitID = 2
    # 无所不知
    Omniscient = 3


# strikeMission
class StrikeMissionType(Enum):
    # 空中截击
    Air_Intercept = 0
    # 对陆打击
    Land_Strike = 1
    # 对海打击
    Maritime_Strike = 2
    # 对潜突击
    Sub_Strike = 3


class MinimumContactStanceToTrigger(Enum):
    #  中立
    Neutral = 0
    #  友方
    Friendly = 1
    # 不友好
    Unfriendly = 2
    # 敌对
    Hostile = 3
    #  未知
    Unknown = 4


class Bingo(Enum):
    # 根据每个挂载方案的设置决定是消耗/抛弃还是带回空地弹药
    const_0 = 0
    # 在最远距离上抛弃空对地弹药，以获取最大打击
    const_1 = 1
    # 如果不能打击目标，则带回空对地弹药
    BringBackIfTargetCanntStrike = 2


class RadarBehaviour(Enum):
    # 整个飞行计划全部使用任务电磁管控
    const_0 = 0
    # 从初始点到武器消耗光打开雷达：winchester
    Land = 1
    # 从攻击进入点到武器消耗光打开雷达
    const_2 = 2
    # 默认，缺省
    Maritime = 3


class UseRefuel(Enum):
    # 允许，不允许加油机对加油机加油
    Yes_ExcepTankerToTanker = 0
    # 不允许
    No = 1
    # 允许
    Yes = 2
    # 多样
    Various = 3
    # 未配置
    NotConfigured = 4


class TankerUsage(Enum):
    # 自动使用
    Automatic = 0
    # 任务中使用
    Mission = 1


class GroupSize(Enum):
    # 无
    NoneValue = 0
    # 单舰
    Single = 1
    # 双舰
    Double = 2
    # 三舰
    Three = 3
    # 四舰
    Four = 4
    # 六舰
    Six = 6


class EscortFlightSize(Enum):
    # 无，对应于没有编队大小限制
    NoneValue = 0
    # 单机
    SingleAircraft = 1
    # 2机编队
    TwoAircraft = 2
    # 3机编队
    ThreeAircraft = 3
    # 4机编队
    FourAircraft = 4
    # 6机编队
    SixAircraft = 6


class AircraftToFlyGroupSize(Enum):
    # 所有飞机编队出动
    All = -99
    # 无偏好
    NoPreferences = 0
    # 一机编队
    Flight_x1 = -97
    Flight_x2 = -96
    Flight_x3 = -95
    Flight_x4 = -94
    Flight_x6 = -93
    Flight_x8 = -92
    Flight_x12 = -91
    Aircraft_x1 = -87
    Aircraft_x2 = -86
    Aircraft_x3 = -85
    Aircraft_x4 = -84
    Aircraft_x6 = -83
    Aircraft_x8 = -82
    Aircraft_x12 = -81


class EscortGroupSize(Enum):
    # 无
    NoneValue = 0
    # 单舰
    Single = 1
    # 双舰
    Double = 2
    # 三舰
    Three = 3
    # 四舰
    Four = 4
    # 六舰
    Six = 6


# unit
class FireIntensityLevel(Enum):
    # 无火
    NoFire = 0
    # 小火
    Minor = 1
    # 中火
    Major = 2
    # 猛火
    Severe = 3
    # 大火
    Conflagration = 4


class FloodingIntensityLevel(Enum):
    # 未进水
    NoFlooding = 0
    # 少量
    Minor = 1
    # 中等
    Major = 2
    # 严重
    Severe = 3
    # 翻覆
    Capsizing = 4
