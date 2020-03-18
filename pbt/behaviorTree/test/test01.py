#!/usr/bin/python
# -*- coding: utf-8 -*-

import behaviorTree.bt.detail as btDet
import behaviorTree.bt.basic as btBas
from behaviorTree.bt.treeBT import BT

'''
def test(fun,prmrs):
    results = exec("%s(%)")
'''

def testEnd():
    print('')
    print('      *************************************')
    print('      *** Have been tested to the End ! ***')
    print('      *************************************')

def testAddAC(mozi):
    a1, a2 = mozi.addAircarft('绾㈡柟', 'AirCraft', 'f1', '6', '32.9', '45.4', '1558', '300', '3000.0')
    b1, b2 = mozi.addAircarft('绾㈡柟', 'AirCraft', 'f2', 6, 33., 45.2, 1558, 300, 4000.0)
    # aa.addAircarft('绾㈡柟', 'AirCraft', 'f1', 6, 44.95, 32.77, 1558, 300, 3000)
    return a2,b2

def testGetWeather(mozi):
    return mozi.getWeather()

def testOperateBtGUID(aa):
    btDet.AddGUID(aa, 'aaaguid', '123-456-789')
    cc = btDet.GetGUID(aa, 'aaaguid')
    print(cc)
    btDet.RemoveAllGUID(aa, 'aaaguid')
    btDet.AddGUID(aa, 'aaaguid', '123-456-789')
    btDet.AddGUID(aa, 'aaaguid', '434-3aa-111')
    btDet.AddGUID(aa, 'aaaguid', '555-4ff-234')
    btDet.RemoveGUID(aa, 'aaaguid', '434-3aa-111')
    cc = btDet.GetGUID(aa, 'aaaguid')
    print(cc)
    dd = btDet.GUIDExists(aa, 'aaaguid', '555-4ff-234')
    print(dd)
    dd = btDet.GUIDExists(aa, 'aaaguid', '555-4ff-233')
    print(dd)
    btDet.SetTimeStampForGUID(aa, 'aaatime')
    ee = btDet.GetTimeStampForGUID(aa, 'aaatime')
    print(ee)
    return cc,ee


    '''
    杩愯�瀹㈡埛绔�嚭鐜扮洰鏍囧悗
    '''
def testContactsBox(env,mozi):
    ff=mozi.getContacts('绾㈡柟')
    print(ff)
    code, contact = mozi.getContact('绾㈡柟', ff[1]['guid'])
    print(contact.name)

    defaults=[btBas.MakeLatLong(0.,0.),btBas.MakeLatLong(0.,1.),btBas.MakeLatLong(1.,1.),btBas.MakeLatLong(1.,0.)]
    gg=btDet.FindBoundingBoxForGivenContacts(mozi, '绾㈡柟', ff, defaults, 10.)
    print(gg)
    return gg

def testMission(mozi):
    code, mm = mozi.getMission('绾㈡柟', 'strike1')
    code2, mm2 = mozi.getMission('绾㈡柟', mm.guid)
    mm3 = mozi.getMissionUnitList('绾㈡柟', mm.guid)
    return mm3

def testRTB(mozi):
    codeHf, hf = mozi.getSideInfo('绾㈡柟')
    hf.contacts[1].name
    hf.units[0].name
    hfGuid = hf.units[0].guid

    rtrn = btDet.DetermineUnitRTB(mozi, hfGuid)
    return rtrn


def leaf01(args):
    if args == 1:
        print('leaf01:True')
        return True
    else:
        print('leaf01:False')
        return False

def leaf02(args):
    if args == 1:
        print('leaf02:True')
        return True
    print('leaf02:False')
    return False

def leaf03(args):
    if args == 0:
        print('leaf03:True')
        return True
    print('leaf03:False')
    return False

def testBT():
    bt0, bt1, bt2, bt3, bt4, bt5 = BT(), BT(), BT(), BT(), BT(), BT()

    bt0.make(bt0.invert, 'guid', 'shortkey', 'options')

    bt1.make(bt1.select, 'guid', 'shortkey', 'options')
    bt2.make(bt2.sequence, 'guid', 'shortkey', 'options')

    bt3.make(leaf01, 'guid', 'shortkey', 'options')
    bt4.make(leaf02, 'guid', 'shortkey', 'options')
    bt5.make(leaf03, 'guid', 'shortkey', 'options')

    bt0.addChild(bt1)

    bt1.addChild(bt2)
    bt1.addChild(bt3)

    bt2.addChild(bt4)
    bt2.addChild(bt5)

    print(bt2.children)
    print(bt0.run(1))
