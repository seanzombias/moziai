#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2020-01-07 03:28
# Modified date : 2020-01-09 20:09
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import torch
import os

app_abspath = os.path.dirname(__file__)
#USE_CUDA = torch.cuda.is_available()
USE_CUDA = False
device = torch.device("cuda" if USE_CUDA else "cpu")

#######################
SERVER_IP = "127.0.0.1"
SERVER_PORT = "6260"
SCENARIO_NAME = "Iraq.scen"
simulate_compression = 4
DURATION_INTERVAL = 90

target_radius = 10000.0
target_name = "坦克排(T-72 MBT x 4)"

task_end_point = {}
#task_end_point["latitude"] = 43.4874
#task_end_point["longitude"] = 34.1755

task_end_point["latitude"] = 33.3610780570352
task_end_point["longitude"] = 44.3777800928825

control_noise = True
#######################

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
EPOCH_FILE = "%s/epochs.txt" %(OUTPUT_PATH)
#######################

TRANS_DATA = True
