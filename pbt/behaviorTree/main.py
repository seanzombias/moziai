#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-01-09 19:22
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from __future__ import division

import numpy as np
import gc

# from rlmodel.ddpg import train
# from rlmodel.ddpg import buffer
from .env import MoziEnv
import pylog

from . import etc
from .pic import write_final_reward
from .pic import write_loss

from .pic import write_file
from .pic import read_file
from .pic import create_needed_folder
from .pic import get_start_epoch
from .pic import get_train_step

from MoziService import MoZiPython
from .test.test01 import *
from .bt.ctrltree import *
import random
import time

def run(train_step, start_epoch, trainer, ram, env):
    for _ep in range(int(start_epoch), etc.MAX_EPISODES):
        if not env.connect_server():
            pylog.info("can not connect to server")
            return False
        observation = env.reset()
        sum_reward = 0
        for step in range(etc.MAX_STEPS):
            state = np.float32(observation)

            if _ep % 5 == 0:
                action = trainer.get_exploitation_action(state)
            else:
                action = trainer.get_exploration_action(state)

            new_observation, reward, done, info = env.step(action)
            sum_reward += reward

            show_str = "EPISODE:%s step:%s observation:%s action:%s new_observation:%s reward:%s sum_reward:%s" % (
                _ep, step, observation, action, new_observation, reward, sum_reward)
            pylog.info(show_str)

            if done:
                new_state = None
            else:
                new_state = np.float32(new_observation)
                ram.add(state, action, reward, new_state)

            if info:
                pylog.info(info)

            observation = new_observation
            trainer.optimize(train_step)
            train_step += 1
            write_file(train_step, "%s/step.txt" % etc.OUTPUT_PATH)
            if done:
                break

        write_final_reward(sum_reward, _ep)
        gc.collect()
        if _ep % 5 == 0:
            trainer.save_model(_ep, etc.MODELS_PATH)
            write_file(_ep)


def get_ram():
    ram = buffer.MemoryBuffer(etc.MAX_BUFFER)
    return ram

'''
def main():
    create_needed_folder()

    env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
    S_DIM = env.observation_space
    A_DIM = env.action_space
    A_MAX = env.action_max

    start_epoch = get_start_epoch()
    train_step = get_train_step()
    ram = get_ram()

    trainer = train.Trainer(S_DIM, A_DIM, A_MAX, ram, etc.device, write_loss, int(start_epoch), etc.MODELS_PATH)
    run(train_step, start_epoch, trainer, ram, env)
'''
def main():
    '''
    #jkjkjkl
    '''
    env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
    if not env.connect_mozi_server(etc.SERVER_IP, etc.SERVER_PORT):
        return False
    observation = env.reset()
    state = np.float32(observation)
    #mozi = env.mozi_service
    mozi = MoZiPython.MoZi(etc.SERVER_IP, etc.SERVER_PORT)

    '''
        测试添加飞机
    '''
    #plane01,plane02 = testAddAC(mozi)

    #weather = testGetWeather(mozi)

    #btguid,btstamp = testOperateBtGUID(mozi)

    #env.scenario.situation.init_situation(mozi, env.scenario)

    '''
        运行客户端出现目标后
    '''
    #btctctsBox = testContactsBox(env,mozi)

    '''
        客户端设置了任务strike1后
    '''
    #btmssunit = testMission(mozi)

    '''
        测试DetermineUnitRTB：加个机场，选择基地，执行返航
    '''
    #btrtb = testRTB(mozi)

    '''
        测试行为树    
    '''
    #testBT()

    '''
        测试推演方信息获取
    '''
    #rn = env.red_side_name
    #cs, rs = mozi.getSideInfo(rn)
    #ropts = mozi.getSideOptions(rn)

    '''
            测试墨子行为树案例
    '''
    #mozi.sendAndRecv("ScenEdit_DeleteUnit({side='a',guid='47a0620b-f3b5-45c2-b516-c55f82f25255'})")
    env.mozi_service.run_simulate()
    stop = 0
    t01 = eval(mozi.getCurrentTime())
    merimackSelector = initializeMerimackMonitorAI(env, '红方', 0, '')
    while (stop == 0) :
        env.mozi_service.suspend_simulate()
        env.scenario.situation.update_situation(env.mozi_service,env.scenario)
        ###############
        result = updateAI(merimackSelector,mozi,env)
        ################
        t02 = eval(mozi.getCurrentTime())
        if (t02-t01)/3600 > 1 :
            stop = 1
        else:
            print('---'+str(random.random())+'---')
            print((t02-t01)/60)
            env.mozi_service.run_simulate()
            time.sleep(3)

    testEnd()





main()
