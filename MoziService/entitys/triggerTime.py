#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : side.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################
from abc import ABCMeta, abstractmethod
import re
import logging

########################################################################
class CTariggerTime():
    #----------------------------------------------------------------------
    def __init__(self, mozi_server):
        self.strName = ""
        self.strGuid = ""
        self.strDescription = ""
        self.bIsRepeatable = ""
        self.bIsActive = ""
        self.bIsMessageShown = ""
        self.sProbability = ""
        self.m_Triggers = ""
        self.m_Conditions = ""
        self.m_Actions = ""