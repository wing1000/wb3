#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-28

@author: Tietang
'''
from setting import *
from pool import Transaction
import torndb
from pool import  Pool, Torndb2PoolableFactory
pool = Pool(Torndb2PoolableFactory(**MasterDbConfig), **poolConfig)

mta = Transaction(pool=pool)
sta = Transaction(pool=pool)