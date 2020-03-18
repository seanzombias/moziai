from MoziService import MoZiPython
from MoziService.entitys import facility

server_ip = '127.0.0.1'
server_port = 6260

guid = '0ec5c4b7-7304-422a-a857-0d8f54f5fb5b'
name = '坦克排(M1A2 SEP 艾布拉姆斯 MBT x4主战坦克)'

side_name = '红方'
mozi_task = MoZiPython.MoZi(server_ip, server_port)
tank1 = facility.Facility(guid, name, side_name, mozi_task)


def _test_fac_get_summary_info():
    ret = tank1.fac_get_summary_info()
    print(ret)


def _test_fac_attack_auto():  # 想想怎么用super()
    target_guid = '123456'

    ret = tank1.fac_attack_auto(target_guid)
    print(ret)

def _test_fac_set_up_throttleI():
    tank1.m_CurrentThrottle = 1
    ret = tank1.fac_set_up_throttleI()
    print(ret)

def _test_fac_set_down_throttleI():
    tank1.m_CurrentThrottle = 0
    ret = tank1.fac_set_down_throttleI()
    print(ret)

def test_fac_set_rader_shutdown():

    ret = tank1.fac_set_rader_shutdown()
    print(ret)

def test_fac_set_OECM_shutdown():

    ret = tank1.fac_set_OECM_shutdown('ture')
    print(ret)

def test_fac_set_desired_speed():
    ret = tank1.fac_set_desired_speed(100)
    print(ret)

def test_fac_set_desired_hight():
    ret = tank1.fac_set_desired_height(1000)
    print(ret)

def test_fac_set_unit_heading():
    ret = tank1.fac_set_unit_heading(100)
    print(ret)

def test_fac_plotted_course():
    ret = tank1.fac_plotted_course([(40, 39.0), (41, 39.0)])
    print(ret)

def test_fac_delete_coursed_point():
    ret = tank1.fac_delete_coursed_point([0, 1])
    print(ret)  # none

def test_fac_assign_unitList_to_mission():
    ret = tank1.fac_assign_unitList_to_mission('AAW')
    print(ret)

def test_fac_manual_pick_war():
    target_guid = 'b9d010af-7504-45b6-8211-42a30bc492bc'
    weapon_dbid = 10
    weapon_num = 2

    ret = tank1.fac_manual_pick_war(target_guid, weapon_dbid, weapon_num)
    print(ret)

def test_fac_all_ocate_salvo_to_target():
    target = 'b9d010af-7504-45b6-8211-42a30bc492bc'
    weaponDBID = 10
    ret = tank1.fac_all_ocate_salvo_to_target(target, weaponDBID)
    print(ret)

def test_fac_unit_obeys_EMCON():
    ret = tank1.fac_unit_obeys_EMCON(True)
    print(ret)


def test():
    # _test_fac_get_summary_info()
    # _test_fac_attack_auto()
    # _test_fac_set_up_throttleI()
    # _test_fac_set_down_throttleI()
    # test_fac_set_rader_shutdown()
    # test_fac_set_OECM_shutdown()
    # test_fac_set_desired_speed()
    # test_fac_set_desired_hight()
    # test_fac_set_unit_heading()
    # test_fac_plotted_course()
    test_fac_delete_coursed_point()
    # test_fac_assign_unitList_to_mission()
    # test_fac_manual_pick_war()
    # test_fac_all_ocate_salvo_to_target()
    # test_fac_unit_obeys_EMCON()

test()

# lua 函数可能有问题
# fac_delete_coursed_point
# fac_manual_pick_war
# fac_unit_obeys_EMCON