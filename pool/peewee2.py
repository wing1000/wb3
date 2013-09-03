#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-27

@author: tietang
'''
from __future__ import absolute_import, division, with_statement
from pool import PoolableFactory, Pool
import _mysql
import copy
import itertools
import logging
import os
import time
from peewee import *
from peewee import Model as _Model
from peewee import MySQLDatabase as _MySQLDatabase

version = "0.1"
version_info = (0, 1, 0, 0)

class Peewee2PoolableFactory(PoolableFactory):
    '''    
        "host" : "127.0.0.1",
        "port":3305,
        "db" :None,
        "user" : "root",
        "password" :None,
        "connect_timeout" : 3000,
        "use_unicode":True,
        "charset","utf8",
    '''
    connect_kwargs = {
        "host" : "127.0.0.1",
        "port":3305,
        "db" :None,
        "user" : "root",
        "password" :None,
        "connect_timeout" : 3000,
        "use_unicode":True,
        "charset":"utf8",
    }
   
    def __init__(self, **connect_kwargs):
        self.__dict__.update(connect_kwargs)
        self.connect_kwargs = connect_kwargs;
    def create(self):
        db = MySQLDatabase(self.connect_kwargs)
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
        
class MySQLDatabase(_MySQLDatabase):
    def __init__(self, **connect_kwargs):
        self.connect_kwargs = connect_kwargs
        
    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._connect(self.database, self.connect_kwargs)

    def ping(self):
        self.get_conn().ping()
       


