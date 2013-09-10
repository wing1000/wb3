#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-28

@author: Tietang
'''
from datetime import datetime
from hashlib import md5

from db import *


class User():
    @staticmethod
    @sta
    def checkHasUser(db):
        return db.get('SELECT `user_id` FROM `sp_user` LIMIT 1')

    @staticmethod
    @sta
    def allUser(db):
        return db.query('SELECT * FROM `sp_user`')

    @staticmethod
    @sta
    def getUserByName(db, name):
        return db.get('SELECT * FROM `sp_user` WHERE `username` = \'%s\' LIMIT 1' % str(name))

    @staticmethod
    @sta
    def getUserByEmail(db, email):

        return db.get('SELECT * FROM `sp_user` WHERE `email` = \'%s\' LIMIT 1' % str(email))

    @staticmethod
    @mta
    def add(db, name, email, pw):
        if name and pw:
            query = "insert into `sp_user` (`username`,`email`,`password`,`create_at`,`update_at`) values(%s,%s,%s,%s,%s)"
            now = datetime.now()
            return db.insert(query, name, email, md5(pw.encode('utf-8')).hexdigest(), now, now)
        else:
            return None

    @staticmethod
    @mta
    def updatePasswordById(db, id=None, pw=None):
        if id and pw:
            query = "update `sp_user` set `password`=%s, `update_at`=%s where id_user=%s "

            return db.execute(query, md5(pw.encode('utf-8')).hexdigest(), datetime.now(), id)
        else:
            return None


    @staticmethod
    @sta
    def checkUser(db, name='', pw=''):
        if name and pw:
            user = db.get_user_by_name(name)
            if user and user.name == name and user.password == pw:
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    User.add("xc", "xx@134.com", "www")