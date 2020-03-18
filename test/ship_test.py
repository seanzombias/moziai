from MoziService import MoZiPython
from MoziService.entitys import ship

server_ip = '127.0.0.1'
server_port = 6260

# {name='DDG 72 “马汉号”阿里伯克级 Flight II驱逐舰 ', guid='1ea9c0fa-5eac-4315-b2ce-7fdba383d1da'}
name='DDG 72 “马汉号”阿里伯克级 Flight II驱逐舰 '
guid='1ea9c0fa-5eac-4315-b2ce-7fdba383d1da'

side_name = '红方'
mozi_task = MoZiPython.MoZi(server_ip, server_port)
ship = ship.CShip(guid, name, side_name, mozi_task)

def test_ship_manual_pick_war():
    target_guid = '12345'
    weapon_dbid = 3
    weapon_num = 10
    ret = ship.ship_manual_pick_war(target_guid, weapon_dbid, weapon_num)
    print(ret)

def test_ship_set_up_throttleI():

    ret = ship.ship_set_up_throttleI()
    print(ret)

def test_ship_set_down_throttleI():
    ret = ship.ship_set_down_throttleI()
    print(ret)

def test_ship_ops_singleout():
    base_guid= '123a'
    ret = ship.ship_ops_singleout(base_guid)
    print(ret)

def test_ship_set_rader_shutdown():
    trunoff = True
    ret = ship.ship_set_rader_shutdown(trunoff)
    print(ret)

def test_ship_set_sonar_shutdown():
    trunoff = True
    ret = ship.ship_set_sonar_shutdown(trunoff)
    print(ret)

def test_set_OECM_shutdown():
    trunoff = True
    ret = ship.set_OECM_shutdown(trunoff)
    print(ret)

def test_ship_set_desired_height():
    trunoff = 100
    ret = ship.ship_set_desired_height(trunoff)
    print(ret)

def test_ship_return_to_base():

    ret = ship.ship_return_to_base()
    print(ret)

def test_ship_plotted_course():
    course = [(30,18), (30, 19)]
    ret = ship.ship_plotted_course(course)
    print(ret)

def test_ship_drop_active_sonobuoy():
    sideName = side_name
    deepOrShallow = 'deep'
    ret = ship.ship_drop_active_sonobuoy(sideName, deepOrShallow)
    print(ret)

def test_ship_drop_passive_sonobuoy():
    sideName = side_name
    deepOrShallow = 'deep'
    ret = ship.ship_drop_passive_sonobuoy(sideName, deepOrShallow)
    print(ret)

def test_ship_attack_auto():
    course = '123'
    ret = ship.ship_attack_auto(course)
    print(ret)


def test():
    # test_ship_manual_pick_war()
    # test_ship_set_up_throttleI()
    # test_ship_set_down_throttleI()
    # test_ship_ops_singleout()  # 不能获取船坞内潜艇的guid
    # test_ship_set_rader_shutdown()
    # test_ship_set_sonar_shutdown()
    # test_set_OECM_shutdown()
    # test_ship_set_desired_height()
    # test_ship_return_to_base()
    # test_ship_plotted_course()
    # test_ship_drop_active_sonobuoy()
    # test_ship_drop_passive_sonobuoy()
    test_ship_attack_auto()


test()

# 返回数据错误
test_ship_plotted_course