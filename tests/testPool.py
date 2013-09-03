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
config = {
    "maxActive": 23,
    "maxIdle" :7   
}
class TestPoolFunctions(unittest.TestCase):

    def setUp(self):
        self.pool = Pool(MsgPackPoolableFactory(), **config)
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.pool.destroy()
    def test_ping(self):
        try:
            client = self.pool.borrowObject()
            self.assertIsNotNone(client, "client is None")
            rs = client.call("ping")
            self.assertEqual(rs, "pong", "is pinged")
            print rs
        finally:
            self.pool.returnObject(client)

   
            
import msgpackrpc
PORT = 18800

class MsgPackPoolableFactory(PoolableFactory):
    def __init__(self):
        pass
    def create(self):
        client = msgpackrpc.Client(msgpackrpc.Address("localhost", PORT))
        logging.debug("create client")
        return client
    def validate(self, obj):
        rs = obj.call("ping")
        logging.debug("ping server")
        return rs == "pong"
    def destroy(self, obj):
        obj.close()
        logging.debug("close client")
        
        
class TestService(object):
    def ping(self):
        return "pong"


   
    
from threading import * 


    
class StartServer(Thread): 
    
    def __init__(self):    
        Thread.__init__(self) 
  
           
    def run(self):   
        self.server = msgpackrpc.Server(TestService())
        self.server.listen(msgpackrpc.Address("localhost", PORT))
        self.server.start()
    def stop(self):
        self.server.stop()
        self.server.close()
        
            
              
if __name__ == '__main__':
    s = StartServer()
    s.start()
    unittest.main()
    logging.debug("finished.")
    s.stop()


 
