#!/usr/bin/python
# -*- coding: utf-8 -*-
# by aie

class BT:
    def __init__(self):
        self.results={'success' :"success", 'fail' : "fail", 'wait' : "wait", 'error' : "error"}
        self.children = {}
        #self.guid = guid
        #self.shortKey = shortKey
        #self.options = options
        #self.run = action

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
        return BT.results['success']
    
    def make(self,action,guid,shortKey,options):
        instance = BT()
        instance.children = {}
        instance.guid = guid
        instance.shortKey = shortKey
        instance.options = options
        instance.run = action
        #TODO: assert type(instance.run) == "function", "Behavior tree node needs a run function, got "..type(instance.run).." instead.")
        return instance

    def addChild(self,child):
        #self.children.update(child)
        n=len(self.children)
        self.children[n+1]=child

    def sequence(self,args):
        for k,v in self.children.items() :
            if (self.wrap(v.run(args)) == self.results['fail']) :
                return self.results['fail']
        return self.results['success']

    def select(self,args):
        for k,v in self.children.items():
            if (self.wrap(v.run(args)) == self.results['success']) :
                return self.results['success']
        return self.results['fail']

    def slicesequence(self,args):
        if (self.current == None) :
            self.current = 1
        else:
            child = self.children[self.current]
            if (child == None) :
                self.current = 1
                return self.results['success']
            result = self.wrap(child.run(args))
            if (result == self.results.fail) :
                self.current = 1
                return self.results['fail']
            if (result == self.results['success']) :
                self.current = self.current + 1
        return self.results['wait']

    def sliceselect(self,args):
        if (self.current == None) :
            self.current = 1
        else:
            child = self.children[self.current]
            if (child == None) :
                self.current = 1
                return BT.results['fail']
            result = self.wrap(child.run(args))
            if (result == self.results['success']) :
                self.current = 1
                return self.results['success']
            if (result == self.results.fail) :
                self.current = self.current + 1
        return self.results['wait']

    def invert(self,args):
        if (self.children[1] == None) :
            return self.results['success']
        result = self.wrap(self.children[1].run(args))
        if (result == self.results.success) :
            return self.results['fail']
        if (result == self.results.fail) :
            return self.results['success']
        return result

    def repeatUntilFail(self,args):
        while (self.wrap(self.children[1].run(args)) != self.results['fail']):1
        return self.results['success']

    def waitUntilFail(self,args):
        if (self.wrap(self.children[1].run(args)) == self.results.fail) :
            return BT.results['success']
        return BT.results['wait']

    def limit(self,args):
        if (self.limit == None) :
            self.limit = 1
            if (self.count == None) :1

stop = 0
while (stop == 0) :
        ###############
    bt = BT()
    btChild = bt.make(bt.select, 'guid', 'shortkey', 'options')
    bt.addChild(btChild)
    print(bt.children)
        ################
    if stop == 1 :
        break