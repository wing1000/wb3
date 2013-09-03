#!/usr/bin/env python
# coding=utf-8

 
#    Normal(0), Busy(1), Error(2), Cancelled(3);
class Status:
    Normal = 0
    Busy = 1 
    Error = 2
    Cancelled = 3
    
class ReadWrite:
    ReadWrite = 0
    Read = 1
    Write = 2
    
class Shard():
    def __init__(self, subject):
        self.__subject = subject
    def __getattr__(self, name):
        return getattr(self.__subject, name)
    
    
class Selector():
    ploy = None
    def __init__(self):
        self.ploy = LoopPloy()
        self.shards = [];
    def select(self, key, funcion):
        pass
    def selectMaste(self, key):
        pass
    def selectSlave(self, key):
        pass
    def selectAny(self, key):
        pass
    def calculate(self, key, shardSize) :
        pass
    def addShard(self, shard):
        pass
 
    def setShard(self, index, shard):
        pass

    def addInstanceInfo(self, index, info):
        pass

    def getShards(self):
        pass

    def getPloy(self):
        return self.ploy

    def setPloy(self, ploy):
        self.ploy = ploy

class Ploy():
    def select(self, key, shard, readWrite):
        pass
    
class LoopPloy(Ploy):
    ct = 0
    def select(self, key, shard, readWrite):
        id = hash(key)
        
    def calculate(self, key, size):
        self.ct += 1
        return  self.ct % size
          
class InstanceInfo():
    def __init__(self):
        self.host;
        self.port;
        self.timeout;
        self.password;
        self.schema;
        self.isMaster = True;
        self.status = Status.Normal;
        self.weight = 1;
 

        

