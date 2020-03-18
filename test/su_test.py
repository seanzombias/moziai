from MoziService import MoZiPython
from MoziService.entitys import submarine

server_ip = '127.0.0.1'
server_port = 6260

# {name='建筑结构(海军码头，船坞)', guid='ce315651-6ef8-401a-8c42-3b716f5abbb3'}
# 蓝方{name='“刀鱼”无人潜航器', guid='1dddd8f8-15cb-4db6-8188-bb2870d5f641'}
# {name='SS-501苍龙级潜艇', guid='dbf2d4b8-c880-4f16-8337-e05a3e1b3a22'}
name='SS-501苍龙级潜艇'
guid='dbf2d4b8-c880-4f16-8337-e05a3e1b3a22'
side_name = '红方'
mozi_task = MoZiPython.MoZi(server_ip, server_port)
sub = submarine.Csubmarine(guid, name, side_name, mozi_task)


def test_subm_manual_pick_war():
    target_guid= '1dddd8f8-15cb-4db6-8188-bb2870d5f641'
    weapon_dbid= 230
    weapon_num = 3
    ret = sub.subm_manual_pick_war(target_guid ,weapon_dbid ,weapon_num)
    print(ret)

def test_subm_attack_auto():
    contact_guid = '123'
    ret = sub.subm_attack_auto(contact_guid)
    print(ret)

def test_subm_set_up_throttleI():
    ret = sub.subm_set_up_throttleI()
    print(ret)

def test_subm_set_down_throttleI():
    ret = sub.subm_set_down_throttleI()
    print(ret)

def test_subm_ops_singleout():
    base_guid='ce315651-6ef8-401a-8c42-3b716f5abbb3'
    ret = sub.ssubm_ops_singleout(base_guid)
    print(ret)

def test_subm_set_rader_shutdown():
    trunoff = False
    ret = sub.subm_set_rader_shutdown(trunoff)
    print(ret)

def test_subm_set_sonar_shutdown():
    trunoff = False
    ret = sub.subm_set_sonar_shutdown(trunoff)
    print(ret)

def test_subm_set_OECM_shutdown():
    trunoff = True
    ret = sub.subm_set_OECM_shutdown(trunoff)
    print(ret)

def test_subm_set_desired_height():
    height= 100
    ret = sub.subm_set_desired_height(height)
    print(ret)

def test_subm_return_to_base():

    ret = sub.subm_return_to_base()
    print(ret)

def test_subm_plotted_course():

    course = [(40, 39.0), (41, 39.0)]
    ret = sub.subm_plotted_course(course)
    print(ret)

def test_subm_drop_active_sonobuoy():
    sideName=side_name
    deepOrShallow = 'deep'
    ret = sub.subm_drop_active_sonobuoy(sideName, deepOrShallow)
    print(ret)

def test_subm_drop_passive_sonobuoy():
    sideName=side_name
    deepOrShallow = 'deep'
    ret = sub.subm_drop_passive_sonobuoy(sideName, deepOrShallow)
    print(ret)






def test():
    # test_subm_manual_pick_war()
    # test_subm_attack_auto()
    # test_subm_set_up_throttleI()
    # test_subm_set_down_throttleI()
    # test_subm_ops_singleout()
    # test_subm_set_rader_shutdown()
    # test_subm_set_sonar_shutdown()
    # test_subm_set_OECM_shutdown()
    # test_subm_set_desired_height()
    # test_subm_return_to_base()
    # test_subm_plotted_course()
    # test_subm_drop_active_sonobuoy()
    test_subm_drop_passive_sonobuoy()
test()