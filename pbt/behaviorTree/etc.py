#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2020-01-07 03:28
# Modified date : 2020-01-09 19:31
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import torch
import os

app_abspath = os.path.dirname(__file__)
# USE_CUDA = torch.cuda.is_available()
USE_CUDA = False
device = torch.device("cuda" if USE_CUDA else "cpu")

#######################
SERVER_IP = "39.105.136.247"
#SERVER_IP = "192.168.142.130"
SERVER_PORT = "6060"
# SCENARIO_NAME = "tank1"  # 最好的版本但是没有任务。
# SCENARIO_NAME = "tank_task1"  # 最好的版本
# SCENARIO_NAME = "tank_task0"  # 距离近，有任务
# SCENARIO_NAME = "0213"  # 距离近，有任务
SCENARIO_NAME = "马博士想定.scen"

simulate_compression = 3
DURATION_INTERVAL = 30

target_radius = 3700.0
target_name = "坦克排(M1A2 SEP 艾布拉姆斯 MBT x4主战坦克)"
task_end_point = {"latitude": 27.74666, "longitude": 16.332222}

control_noise = True

#######################
MAX_EPISODES = 5000
MAX_BUFFER = 1000000
MAX_STEPS = 30
#######################

#######################
TMP_PATH = "%s/%s/tmp" % (app_abspath, SCENARIO_NAME)
OUTPUT_PATH = "%s/%s/output" % (app_abspath, SCENARIO_NAME)

CMD_LUA = "%s/cmd_lua" % TMP_PATH
PATH_CSV = "%s/path_csv" % OUTPUT_PATH
MODELS_PATH = "%s/Models/" % OUTPUT_PATH
EPOCH_FILE = "%s/epochs.txt" % (OUTPUT_PATH)
#######################

TRANS_DATA = True

WEBSOCKET_PORT = 9998
WEBSOCKET_SERVER = "39.105.136.247"
