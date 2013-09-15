#!/usr/bin/env python
# coding=utf-8
"""
Created on 2013-6-20

@author: Tietang
"""

import MySQLdb
import time
import string
from Queue import *
import logging
import pickle
from threading import *

from datetime import *
import time

logging.basicConfig(level=logging.DEBUG)


class PoolableFactory():
    def create(self):
        """实例化一个对象"""
        pass

    def activate(self, obj):
        '''激活对象，使其可用，如果对象是一个socke链接，通常是建立连接'''
        pass

    def passivate(self, obj):
        '''去活对象，使其不可用，如果对象是一个socke链接，通常是关闭连接'''
        pass

    def validate(self, obj):
        '''验证对象是否激活，如果对象是一个socke链接，通常是来检测连接是否有效，最好通过基于业务的ping来检测'''
        pass

    def destroy(self, obj):
        '''去活对象并释放梭占用的资源'''
        pass


class ExhaustedAction:
    WHEN_EXHAUSTED_FAIL = 0;
    WHEN_EXHAUSTED_BLOCK = 1;
    WHEN_EXHAUSTED_GROW = 2;


class Pool:
    # 设置后进先出的池策略 
    lifo = True
    # 允许最大活动对象数 
    maxActive = 10
    # 允许最大空闲对象数 
    maxIdle = 6
    # 允许最大等待时间毫秒数 
    maxWait = 150000
    # 被空闲对象回收器回收前在池中保持空闲状态的最小时间毫秒数 
    minEvictableIdleTimeMillis = 100000
    # 设定在进行后台对象清理时，每次检查对象数 
    numTestsPerEvictionRun = 1
    # 指明是否在从池中取出对象前进行检验,如果检验失败,则从池中去除连接并尝试取出另一个. 
    testOnBorrow = False
    # 指明是否在归还到池中前进行检验 
    testOnReturn = False
    # 指明连接是否被空闲连接回收器(如果有)进行检验.如果检测失败,则连接将被从池中去除. 
    testWhileIdle = False
    # 在空闲连接回收器线程运行期间休眠的时间毫秒数. 如果设置为非正数,则不运行空闲连接回收器线程 
    timeBetweenEvictionRunsMillis = 120000  # 2分钟
    # 当池中对象用完时，请求新的对象所要执行的动作 
    whenExhaustedAction = ExhaustedAction.WHEN_EXHAUSTED_FAIL;
    # numTestsPerEvictionRun=3
    timeBetweenEvictionRunsMillis = 60000  # 当 >0时启用                                                                                                    
    # softMinEvictableIdleTimeMillis      

    __timedelta = timedelta(seconds=-60)
    _available = True


    def __init__(self, poolableFactory, **config):
        from Queue import Queue, LifoQueue

        self.__dict__.update(config)
        logging.debug(config)
        logging.debug(self)
        if self.lifo:
            self._pool = LifoQueue(self.maxActive)
            logging.debug("create a lifo queue.")
        else:
            self._pool = Queue(self.maxActive)  # create the queue
            logging.debug("create a FIFO queue.")

        self.poolableFactory = poolableFactory

        try:
            logging.info("Init {0} objects for pool.".format(self.maxIdle))
            for i in range(self.maxIdle):
                self.put(self.poolableFactory.create())
            logging.info("Inited {0} objects for pool.".format(self.maxIdle))
            self._available = True
            if self.timeBetweenEvictionRunsMillis > 0:
            #                 self.__startCheckThread()
                pass
        except Exception, e:
            raise e

    def put(self, obj):
        self.__check()
        try:
            self._pool.put(obj)
        except Exception, e:
            raise Exception("fill object error:" + str(e))

    def returnObject(self, obj):
        try:
            isValidated = True;
            if self.testOnReturn:
                isValidated = self.poolableFactory.validate(obj)
            if isValidated:
                if self._pool.full():
                    self.poolableFactory.destroy(obj)
                else:
                    self._pool.put(obj)
        except Exception, e:
            raise Exception("return object error:" + str(e))

    def borrowObject(self):
        self.__check()
        isValidate = True;
        try:
            timeout = self.maxWait
            if self.whenExhaustedAction is not ExhaustedAction.WHEN_EXHAUSTED_BLOCK:
                timeout = -1

            if self._pool.empty():
                obj = self.poolableFactory.create()
                isValidate = False;
                self.put(obj)
                logging.debug("create one")
            else:
                obj = self._pool.get(self.whenExhaustedAction == ExhaustedAction.WHEN_EXHAUSTED_BLOCK, timeout)
                logging.debug("get one")

            if self.testOnReturn and isValidate:
                self.poolableFactory.validate(obj)
                logging.debug("validate one")

            return obj
        except Exception, e:
            raise Exception("borrow object error:" + str(e))

    def __check(self):
        if not self._available:
            raise Exception("Current pool is not available.")
        #     def __str__(self):
        #         return  pickle.dumps(self)

    def __checkObject(self):
        self.__check();
        while True:
            try:
                obj = self._pool.get(block=True);
                if obj is not None:
                    hasAttr = hasattr(obj, 'checkTime');
                    if not hasAttr or (hasAttr and obj.checkTime - datetime.now() > self.__timedelta):
                        isValidate = True;
                        obj.checkTime = datetime.now()
                    else:
                        isValidate = False;
                        self.put(obj)

                    if isValidate:
                        if self.poolableFactory.validate(obj):
                            self.put(obj)
                        else:
                            self.poolableFactory.destroy(obj)
                            logging.debug("can't validate object: " + str(obj))
                else:
                    time.sleep(60)
                time.sleep(0.1)
            except Exception, e:

                logging.debug("validate object error. {0} {1}".format(self._pool.qsize(), str(e)))


    def __startCheckThread(self):
        te = Thread(target=self.__checkObject)
        te.start()

    def destroy(self):
        '''
                销毁整个对象池
        '''
        self._available = False
        try:
            #             self._pool.get().close()
            while True:
                try:
                    obj = self._pool.get_nowait()
                    self.poolableFactory.destroy(obj)
                except Empty, e:
                    logging.debug("destory finished and exit.")
                    break
            logging.debug("destory pool")
        except Exception, e:
            raise Exception("destroy pool error:" + str(e))

 
 
        
