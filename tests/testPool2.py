#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-21

@author: Tietang
'''
import random
import unittest
from pool import  PoolableFactory, Pool
import logging        
import redis  
config = {
    "maxActive": 23,
    "maxIdle" :7   
}
  
            
PORT = 18800

class RedisPoolableFactory(PoolableFactory):
    def __init__(self):
        pass
    def create(self):
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        logging.debug("create client")
        return client
    def validate(self, obj):
        try:
            rs = obj.ping()
            logging.debug("ping server")
            return rs == "pong"
        except Exception, e:
            return False
    def destroy(self, obj):
        try:
            obj.close()
            logging.debug("close client")
        except Exception,e:
            logging.debug("close error: "+str(e))
        
        
   
    
from threading import * 
pool = Pool(RedisPoolableFactory(), **config)
class ClientTest(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.pool = pool
        self.name = "th-{0}".format(i)
    def run(self):
        try:
            client = self.pool.borrowObject()
            rs = client.ping()
            print current_thread().name + " " + str(rs)
            rs = client.set("x2", 3)
            print rs
            rs = client.get("x2")
            print rs
        finally:
            self.pool.returnObject(client)  
   
  
if __name__ == '__main__':
    for i in range(1, 1):
        ClientTest(i).start()
    logging.debug("finished.")
 



 
