#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : paser_show.py
# Create date : 2019-12-06 11:58
# Modified date : 2019-12-06 11:59
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
import pylog

def show_class_info(dic):
    for key in dic:
        pylog.info("%s:%s" % (key, len(dic[key])))

def show_item_info(dic):
    for key in dic:
        pylog.info("%s:%s" % (key, dic[key]))
