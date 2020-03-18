#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main.py
# Create date : 2019-10-20 19:37
# Modified date : 2019-12-11 10:58
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################


from __future__ import division

import behaviorTree.etc as etc

from .env import MoziEnv

import behaviorTree.bt.detail as btDet
import behaviorTree.bt.basic as btBas

MAX_EPISODES = 5000
MAX_BUFFER = 1000000

MAX_TOTAL_REWARD = 300
env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
S_DIM = env.observation_dim
A_DIM = env.action_dim
A_MAX = env.action_max


def discritize(state_value, env_value):
    return int(1000 * (state_value - env_value)) / 10000.0


def run():
    '''
    运行函数
    入口 run
    '''
    if not env.connect_server():
        return False
    env.reset()

if __name__ == '__main__':
    '''
    入口函数
    '''
    run()
    scnr = env.mozi_service.load_scenario("linux")

    aa = env.mozi_service.mozi_task
    a1,a2 = aa.addAircarft('红方', 'AirCraft', 'f1', '6', '32.9', '45.4', '1558', '300', '3000.0')
    b1,b2 = aa.addAircarft('红方', 'AirCraft', 'f2', 6, 33., 45.2, 1558, 300, 4000.0)
   # aa.addAircarft('红方', 'AirCraft', 'f1', 6, 44.95, 32.77, 1558, 300, 3000)

    aaw = aa.getWeather()
    print(aaw)

    btDet.AddGUID(aa, 'aaaguid', '123-456-789')
    cc = btDet.GetGUID(aa, 'aaaguid')
    btDet.RemoveAllGUID(aa, 'aaaguid')
    btDet.AddGUID(aa, 'aaaguid', '123-456-789')
    btDet.AddGUID(aa, 'aaaguid', '434-3aa-111')
    btDet.AddGUID(aa, 'aaaguid', '555-4ff-234')
    btDet.RemoveGUID(aa, 'aaaguid', '434-3aa-111')
    cc = btDet.GetGUID(aa, 'aaaguid')
    print(cc)
    dd = btDet.GUIDExists(aa, 'aaaguid', '555-4ff-234')
    print(dd)
    dd = btDet.GUIDExists(aa, 'aaaguid', '555-4ff-233')
    print(dd)
    btDet.SetTimeStampForGUID(aa, 'aaatime')
    ee = btDet.GetTimeStampForGUID(aa, 'aaatime')
    print(ee)

    print(env.scenario)
    env.scenario.situation.init_situation(aa, env.scenario)

    '''
    运行客户端出现目标后
    '''
    ff=aa.getContacts('红方')
    print(ff)
    code, contact = aa.getContact('红方', ff[1]['guid'])
    print(contact.name)

    defaults=[btBas.MakeLatLong(0.,0.),btBas.MakeLatLong(0.,1.),btBas.MakeLatLong(1.,1.),btBas.MakeLatLong(1.,0.)]
    gg=btDet.FindBoundingBoxForGivenContacts(aa, '红方', ff, defaults, 10.)
    print(gg)

    '''
    客户端设置了任务strike1后
    '''
    code,mm=aa.getMission('红方','strike1')
    code2,mm2=aa.getMission('红方',mm.guid)
    mm3 = aa.getMissionUnitList('红方',mm.guid)

    aa.scenEdit_GetUnit()

    ss=env.mozi_service
    ss.set_run_mode()

    env.scenario
    env.scenario.situation
    env.scenario.situation.all_info_dict

    for k, v in env.scenario.situation.all_info_dict.items():
        print(k)

    for k, v in env.scenario.situation.all_info_dict.items():
        print(len(v))
        if len(v) > 20 :
            print(v)

    '''
    测试DetermineUnitRTB：加个机场，选择基地，执行返航
    '''
    codeHf,hf = aa.getSideInfo('红方')
    hf.contacts[1].name
    hf.units[0].name
    hfGuid = hf.units[0].guid

    rtrn = btDet.DetermineUnitRTB(aa,hfGuid)






