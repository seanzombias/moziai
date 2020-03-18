#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : pyfile.py
# Create date : 2013-07-17 19:19
# Modified date : 2020-01-09 05:50
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from __future__ import division
from __future__ import print_function

import os
import sys
from . import pylog

def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def write_file(con, name="default", path='./tmp_file/'):
    f = create_file(path, name)
    f.write(con)
    f.close()

def get_file_full_name(path, name):
    create_path(path)
    if path[-1] == "/":
        full_name = path +  name
    else:
        full_name = path + "/" +  name
    return full_name

def open_file(path, name, open_type='a'):
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)

def create_file(path, name, open_type='w'):
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)

def check_is_have_file(path, name):
    file_name = get_file_full_name(path, name)
    return os.path.exists(file_name)

def open_file_with_full_name(full_path, open_type):
    try:
        file_object = open(full_path, open_type)
        return file_object
    except Exception as e:
        if e.args[0] == 2:
            open(full_path, 'w')
        else:
            pylog.error(e)

def delete_dir(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except Exception as e:
            pylog.error(e)
            return False
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_dir(itemsrc)
        try:
            os.rmdir(src)
        except Exception as e:
            pylog.error(e)
            return False
    return True
