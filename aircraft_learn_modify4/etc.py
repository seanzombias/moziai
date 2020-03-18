#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2020-01-07 03:28
# Modified date : 2020-03-10 11:05
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
SERVER_PORT = "6060"
SCENARIO_NAME = "aircraft2"
simulate_compression = 3
DURATION_INTERVAL = 30

target_radius = 6000.0
target_name = "PL-636.3“阿尔罗萨级”柴电潜艇"

task_end_point = {}
task_end_point["latitude"] = 43.4874
task_end_point["longitude"] = 34.1755

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

DESTROY_LOSS_RATE_PATH = "%s/destroy_loss_rate" % (OUTPUT_PATH)
PRIMARY_DESTROY_LOSS_RATE_FILE = "primary.csv"
LEARNING_DESTROY_LOSS_RATE_FILE = "learning.csv"

PRIMARY_LOSS = False


