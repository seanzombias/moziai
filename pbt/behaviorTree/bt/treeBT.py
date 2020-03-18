# !/usr/bin/python
# -*- coding: utf-8 -*-
# by aie

class BT:
    '''
    行为树
    '''
    def __init__(self):
        self.results={'success' :"success", 'fail' : "fail", 'wait' : "wait", 'error' : "error"}
        self.children = {}
        self.guid = None
        self.shortKey = None
        self.options = None
        self.run = None
        self.name = None

    def wrap(self, value):
        for k, v in self.results.items() :
            if (value == k) :
                return v
            if (value == v) :
                return v
        #If it's false, return fail
        if (value == False) :
            return self.results['fail']\
        #If it's anything else, return success
        return self.results['success']

    def make(self, action, guid, shortKey, options):
        self.guid = guid
        self.shortKey = shortKey
        self.options = options
        self.run = action
        self.name = str(action)

    def addChild(self,child):
        #self.children.update(child)
        n=len(self.children)
        self.children[n+1]=child

    def sequence(self,mozi,env):
        '''
        判断节点子节点

        '''
        for k,v in self.children.items() :
            if (self.wrap(v.run(mozi,env)) == self.results['fail']) :
                return self.results['fail']
        return self.results['success']

    def select(self,mozi,env):
        '''一个成功都往下走'''
        for k,v in self.children.items():
            if (self.wrap(v.run(mozi,env)) == self.results['success']) :
                return self.results['success']
        return self.results['fail']

    def slicesequence(self,mozi,env):
        if (self.current == None) :
            self.current = 1
        else:
            child = self.children[self.current]
            if (child == None) :
                self.current = 1
                return self.results['success']
            result = self.wrap(child.run(mozi,env))
            if (result == self.results.fail) :
                self.current = 1
                return self.results['fail']
            if (result == self.results['success']) :
                self.current = self.current + 1
        return self.results['wait']

    def sliceselect(self,mozi,env):
        if (self.current == None) :
            self.current = 1
        else:
            child = self.children[self.current]
            if (child == None) :
                self.current = 1
                return BT.results['fail']
            result = self.wrap(child.run(mozi,env))
            if (result == self.results['success']) :
                self.current = 1
                return self.results['success']
            if (result == self.results.fail) :
                self.current = self.current + 1
        return self.results['wait']

    def invert(self,mozi,env):
        if (self.children[1] == None) :
            return self.results['success']
        result = self.wrap(self.children[1].run(mozi,env))
        if (result == self.results['success']) :
            return self.results['fail']
        if (result == self.results['fail']) :
            return self.results['success']
        return result

    def repeatUntilFail(self,mozi,env):
        while (self.wrap(self.children[1].run(mozi,env)) != self.results['fail']):1
        return self.results['success']

    def waitUntilFail(self,mozi,env):
        if (self.wrap(self.children[1].run(mozi,env)) == self.results.fail) :
            return BT.results['success']
        return BT.results['wait']

    def limit(self,mozi,env):
        if (self.limit == None) :
            self.limit = 1
            if (self.count == None) :1




