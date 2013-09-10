#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-28

@author: Tietang
'''
from db import *
from datetime import datetime
from hashlib import md5
class User():
    @staticmethod
    @sta    
    def userExists(db):
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


class Tables():
    @staticmethod
    @mta
    def flush_all_data(db):
        sql = """
        TRUNCATE TABLE `sp_category`;
        TRUNCATE TABLE `sp_comments`;
        TRUNCATE TABLE `sp_links`;
        TRUNCATE TABLE `sp_posts`;
        TRUNCATE TABLE `sp_tags`;
        TRUNCATE TABLE `sp_user`;
        """
        
        db.execute(sql)

    @staticmethod
    @mta        
    def creat_table(db):
        sql = """
DROP TABLE IF EXISTS `sp_category`;
CREATE TABLE IF NOT EXISTS `sp_category` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(17) NOT NULL DEFAULT '',
  `id_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `sp_comments`;
CREATE TABLE IF NOT EXISTS `sp_comments` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `postid` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `url` varchar(75) NOT NULL,
  `visible` tinyint(1) NOT NULL DEFAULT '1',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `postid` (`postid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `sp_links`;
CREATE TABLE IF NOT EXISTS `sp_links` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `displayorder` tinyint(3) NOT NULL DEFAULT '0',
  `name` varchar(100) NOT NULL DEFAULT '',
  `url` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `sp_posts`;
CREATE TABLE IF NOT EXISTS `sp_posts` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(17) NOT NULL DEFAULT '',
  `title` varchar(100) NOT NULL DEFAULT '',
  `content` mediumtext NOT NULL,
  `comment_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `closecomment` tinyint(1) NOT NULL DEFAULT '0',
  `tags` varchar(100) NOT NULL,
  `password` varchar(8) NOT NULL DEFAULT '',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0',
  `edit_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `category` (`category`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `sp_tags`;
CREATE TABLE IF NOT EXISTS `sp_tags` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(17) NOT NULL DEFAULT '',
  `id_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `id_num` (`id_num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `sp_user`;
CREATE TABLE `sp_user` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL DEFAULT '',
  `email` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL DEFAULT '',
  `create_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
"""
        db.execute(sql)
        
if __name__ == '__main__':
    User.add("xc" , "xx@134.com", "www")
 
