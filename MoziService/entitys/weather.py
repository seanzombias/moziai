# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : weather.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################


class CWeather():
    '''天气'''
    def __init__(self, mozi_server):
        self.mozi_server = mozi_server
        self.ClassName = ""
        self.fSkyCloud = 0.0
        self.fRainFallRate = 0.0
        self.dTemperature = 0.0
        self.iSeaState = 0

    def setWeather(self, temperature, rainfall, undercloud, seastate):
        '''
        设置当前天气条件
        temperature number 当前基线温度（摄氏度），随纬度变化。
        rainfall number 降水量，0-50.
        undercloud number 云层覆盖度， 0.0-1.0
        seastate number 当前海况， 0-9.
        '''        
        return self.mozi_server.sendAndRecv(
            "ScenEdit_SetWeather({},{},{},{})".format(temperature,rainfall,undercloud,seastate))

    def getWeather(self):
        '''
        得到当前天气条件
        返回：table 天气参数数组
        '''        
        return self.mozi_server.sendAndRecv("ScenEdit_GetWeather()")        

