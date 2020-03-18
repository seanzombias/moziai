#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : pic.py
# Create date : 2019-10-15 20:31
# Modified date : 2020-03-10 12:47
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

import pandas

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
    for i in range(len(con_lt)-1):
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
    for i in range(len(con_lt)-1):
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
    plt.plot(e,r)
    plt.xlabel('Epochs')
    plt.ylabel('Reward')
    plt.show()

def show_loss_pic(loss_name="loss_critic"):
    file_name = "%s/%s.txt" % (etc.OUTPUT_PATH, loss_name)
    step_list, loss_list = read_loss_file(file_name)
    e = np.asarray(step_list)
    r = np.asarray(loss_list)
    plt.figure()
    plt.plot(e,r)
    plt.xlabel('steps')
    plt.ylabel(loss_name)
    plt.show()

def get_sum_lt(num_lt):
    sum_lt = [] 
    sum_num = 0
    for num in num_lt:
        sum_num += num
        sum_lt.append(sum_num)
    return sum_lt

def get_destroy_loss_rate_lt(path, name):
    data = pandas.read_csv("%s/%s" % (path, name))

    destroy_num_lt = data["destroy_num"].tolist()
    destroy_sum_lt = get_sum_lt(destroy_num_lt)

    loss_num_lt = data["loss_num"].tolist()
    loss_sum_lt = get_sum_lt(loss_num_lt)
    rate_lt = []
    for i in range(len(destroy_sum_lt)):
        destroy_num = destroy_sum_lt[i]
        loss_num = loss_sum_lt[i]
        if loss_num == 0:
            loss_num = 1
        rate = destroy_num / loss_num
        rate_lt.append(rate)

    return rate_lt

def get_learning_destroy_loss_rate():
    path = etc.DESTROY_LOSS_RATE_PATH
    name = etc.LEARNING_DESTROY_LOSS_RATE_FILE
    return get_destroy_loss_rate_lt(path, name)

def get_primary_destroy_loss_rate():
    path = etc.DESTROY_LOSS_RATE_PATH
    name = etc.PRIMARY_DESTROY_LOSS_RATE_FILE
    return get_destroy_loss_rate_lt(path, name)

def show_destroy_loss_rate():
    primary_rate_lt = get_primary_destroy_loss_rate()

    primary_step_lt = range(len(primary_rate_lt))

    learning_rate_lt = get_learning_destroy_loss_rate()
    learning_step_lt = range(len(learning_rate_lt))

    primary_e = np.asarray(primary_step_lt)
    primary_r = np.asarray(primary_rate_lt)
    learning_e = np.asarray(learning_step_lt)
    learning_r = np.asarray(learning_rate_lt)

    plt.figure()
    plt.plot(learning_e,learning_r, label="learning_destroy_loss_rate")
    plt.plot(primary_e,primary_r, label="primary_destroy_loss_rate")
    plt.legend()
    plt.xlabel('steps')
    plt.ylabel("destroy_loss_rate")
    plt.show()

def show_primary_destroy_loss_rate():
    rate_lt = get_primary_destroy_loss_rate()

    step_lt = range(len(rate_lt))

    e = np.asarray(step_lt)
    r = np.asarray(rate_lt)
    plt.figure()
    plt.plot(e,r)
    plt.xlabel('steps')
    plt.ylabel("destroy_loss_rate")
    plt.show()

def show_learning_destroy_loss_rate():
    rate_lt = get_learning_destroy_loss_rate()

    step_lt = range(len(rate_lt))

    e = np.asarray(step_lt)
    r = np.asarray(rate_lt)
    plt.figure()
    plt.plot(e,r)
    plt.xlabel('steps')
    plt.ylabel("destroy_loss_rate")
    plt.show()

def show_pic():
    show_destroy_loss_rate()
    #show_primary_destroy_loss_rate()
    #show_learning_destroy_loss_rate()
    #show_reward_pic()
    #show_loss_pic("loss_actor")
    #show_loss_pic("loss_critic")
