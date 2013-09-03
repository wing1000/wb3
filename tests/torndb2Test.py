#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-27

@author: tietang
'''
from pool import   *

dbconfig = {
    "host":"127.0.0.1:4000",
    "user":"root",
    "password":"",
    "database":"test"  
}
import MySQLdb
 
db = MySQlConnection("127.0.0.1:4000", "test", user="root", password="")
print db
print db.ping()
print db.query("select 1")

poolConfig = {}
ta = Transaction(dbconfig, poolConfig)

@ta
def test(db):
    return db.get("select now() as time")
@ta
def insert(db,name, birthday, is_relative):
    return db.insert("insert into person(name,birthday,is_relative) values(%s,%s,%s)", name, birthday, is_relative)

class Test3():
    @staticmethod
    @ta
    def test(db):
        return db.get("select now() as time")   
    
    @staticmethod
    @ta
    def test2(db, x, p=""):
        return db.get("select now() as time")
    
 

print test()
from datetime import date
print insert("x1", date.today(), 1)
print Test3.test()
 
print Test3.test2(1, p="xx")
print 123

# def fun_a(ob):
#     def new(*args):
#         db=90
#         print "start ta."
#         x=  ob(db,*args)
#         print "invoke ta."
#         print "finished ta."
#         return x
#   
#     return new
#  
# @fun_a
# def fun_b(db,a, b):
#     """this is function b"""
#     print db
#     print a + b
#     print "world"
# 
# fun_b(3, 4)
