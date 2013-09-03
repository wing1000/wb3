#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-21

@author: tietang
'''


from pool import  Transaction
  
dbconfig = {
    "host":"127.0.0.1:4000",
    "user":"root",
    "password":"",
    "database":"test"  
}
poolConfig = {}

def test(db):
    return db.get("select now() as time")

def test2(db):
    return db.query("select now() as time")

class Test3():
    @staticmethod
    def test(db):
        return db.get("select now() as time")
    
class Test4():
    def test(self,db):
        return db.get("select now() as time")

if __name__ == '__main__':
    t=Transaction(dbconfig, poolConfig)
    rs = t.execute(test)
    print rs.time
    rses = t.execute(test2)
    print [str(rs.time) for rs in rses]
    rs = t.execute(Test3.test)
    print rs.time
    rs = t.execute(Test4().test)
    print rs.time
    rs= t.execute(lambda db:db.get("select now() as time"))
    print rs.time
    t.destory()
    
