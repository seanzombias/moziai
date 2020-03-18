#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : pic.py
# Create date : 2019-10-15 20:31
# Modified date : 2020-01-09 18:08
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

import matplotlib.pyplot as plt

import numpy as np
from . import etc

import os
from . import pyfile
from . import pylog


def create_needed_folder():
    pyfile.create_dir(etc.CMD_LUA)
    pyfile.create_dir(etc.PATH_CSV)
    pyfile.create_dir(etc.MODELS_PATH)


def get_start_epoch():
    start_epoch = read_file()
    pylog.info("start epochs:%s" % start_epoch)
    return start_epoch


def get_train_step():
    start_step = read_file("%s/step.txt" % etc.OUTPUT_PATH)
    train_step = int(start_step)
    return train_step


def write_file(epochs, file_path="%s/ep.txt" % etc.OUTPUT_PATH):
    '''
    打开文件
    mytest
    '''
    f = open(file_path, "w")
    f.write("%s" % epochs)
    f.close()


def read_file(file_path="%s/ep.txt" % etc.OUTPUT_PATH):
    '''
    打开文件
    '''

    if not os.path.exists(file_path):
        return '0'

    f = open(file_path, "r")
    ret = f.read()
    f.close()
    if not ret:
        return '0'
    return ret


def write_final_reward(reward, epochs):
    file_path = "%s/final_reward.txt" % etc.OUTPUT_PATH
    if not os.path.exists(file_path):
        f = open(file_path, "w")
    else:
        f = open(file_path, "a")
    f.write("%s,%s\n" % (epochs, reward))
    f.close()


def write_loss(step, loss_value, loss_name="loss_critic"):
    pyfile.create_dir(etc.OUTPUT_PATH)
    file_path = "%s/%s.txt" % (etc.OUTPUT_PATH, loss_name)
    if not os.path.exists(file_path):
        f = open(file_path, "w")
    else:
        f = open(file_path, "a")

    f.write("%s,%s\n" % (step, loss_value))
    f.close()


def read_reward_file():
    epochs_list = []
    reward_list = []
    f = open("%s/final_reward.txt" % etc.OUTPUT_PATH)
    con = f.read()
    f.close()
    con_lt = con.split("\n")
    for i in range(len(con_lt) - 1):
        lt = con_lt[i].split(',')
        epochs_list.append(int(lt[0]))
        reward_list.append(float(lt[1]))
    return epochs_list, reward_list


def read_loss_file(file_name=""):
    epochs_list = []
    reward_list = []
    f = open(file_name)
    con = f.read()
    f.close()
    con_lt = con.split("\n")
    for i in range(len(con_lt) - 1):
        lt = con_lt[i].split(',')
        epochs_list.append(int(lt[0]))
        reward_list.append(float(lt[1]))
    return epochs_list, reward_list


def show_reward_pic():
    epoch_list, reward_list = read_reward_file()
    reward_sum = 0.0
    for i in range(len(reward_list)):
        reward_sum += reward_list[i]

    reward_mean = reward_sum / len(reward_list)
    e = np.asarray(epoch_list)
    r = np.asarray(reward_list)
    plt.figure()
    plt.plot(e, r)
    plt.xlabel('Epochs')
    plt.ylabel('Reward')
    plt.show()


def show_loss_pic(loss_name="loss_critic"):
    file_name = "%s/%s.txt" % (etc.OUTPUT_PATH, loss_name)
    step_list, loss_list = read_loss_file(file_name)
    e = np.asarray(step_list)
    r = np.asarray(loss_list)
    plt.figure()
    plt.plot(e, r)
    plt.xlabel('steps')
    plt.ylabel(loss_name)
    plt.show()


def show_pic():
    show_reward_pic()
    show_loss_pic("loss_actor")
    show_loss_pic("loss_critic")
