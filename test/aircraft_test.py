from MoziService import MoZiPython
from MoziService.entitys import aircraft

server_ip = '127.0.0.1'
server_port = 6260

# guid = 'c52ca175-d249-4c10-9f36-e7ea2a43ae56'
# name = 'S-3B型“海盗”反潜机'

# {name='F-14A型“雄猫”战斗机', guid='7383bffe-e88d-4edd-af4f-355cd61ff01e'}
# name='F-14A型“雄猫”战斗机'
# guid='7383bffe-e88d-4edd-af4f-355cd61ff01e'

#{name='单实体机场 (2x 3201-4000m 跑道)', guid='91c12e65-1362-4550-bd01-07d5dfdca6a4'}
# name='单实体机场 (2x 3201-4000m 跑道)'
# guid='91c12e65-1362-4550-bd01-07d5dfdca6a4'

# {name='F-14A型“雄猫”战斗机 #1', guid='c2e21ff5-53af-4bc3-aea4-9312a2295f38'}
name='F-14A型“雄猫”战斗机 #1'
guid='c2e21ff5-53af-4bc3-aea4-9312a2295f38'
side_name = '红方'
mozi_task = MoZiPython.MoZi(server_ip, server_port)
air = aircraft.Aircraft(guid, name, side_name, mozi_task)


def test_air_delete_sub_object():
    ret = air.air_delete_sub_object()
    print(ret)

def test_air_get_loadout_info():
    ret = air.air_get_loadout_info()
    print(ret)

def test_air_get_valid_weapons():
    ret = air.air_get_valid_weapons()
    print(ret)

def test_air_get_summary_info():
    ret = air.air_get_summary_info()
    print(ret)

def test_get_status_type():
    ret = air.get_status_type()
    print(ret)

def test_air_set_waypoint():
    side_name = air.side_name
    longitude = 22
    latitude = 30
    ret = air.air_set_waypoint(side_name, guid, longitude, latitude)
    print(ret)

def test_air_autoattack_target():
    target_guid = '12345'
    ret = air.air_autoattack_target(target_guid)
    print(ret)

def test_air_get_guid_from_name():
    target_name = '米格-29战斗机(C空军基地) #11'
    all_info_dict = {'3f11e3d4-9d82-4022-bad1-756488b428ce':{"ClassName":"CAircraft","strName":"米格-29战斗机(C空军基地) #11","strGuid":"3f11e3d4-9d82-4022-bad1-756488b428ce"},
                     "c6d649fe-809e-433f-a391-6ee367dccb0f":{"ClassName":"CSensor","strName":"L-203“栀子花”（Gardenya）电子战干扰机","strGuid":"c6d649fe-809e-433f-a391-6ee367dccb0f","iDBID":1962}}

    ret =air.air_get_guid_from_name(target_name, all_info_dict)
    print(ret)

def test_air_manual_pick_war():
    target_guid= '12345'
    weapon_dbid = 591
    weapon_num = 2
    ret = air.air_manual_pick_war(target_guid, weapon_dbid, weapon_num)
    print(ret)

def test_air_set_up_throttleI():
    ret = air.air_set_up_throttleI()
    print(ret)

def test_air_set_down_throttleI():
    ret = air.air_set_down_throttleI()
    print(ret)

def test_air_ops_singleout():
    base_guid = '123'
    ret = air.air_ops_singleout(base_guid)
    print(ret)

def test_air_set_rader_shutdown():
    turnoff = True
    ret = air.air_set_rader_shutdown(turnoff)
    print(ret)

def test_set_air_desired_height():
    desired_h = 1000
    ret = air.set_air_desired_height(desired_h)
    print(ret)

def test_air_return_to_base():
    ret = air.air_return_to_base()
    print(ret)

def test_air_plotted_course():
    course = [(40, 39.0), (41, 39.0)]
    ret = air.air_plotted_course(course)
    print(ret)

def test_air_deploy_dipping_sonar():
    ret = air.air_deploy_dipping_sonar()
    print(ret)

def test_air_assign_unitList_to_missionEscort():
    mission_name ='aas'
    ret = air.air_assign_unitList_to_missionEscort(mission_name)
    print(ret)

def test_air_drop_active_sonobuoy():
    sideName = side_name
    deepOrShallow = 'deep'
    ret = air.air_drop_active_sonobuoy(sideName, deepOrShallow)
    print(ret)

def test_air_drop_passive_sonobuoy():
    sideName = side_name
    deepOrShallow = 'deep'
    ret = air.air_drop_passive_sonobuoy(sideName, deepOrShallow)
    print(ret)

def test_setAirborneTime():

    unitNameOrId = name
    hour = '01'
    minute =' 01'
    second ='01'
    ret = air.setAirborneTime(unitNameOrId, hour, minute, second)
    print(ret)

def test_timeToReady():
    time = '00:00:05'
    ret =air.timeToReady(time)
    print(ret)


def test():
    # test_air_delete_sub_object()
    # test_air_get_loadout_info()
    # test_air_get_valid_weapons()  # 未知
    # test_air_get_summary_info()
    # test_get_status_type()
    # test_air_set_waypoint()
    # test_air_autoattack_target()
    # test_air_get_guid_from_name()
    # test_air_manual_pick_war()
    # test_air_set_up_throttleI()
    # test_air_set_down_throttleI
    # test_air_ops_singleout()
    # test_air_set_rader_shutdown()
    # test_air_return_to_base()
    # test_air_plotted_course()
    # test_air_deploy_dipping_sonar()
    # test_air_assign_unitList_to_missionEscort()
    # test_air_drop_active_sonobuoy()
    # test_air_drop_passive_sonobuoy()
    # test_setAirborneTime()
    test_timeToReady()



test()


# 脚本执行出错
"""
air_manual_pick_war
air_ops_singleout
air_return_to_base
air_deploy_dipping_sonar

setAirborneTime   想定有问题？ 
timeToReady  飞机在机场内设置，怎么能拿到每一架飞机的guid   
"""
