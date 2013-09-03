#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-28

@author: Tietang
'''

import logging
import re
from hashlib import md5

from datetime import *

from commons import slugfy, time_from_now, cnnow, timestamp_to_datetime, safe_encode
from setting import *
from db import *

# 主数据库 进行Create,Update,Delete 操作
# 从数据库 读取

# #
HTML_REG = re.compile(r"""<[^>]+>""", re.I | re.M | re.S)



# mta=Transaction(MasterDbConfig, poolConfig)
# sta=Transaction(SlaveDbConfig, poolConfig)

# ##
CODE_RE = re.compile(r"""\[code\](.+?)\[/code\]""", re.I | re.M | re.S)

def n2br(text):
    con = text.replace('>\n\n', '>').replace('>\n', '>')
    con = "<p>%s</p>" % ('</p><p>'.join(con.split('\n\n')))
    return '<br/>'.join(con.split("\n"))    
    
def tran_content(text, code=False):
    if code:
        codetag = '[mycodeplace]'
        codes = CODE_RE.findall(text)
        for i in range(len(codes)):
            text = text.replace(codes[i], codetag)
        text = text.replace("[code]", "").replace("[/code]", "")
        
        text = n2br(text)
        
        a = text.split(codetag)
        b = []
        for i in range(len(a)):
            b.append(a[i])
            try:
                b.append('<pre><code>' + safe_encode(codes[i]) + '</code></pre>')
            except:
                pass
                        
        return ''.join(b)
    else:
        return n2br(text)

def post_list_format(posts):
    for obj in posts:
        obj.absolute_url = '%s/topic/%d/%s' % (BASE_URL, obj.id, slugfy(obj.title))
        obj.taglist = ', '.join(["""<a href="%s/tag/%s/" rel="tag">%s</a>""" % (BASE_URL, tag, tag) for tag in obj.tags.split(',')])
        
        if '<!--more-->' in obj.content:
            obj.shorten_content = obj.content.split('<!--more-->')[0]
        else:
            obj.shorten_content = HTML_REG.sub('', obj.content[:SHORTEN_CONTENT_WORDS])
        
        obj.add_time_fn = time_from_now(int(obj.add_time))
    return posts

def post_detail_formate(obj, db):
    if obj:
        slug = slugfy(obj.title)
        obj.slug = slug
        obj.absolute_url = '%s/topic/%d/%s' % (BASE_URL, obj.id, slug)
        obj.shorten_url = '%s/t/%s' % (BASE_URL, obj.id)
        if '[/code]' in obj.content:
            obj.highlight = True
        else:
            obj.highlight = False        
        obj.content = tran_content(obj.content, obj.highlight)
        obj.taglist = ', '.join(["""<a href="%s/tag/%s/" rel="tag">%s</a>""" % (BASE_URL, tag, tag) for tag in obj.tags.split(',')])
        obj.add_time_fn = time_from_now(int(obj.add_time))
        obj.last_modified = timestamp_to_datetime(obj.edit_time)
        obj.keywords = obj.tags
        obj.description = HTML_REG.sub('', obj.content[:DESCRIPTION_CUT_WORDS])
        # get prev and next obj
        obj.prev_obj = db.get('SELECT `id`,`title` FROM `sp_posts` WHERE `id` > %s LIMIT 1' % str(obj.id))
        if obj.prev_obj:
            obj.prev_obj.slug = slugfy(obj.prev_obj.title)
        obj.next_obj = db.get('SELECT `id`,`title` FROM `sp_posts` WHERE `id` < %s ORDER BY `id` DESC LIMIT 1' % str(obj.id))
        if obj.next_obj:
            obj.next_obj.slug = slugfy(obj.next_obj.title)
        # get relative obj base tags
        obj.relative = []
        if obj.tags:
            idlist = []
            getit = False
            for tag in obj.tags.split(','):
                tagobj = Tag.get_tag_by_name(tag)
                if tagobj and tagobj.content:
                    pids = tagobj.content.split(',')
                    for pid in pids:
                        if pid != str(obj.id) and pid not in idlist:
                            idlist.append(pid)
                            if len(idlist) >= RELATIVE_POST_NUM:
                                getit = True
                                break
                if getit:
                    break
            #
            if idlist:
                obj.relative = db.query('SELECT `id`,`title` FROM `sp_posts` WHERE `id` in(%s) LIMIT %s' % (','.join(idlist), str(len(idlist))))
                if obj.relative:
                    for robj in obj.relative:
                        robj.slug = slugfy(robj.title)
        # get comment
        obj.coms = []
        if obj.comment_num > 0:
            if obj.comment_num >= EACH_PAGE_COMMENT_NUM:
                first_limit = EACH_PAGE_COMMENT_NUM
            else:
                first_limit = obj.comment_num
            obj.coms = Comment.get_post_page_comments_by_id(obj.id, 0, first_limit)
    return obj

def comment_format(objs):
    for obj in objs:
        obj.gravatar = 'http://www.gravatar.com/avatar/%s' % md5(obj.email).hexdigest()
        obj.add_time = time_from_now(int(obj.add_time))
        
        if obj.visible:
            obj.short_content = HTML_REG.sub('', obj.content[:RECENT_COMMENT_CUT_WORDS])
        else:
            obj.short_content = 'Your comment is awaiting moderation.'[:RECENT_COMMENT_CUT_WORDS]
        
        obj.content = obj.content.replace('\n', '<br/>')
    return objs



class Article():
    @staticmethod
    @sta
    def get_max_id(db):
        
        maxobj = db.query("select max(id) as maxid from `sp_posts`")
        return str(maxobj[0]['maxid'])
    @staticmethod
    @sta
    def get_last_post_add_time(db):
        
        obj = db.get('SELECT `add_time` FROM `sp_posts` ORDER BY `id` DESC LIMIT 1')
        if obj:
            return datetime.fromtimestamp(obj.add_time)
        else:
            return datetime.utcnow() + timedelta(hours= +8)
    @staticmethod
    @sta
    def count_all_post(db):
        
        return db.query('SELECT COUNT(*) AS postnum FROM `sp_posts`')[0]['postnum']
    @staticmethod
    @sta
    def get_all_article(db):
        return post_list_format(db.query("SELECT * FROM `sp_posts` ORDER BY `id` DESC"))
    @staticmethod
    @sta
    def get_post_for_homepage(db):
        
        return post_list_format(db.query("SELECT * FROM `sp_posts` ORDER BY `id` DESC LIMIT %s" % str(EACH_PAGE_POST_NUM)))
    @staticmethod
    @sta
    def get_page_posts(db, direction='next', page=1 , base_id='', limit=EACH_PAGE_POST_NUM):
        
        if direction == 'next':
            return post_list_format(db.query("SELECT * FROM `sp_posts` WHERE `id` < %s ORDER BY `id` DESC LIMIT %s" % (str(base_id), str(EACH_PAGE_POST_NUM))))
        else:
            return post_list_format(db.query("SELECT * FROM `sp_posts` WHERE `id` > %s ORDER BY `id` ASC LIMIT %s" % (str(base_id), str(EACH_PAGE_POST_NUM))))
    @staticmethod
    @sta
    def get_article_by_id_detail(db, id):
        
        return post_detail_formate(db.get('SELECT * FROM `sp_posts` WHERE `id` = %s LIMIT 1' % str(id)))
    @staticmethod
    @sta
    def get_article_by_id_simple(db, id):
        
        return db.get('SELECT `id`,`title`,`comment_num`,`closecomment`,`password` FROM `sp_posts` WHERE `id` = %s LIMIT 1' % str(id))
    @staticmethod
    @sta
    def get_article_by_id_edit(db, id):
        
        return db.get('SELECT * FROM `sp_posts` WHERE `id` = %s LIMIT 1' % str(id))
    @staticmethod
    @mta
    def add_new_post(db, params):
        query = "INSERT INTO `sp_posts` (`category`,`title`,`content`,`closecomment`,`tags`,`password`,`add_time`,`edit_time`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        
        return db.execute(query, params['category'], params['title'], params['content'], params['closecomment'], params['tags'], params['password'], params['add_time'], params['edit_time'])
    @staticmethod
    @mta
    def update_post_edit(db, params):
        query = "UPDATE `sp_posts` SET `category` = %s, `title` = %s, `content` = %s, `closecomment` = %s, `tags` = %s, `password` = %s, `edit_time` = %s WHERE `id` = %s LIMIT 1"
        
        db.execute(query, params['category'], params['title'], params['content'], params['closecomment'], params['tags'], params['password'], params['edit_time'], params['id'])
        # ## update 返回不了 lastrowid，直接返回 post id
        return params['id']
    @staticmethod
    @mta        
    def update_post_comment(db, num=1, id=''):
        query = "UPDATE `sp_posts` SET `comment_num` = %s WHERE `id` = %s LIMIT 1"
        
        return db.execute(query, num, id)
    @staticmethod
    @sta         
    def get_post_for_sitemap(db, ids=[]):
        
        return db.query("SELECT `id`,`edit_time` FROM `sp_posts` WHERE `id` in(%s) ORDER BY `id` DESC LIMIT %s" % (','.join(ids), str(len(ids))))
    @staticmethod
    @mta            
    def del_post_by_id(db, id=''):
        if id:
            obj = db.get_article_by_id_simple(id)
            if obj:
                limit = obj.comment_num
                
                db.execute("DELETE FROM `sp_posts` WHERE `id` = %s LIMIT 1", id)
                db.execute("DELETE FROM `sp_comments` WHERE `postid` = %s LIMIT %s", id, limit)
                


class Comment():
    @staticmethod
    @mta        
    def del_comment_by_id(db, id):
        cobj = db.get_comment_by_id(id)
        postid = cobj.postid
        pobj = Article.get_article_by_id_edit(db, postid)
        
        
        db.execute("DELETE FROM `sp_comments` WHERE `id` = %s LIMIT 1", id)
        if pobj:
            Article.update_post_comment(db, pobj.comment_num - 1, postid)
        return
    @staticmethod
    @sta           
    def get_comment_by_id(db, id):
        
        return db.get('SELECT * FROM `sp_comments` WHERE `id` = %s LIMIT 1' % str(id))
    @staticmethod
    @sta        
    def get_recent_comments(db, limit=RECENT_COMMENT_NUM):
        
        return comment_format(db.query('SELECT * FROM `sp_comments` ORDER BY `id` DESC LIMIT %s' % str(limit)))
    @staticmethod
    @sta    
    def get_post_page_comments_by_id(db, postid=0, min_comment_id=0, limit=EACH_PAGE_COMMENT_NUM):
        
        if min_comment_id == 0:
            
            return comment_format(db.query('SELECT * FROM `sp_comments` WHERE `postid`= %s ORDER BY `id` DESC LIMIT %s' % (str(postid), str(limit))))
        else:
            
            return comment_format(db.query('SELECT * FROM `sp_comments` WHERE `postid`= %s AND `id` < %s ORDER BY `id` DESC LIMIT %s' % (str(postid), str(min_comment_id), str(limit))))
    @staticmethod
    @mta        
    def add_new_comment(db, params):
        query = "INSERT INTO `sp_comments` (`postid`,`author`,`email`,`url`,`visible`,`add_time`,`content`) values(%s,%s,%s,%s,%s,%s,%s)"
        
        return db.execute(query, params['postid'], params['author'], params['email'], params['url'], params['visible'], params['add_time'], params['content'])
    @staticmethod
    @mta        
    def update_comment_edit(db, params):
        query = "UPDATE `sp_comments` SET `author` = %s, `email` = %s, `url` = %s, `visible` = %s, `content` = %s WHERE `id` = %s LIMIT 1"
        
        db.execute(query, params['author'], params['email'], params['url'], params['visible'], params['content'], params['id'])
        # ## update 返回不了 lastrowid，直接返回 id
        return params['id']
    

class Tag():
    @staticmethod
    @sta
    def get_all_tag_name(db):
        # for add/edit post
        
        return db.query('SELECT `name` FROM `sp_tags` ORDER BY `id` DESC LIMIT %d' % HOT_TAGS_NUM)
    @staticmethod
    @sta
    def get_all_tag(db):
        
        return db.query('SELECT * FROM `sp_tags` ORDER BY `id` DESC LIMIT %d' % HOT_TAGS_NUM)
    @staticmethod
    @sta    
    def get_hot_tag_name(db):
        # for sider
        
        return db.query('SELECT `name`,`id_num` FROM `sp_tags` ORDER BY `id_num` DESC LIMIT %d' % HOT_TAGS_NUM)
    @staticmethod
    @sta    
    def get_tag_by_name(db, name=''):
        
        return db.get('SELECT * FROM `sp_tags` WHERE `name` = \'%s\' LIMIT 1' % name)
    @staticmethod
    @sta
    def get_all_post_num(db, name=''):
        obj = db.get_tag_by_name(name)
        if obj and obj.content:
            return len(obj.content.split(','))
        else:
            return 0
    @staticmethod
    @sta        
    def get_tag_page_posts(db, name='', page=1, limit=EACH_PAGE_POST_NUM):
        obj = db.get_tag_by_name(name)
        if obj and obj.content:
            page = int(page)
            idlist = obj.content.split(',')
            getids = idlist[limit * (page - 1):limit * page]
            
            return post_list_format(db.query("SELECT * FROM `sp_posts` WHERE `id` in(%s) ORDER BY `id` DESC LIMIT %s" % (','.join(getids), len(getids))))
        else:
            return []
    @staticmethod
    @mta           
    def add_postid_to_tags(db, tags=[], postid=''):
        
        for tag in tags:
            obj = db.get('SELECT * FROM `sp_tags` WHERE `name` = \'%s\' LIMIT 1' % tag)
            
            if obj:
                query = "UPDATE `sp_tags` SET `id_num` = `id_num` + 1, `content` =  concat(%s, `content`) WHERE `id` = %s LIMIT 1"
                db.execute(query, "%s," % postid, obj.id)
            else:
                query = "INSERT INTO `sp_tags` (`name`,`id_num`,`content`) values(%s,1,%s)"
                db.execute(query, tag, postid)
    @staticmethod
    @mta        
    def remove_postid_from_tags(db, tags=[], postid=''):
        
        for tag in tags:
            obj = db.get('SELECT * FROM `sp_tags` WHERE `name` = \'%s\' LIMIT 1' % tag)
            
            if obj:
                idlist = obj.content.split(',')
                if postid in idlist:
                    idlist.remove(postid)
                    try:
                        idlist.remove('')
                    except:
                        pass
                    if len(idlist) == 0:
                        db.execute("DELETE FROM `sp_tags` WHERE `id` = %s LIMIT 1", obj.id)
                    else:
                        query = "UPDATE `sp_tags` SET `id_num` = %s, `content` =  %s WHERE `id` = %s LIMIT 1"
                        db.execute(query, len(idlist), ','.join(idlist), obj.id)                
                else:
                    pass            
    

class Link():
    @staticmethod
    @sta
    def get_all_links(db, limit=LINK_NUM):
        db._ensure_connected()
        return db.query('SELECT * FROM `sp_links` ORDER BY `displayorder` DESC LIMIT %s' % str(limit))
    @staticmethod
    @mta    
    def add_new_link(db, params):
        query = "INSERT INTO `sp_links` (`displayorder`,`name`,`url`) values(%s,%s,%s)"
        db._ensure_connected()
        return db.execute(query, params['displayorder'], params['name'], params['url'])
    @staticmethod
    @mta    
    def update_link_edit(db, params):
        query = "UPDATE `sp_links` SET `displayorder` = %s, `name` = %s, `url` = %s WHERE `id` = %s LIMIT 1"
        db._ensure_connected()
        db.execute(query, params['displayorder'], params['name'], params['url'], params['id'])
    @staticmethod
    @mta    
    def del_link_by_id(db, id):
        db._ensure_connected()
        db.execute("DELETE FROM `sp_links` WHERE `id` = %s LIMIT 1", id)
    @staticmethod
    @sta        
    def get_link_by_id(db, id):
        db._ensure_connected()
        return db.get('SELECT * FROM `sp_links` WHERE `id` = %s LIMIT 1' % str(id))    


class Category():
    @staticmethod
    @sta
    def get_all_cat_name(db):
        db._ensure_connected()
        return db.query('SELECT `name`,`id_num` FROM `sp_category` ORDER BY `id` DESC')
    @staticmethod
    @sta        
    def get_all_cat(db):
        db._ensure_connected()
        return db.query('SELECT * FROM `sp_category` ORDER BY `id` DESC')
    @staticmethod
    @sta    
    def get_all_cat_id(db):
        db._ensure_connected()
        return db.query('SELECT `id` FROM `sp_category` ORDER BY `id` DESC')
    @staticmethod
    @sta    
    def get_cat_by_name(db, name=''):
        db._ensure_connected()
        return db.get('SELECT * FROM `sp_category` WHERE `name` = \'%s\' LIMIT 1' % name)
    @staticmethod
    @sta            
    def get_all_post_num(db, name=''):
        obj = db.get_cat_by_name(name)
        if obj and obj.content:
            return len(obj.content.split(','))
        else:
            return 0
    @staticmethod
    @sta        
    def get_cat_page_posts(db, name='', page=1, limit=EACH_PAGE_POST_NUM):
        obj = db.get_cat_by_name(name)
        if obj:
            page = int(page)
            idlist = obj.content.split(',')
            getids = idlist[limit * (page - 1):limit * page]
            db._ensure_connected()
            return post_list_format(db.query("SELECT * FROM `sp_posts` WHERE `id` in(%s) ORDER BY `id` DESC LIMIT %s" % (','.join(getids), str(len(getids)))))
        else:
            return []
    @staticmethod
    @mta            
    def add_postid_to_cat(db, name='', postid=''):
        db._ensure_connected()
        # 因为 UPDATE 时无论有没有影响行数，都返回0，所以这里要多读一次（从主数据库读）
        obj = db.get('SELECT * FROM `sp_category` WHERE `name` = \'%s\' LIMIT 1' % name)        
        
        if obj:
            query = "UPDATE `sp_category` SET `id_num` = `id_num` + 1, `content` =  concat(%s, `content`) WHERE `id` = %s LIMIT 1"
            db.execute(query, "%s," % postid, obj.id)
        else:
            query = "INSERT INTO `sp_category` (`name`,`id_num`,`content`) values(%s,1,%s)"
            db.execute(query, name, postid)
    @staticmethod
    @mta    
    def remove_postid_from_cat(db, name='', postid=''):
        db._ensure_connected()
        obj = db.get('SELECT * FROM `sp_category` WHERE `name` = \'%s\' LIMIT 1' % name)        
        if obj:
            idlist = obj.content.split(',')
            if postid in idlist:
                idlist.remove(postid)
                try:
                    idlist.remove('')
                except:
                    pass
                if len(idlist) == 0:
                    db.execute("DELETE FROM `sp_category` WHERE `id` = %s LIMIT 1", obj.id)
                else:
                    query = "UPDATE `sp_category` SET `id_num` = %s, `content` =  %s WHERE `id` = %s LIMIT 1"
                    db.execute(query, len(idlist), ','.join(idlist), obj.id)                
            else:
                pass
    @staticmethod
    @sta    
    def get_cat_by_id(db, id=''):
        db._ensure_connected()
        return db.get('SELECT * FROM `sp_category` WHERE `id` = %s LIMIT 1' % str(id))
    @staticmethod
    @sta    
    def get_sitemap_by_id(db, id=''):
        
        obj = db.get_cat_by_id(id)
        if not obj:
            return ''
        if not obj.content:
            return ''
        
        urlstr = """<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n """        
        urllist = []
        urllist.append('<?xml version="1.0" encoding="UTF-8"?>\n')
        urllist.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        
        urllist.append(urlstr % ("%s/c/%s" % (BASE_URL, str(obj.id)), cnnow().strftime("%Y-%m-%dT%H:%M:%SZ"), 'daily', '0.8'))
        
        objs = Article.get_post_for_sitemap(db, obj.content.split(','))
        for p in objs:
            if p:
                urllist.append(urlstr % ("%s/t/%s" % (BASE_URL, str(p.id)), timestamp_to_datetime(p.edit_time).strftime("%Y-%m-%dT%H:%M:%SZ"), 'weekly', '0.6'))
        
        urllist.append('</urlset>')
        return ''.join(urllist)
    
 
