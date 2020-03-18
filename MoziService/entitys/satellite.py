# -*- coding:utf-8 -*-
##########################################################################################################
# File name : satellite.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################
from MoziService.entitys.activeunit import CActiveUnit


class Csatellite(CActiveUnit):
    '''
    卫星类
    '''
    def __init__(self):
        '''卫星'''
        super().__init__()
        self.m_SatelliteCategory=None #卫星类别
        self.m_TracksPoints=None #卫星航迹线 航迹是根据卫星算法得出的
        
    def sate_set_rader_shutdown(self,trunoff):
        '''
        类别：编辑使用函数
        设置雷达开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_rader_shutdown(trunoff)

    def sate_set_sonar_shutdown(self,trunoff):
        '''
        类别：编辑使用函数
        设置声纳开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_sonar_shutdown(trunoff)

    def sate_set_OECM_shutdown(self,trunoff):
        '''
        类别：编辑使用函数
        设置干扰开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_OECM_shutdown(trunoff)