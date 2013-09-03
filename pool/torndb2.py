#!/usr/bin/env python
# coding=utf-8
'''
Created on Jun 21, 2013
基于torndb以便能手动提交事务 
@author: tietang
'''
from __future__ import absolute_import, division, with_statement
from pool import PoolableFactory, Pool
from torndb import Connection
import _mysql
import copy
import itertools
import logging
import os
import time


try:
    import MySQLdb.constants
    import MySQLdb.converters
    import MySQLdb.cursors
except ImportError:
    # If MySQLdb isn't available this module won't actually be useable,
    # but we want it to at least be importable on readthedocs.org,
    # which has limitations on third-party modules.
    if 'READTHEDOCS' in os.environ:
        MySQLdb = None
    else:
        raise

version = "0.1"
version_info = (0, 1, 0, 0)

class Torndb2PoolableFactory(PoolableFactory):
    host = "127.0.0.1:3306"
    database = None
    user = "root"
    password = None
    max_idle_time = 7 * 3600
    connect_timeout = 3000
    time_zone = '+8:00'
    
    def __init__(self, **config):
        self.__dict__.update(config)
    def create(self):
        db = MySQlConnection(self.host, self.database, self.user, self.password, self.max_idle_time, self.connect_timeout, self.time_zone)
        return db
    def activate(self, db):
        db.reconnect()
    def passivate(self, db):
        db.close()
    def validate(self, db):
        try:
            db.ping()
            return True
        except Exception , e:
            return False
    
    def destroy(self, db):
        db.close()
        db = None
        
class MySQlConnection(Connection):
    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(False)
    def commit(self):
        self._db.commit()
    def rollback(self):
        self._db.rollback()
    def ping(self):
        self._db.ping()
        


class Transaction():
    '''
      基本用法1:
    ta = Transaction(dbconfig, poolConfig)
    
    @ta
    def test(param1,param2,db):
        return db.get("select now() as time")
    test(param1,param2)
       注意db参数在函数的 第一个
       
    基本用法1:
    ta=Transaction(dbconfig, poolConfig)
    def fun():
        //do something
    ta.execute(fun)
    
    example1:
    
    dbconfig = {
        "host":"127.0.0.1:4000",
        "user":"root",
        "password":"",
        "database":"test"  
    }
    poolConfig = {}
    ta = Transaction(dbconfig, poolConfig)
    
    @ta
    def test(db):
        return db.get("select now() as time")
    @ta
    def insert(name, birthday, is_relative,db):
        return db.insert("insert into person(name,birthday,is_relative) values(%s,%s,%s)", name, birthday, is_relative)
    
    class Test3():
        @staticmethod
        @ta
        def test(db):
            return db.get("select now() as time")
        
 
    
    print test()
    from datetime import date
    print insert("x1", date.today(), 1)
    print Test3.test()
 

    example2:
    
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
    '''
    
    def __init__(self, dbConfig=None, poolConfig=None, pool=None):
        '''可给定dbConfig 和poolConfig 或者pool'''
        if pool is None:
            self._pool = Pool(Torndb2PoolableFactory(**dbConfig), **poolConfig)
        else:
            self._pool = pool
            
    def destory(self):
        self._pool.destroy()  
        
    def __call__(self, func):
       
        def execute(*args,**kwargs):
            try:
                db = self._pool.borrowObject()
                a = []
                a.append(db)
                for arg in args:
                    a.append(arg)
                
                newArgs = tuple(a)
#                 print newArgs
                return func(*newArgs,**kwargs)
            except Exception, e:
                db.rollback()
                raise e
            finally:
                db.commit()
                self._pool.returnObject(db)
        return execute    
    
    def __call_instance__(self, func):
       
        def execute(*args,**kwargs):
            try:
                db = self._pool.borrowObject()
                a = []
                for arg in args:
                    a.append(arg)
                a.append(db)
                newArgs = tuple(a)
                return func(*newArgs,**kwargs)
            except Exception, e:
                db.rollback()
                raise e
            finally:
                db.commit()
                self._pool.returnObject(db)
        return execute

    def execute(self, callback):
        ''''''
        try:
            db = self._pool.borrowObject()
            return callback(db)  
        except Exception, e:
            db.rollback()
            raise e
        finally:
            db.commit()
            self._pool.returnObject(db)
            


         
