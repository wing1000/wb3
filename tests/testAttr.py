#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-24

@author: tietang
'''
# coding: utf-8
import hashlib
class AAA():
    aaa = 10

obj1 = AAA()
obj2 = AAA()
print obj1.aaa, obj2.aaa, AAA.aaa
print obj1.__dict__, obj2.__dict__, AAA.__dict__

obj1.aaa += 2
print obj1.aaa, obj2.aaa, AAA.aaa 
print obj1.__dict__, obj2.__dict__, AAA.__dict__

AAA.aaa += 3
print obj1.aaa, obj2.aaa, AAA.aaa
print obj1.__dict__, obj2.__dict__, AAA.__dict__
obj1.xxx=90
print obj1.xxx
print  hash("42uroeiwurwo32")
print hex(2312)
