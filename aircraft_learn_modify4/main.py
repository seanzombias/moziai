#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-03-10 11:05
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from __future__ import division

import numpy as np
import torch
from torch.autograd import Variable
import os
import gc
import time

from rlmodel.ddpg import train
from rlmodel.ddpg import buffer
from .env import MoziEnv
from . import pyfile
import pylog

from . import etc
from .pic import write_final_reward
from .pic import write_loss

from .pic import write_file
from .pic import read_file
from .pic import create_needed_folder
from .pic import get_start_epoch
from .pic import get_train_step

import pandas
import os
from . import pyfile

def write_destroy_loss_file(path, name, con):
    if pyfile.check_is_have_file(path, name):
        f = pyfile.open_file(path, name)
        f.write("%s\n" % con)
        f.close()
    else:
        f = pyfile.create_file(path, name)
        f.write("loss_num,destroy_num\n%s\n" % con)
        f.close()

def write_primary_file(con):
    path = etc.DESTROY_LOSS_RATE_PATH
    name = etc.PRIMARY_DESTROY_LOSS_RATE_FILE
    write_destroy_loss_file(path, name, con)

def write_learning_file(con):
    path = etc.DESTROY_LOSS_RATE_PATH
    name = etc.LEARNING_DESTROY_LOSS_RATE_FILE
    write_destroy_loss_file(path, name, con)

def run_primary(train_step, start_epoch, trainer, ram, env):

    loss_num_sum = 0
    destroy_num_sum = 0
    for _ep in range(int(start_epoch), etc.MAX_EPISODES):
        if not env.connect_server():
            pylog.info("can not connect to server")
            return False
        observation = env.reset()
        for step in range(etc.MAX_STEPS):
            new_observation, reward, done, info = env.step(None)

            if done:
                pylog.info("done from reward")
                break

        loss_num = len(env.red_unit_list) - env.last_red_aircraft_num
        loss_num_sum += loss_num

        destroy_num = len(env.blue_unit_list) - env.last_blue_aircraft_num
        destroy_num_sum += destroy_num

        write_primary_file("%s,%s"% (loss_num, destroy_num))

        pylog.info("loss_num_sum:%s destroy_num_sum:%s" % (loss_num_sum, destroy_num_sum))


def run(train_step, start_epoch, trainer, ram, env):

    loss_num_sum = 0
    destroy_num_sum = 0
    for _ep in range(int(start_epoch), etc.MAX_EPISODES):
        if not env.connect_server():
            pylog.info("can not connect to server")
            return False
        observation = env.reset()
        sum_reward = 0
        for step in range(etc.MAX_STEPS):
            #pylog.info("step:%s" % step)
            state = np.float32(observation)

            if _ep%5 == 0:
                action = trainer.get_exploitation_action(state)
            else:
                action = trainer.get_exploration_action(state)

            new_observation, reward, done, info = env.step(action)
            sum_reward += reward

            show_str = "EPISODE:%s step:%s observation:%s action:%s new_observation:%s reward:%s sum_reward:%s" % (_ep, step, observation, action, new_observation, reward, sum_reward)
            #pylog.info(show_str)

            if done:
                new_state = None
            else:
                new_state = np.float32(new_observation)
                ram.add(state, action, reward, new_state)

            if info:
                pylog.info(info)

            observation = new_observation
            trainer.optimize(train_step)
            train_step +=1
            write_file(train_step, "%s/step.txt" % etc.OUTPUT_PATH)
            if done:
                pylog.info("done from reward")
                break

        loss_num = len(env.red_unit_list) - env.last_red_aircraft_num
        loss_num_sum += loss_num

        destroy_num = len(env.blue_unit_list) - env.last_blue_aircraft_num
        destroy_num_sum += destroy_num

        write_learning_file("%s,%s"% (loss_num, destroy_num))

        pylog.info("loss_num_sum:%s destroy_num_sum:%s" % (loss_num_sum, destroy_num_sum))

        write_final_reward(sum_reward, _ep)
        gc.collect()
        if _ep % 5 == 0:
            trainer.save_model(_ep, etc.MODELS_PATH)
            write_file(_ep)


def get_ram():
    ram = buffer.MemoryBuffer(etc.MAX_BUFFER)
    return ram

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
    if not etc.PRIMARY_LOSS:
        run(train_step, start_epoch, trainer, ram, env)
    else:
        run_primary(train_step, start_epoch, trainer, ram, env)

main()
