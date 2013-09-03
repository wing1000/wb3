# -*- coding: utf-8 -*-

import logging

import json
    
from hashlib import md5
from time import time

from setting import *


from commons import *

from models import Article, Comment, Link, Category, Tag

###############
class HomePage(BaseHandler):
    
    def get(self):
        try:
            objs = Article.get_post_for_homepage()
        except:
            self.redirect('/install')
            return
        if objs:
            fromid = objs[0].id
            endid = objs[-1].id
        else:
            fromid = endid = ''
        
        allpost =  Article.count_all_post()
        allpage = allpost/EACH_PAGE_POST_NUM
        if allpost%EACH_PAGE_POST_NUM:
            allpage += 1


        output = self.render('index.html', {
            'title': "%s - %s"%(SITE_TITLE,SITE_SUB_TITLE),
            'keywords':KEYWORDS,
            'description':SITE_DECR,
            'objs': objs,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': 1,
            'allpage': allpage,
            'listtype': 'index',
            'fromid': fromid,
            'endid': endid,
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        print '---------------------------------------'
        self.write(output)
        print '---------------------------------------'
#         return output

class IndexPage(BaseHandler):
     
    def get(self, direction = 'next', page = '2', base_id = '1'):
        if page == '1':
            self.redirect(BASE_URL)
            return
        objs = Article.get_page_posts(direction, page, base_id)
        if objs:
            if direction == 'prev':
                objs.reverse()            
            fromid = objs[0].id
            endid = objs[-1].id
        else:
            fromid = endid = ''
        
        allpost =  Article.count_all_post()
        allpage = allpost/EACH_PAGE_POST_NUM
        if allpost%EACH_PAGE_POST_NUM:
            allpage += 1
        output = self.render('index.html', {
            'title': "%s - %s | Part %s"%(SITE_TITLE,SITE_SUB_TITLE, page),
            'keywords':KEYWORDS,
            'description':SITE_DECR,
            'objs': objs,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': int(page),
            'allpage': allpage,
            'listtype': 'index',
            'fromid': fromid,
            'endid': endid,
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        self.write(output)
        return output
        
class PostDetailShort(BaseHandler):
    @client_cache(600, 'public')
    def get(self, id = ''):
        obj = Article.get_article_by_id_simple(id)
        if obj:
            self.redirect('%s/topic/%d/%s'% (BASE_URL, obj.id, obj.title), 301)
            return
        else:
            self.redirect(BASE_URL)

class PostDetail(BaseHandler):
  
    def get(self, id = '', title = ''):
        tmpl = ''
        obj = Article.get_article_by_id_detail(id)
        if not obj:
            self.redirect(BASE_URL)
            return
        #redirect to right title
        try:
            title = unquote(title).decode('utf-8')
        except:
            pass
        if title != obj.slug:
            self.redirect(obj.absolute_url, 301)
            return        
        #
        if obj.password and THEME == 'default':
            rp = self.get_cookie("rp%s" % id, '')
            if rp != obj.password:
                tmpl = '_pw'
        
        
        self.set_header("Last-Modified", obj.last_modified)
            
        output = self.render('page%s.html'%tmpl, {
            'title': "%s - %s"%(obj.title, SITE_TITLE),
            'keywords':obj.keywords,
            'description':obj.description,
            'obj': obj,
            'cobjs': obj.coms,
            'postdetail': 'postdetail',
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': 1,
            'allpage': 10,
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        self.write(output)
        
        if obj.password and THEME == 'default':
            return
        else:
            return output
        
    def post(self, id = '', title = ''):
        action = self.get_argument("act")
        
        if action == 'inputpw':
            wrn = self.get_cookie("wrpw", '0')
            if int(wrn)>=10:
                self.write('403')
                return
            
            pw = self.get_argument("pw",'')
            pobj = Article.get_article_by_id_simple(id)
            wr = False
            if pw:             
                if pobj.password == pw:
                    self.set_cookie("rp%s" % id, pobj.password, path = "/", expires_days =1)
                else:
                    wr = True
            else:
                wr = True
            if wr:
                wrn = self.get_cookie("wrpw", '0')
                self.set_cookie("wrpw", str(int(wrn)+1), path = "/", expires_days = 1 )
            
            self.redirect('%s/topic/%d/%s'% (BASE_URL, pobj.id, pobj.title))
            return
        
        self.set_header('Content-Type','application/json')
        rspd = {'status': 201, 'msg':'ok'}
        
        if action == 'readmorecomment':
            fromid = self.get_argument("fromid",'')
            allnum = int(self.get_argument("allnum",0))
            showednum = int(self.get_argument("showednum", EACH_PAGE_COMMENT_NUM))
            if fromid:
                rspd['status'] = 200
                if (allnum - showednum) >= EACH_PAGE_COMMENT_NUM:
                    limit = EACH_PAGE_COMMENT_NUM
                else:
                    limit = allnum - showednum
                cobjs = Comment.get_post_page_comments_by_id( id, fromid, limit )
                rspd['commentstr'] = self.render('comments.html', {'cobjs': cobjs})
                rspd['lavenum'] = allnum - showednum - limit
                self.write(json.dumps(rspd))
            return
        
        #
        usercomnum = self.get_cookie('usercomnum','0')
        if int(usercomnum) > MAX_COMMENT_NUM_A_DAY:
            rspd = {'status': 403, 'msg':'403: Forbidden'}
            self.write(json.dumps(rspd))
            return
        
        try:
            timestamp = int(time())
            post_dic = {
                'author': self.get_argument("author"),
                'email': self.get_argument("email"),
                'content': safe_encode(self.get_argument("con").replace('\r','\n')),
                'url': self.get_argument("url",''),
                'postid': self.get_argument("postid"),
                'add_time': timestamp,
                'toid': self.get_argument("toid",''),
                'visible': COMMENT_DEFAULT_VISIBLE
            }
        except:
            rspd['status'] = 500
            rspd['msg'] = '错误： 注意必填的三项'
            self.write(json.dumps(rspd))
            return
        
        pobj = Article.get_article_by_id_simple(id)
        if pobj and not pobj.closecomment:
            cobjid = Comment.add_new_comment(post_dic)
            if cobjid:
                Article.update_post_comment( pobj.comment_num+1, id)
                rspd['status'] = 200
                #rspd['msg'] = '恭喜： 已成功提交评论'
                
                rspd['msg'] = self.render('comment.html', {
                        'cobjid': cobjid,
                        'gravatar': 'http://www.gravatar.com/avatar/%s'%md5(post_dic['email']).hexdigest(),
                        'url': post_dic['url'],
                        'author': post_dic['author'],
                        'visible': post_dic['visible'],
                        'content': post_dic['content'],
                    })
                
#                 clear_cache_by_pathlist(['/','post:%s'%id])
                #send mail
                if not debug:
                    try:
                        if NOTICE_MAIL:
                            tolist = [NOTICE_MAIL]
                        else:
                            tolist = []
                        if post_dic['toid']:
                            toid=post_dic['toid']
                            tcomment = Comment.get_comment_by_id(toid)
                            if tcomment and tcomment.email:
                                tolist.append(tcomment.email)
                        commenturl = "%s/t/%s#r%s" % (BASE_URL, str(pobj.id), str(cobjid))
                        m_subject = u'有人回复您在 《%s》 里的评论 %s' % ( pobj.title,str(cobjid))
                        m_html = u'这是一封提醒邮件（请勿直接回复）： %s ，请尽快处理： %s' % (m_subject, commenturl)
                        
                        if tolist:
                            import sae.mail
                            sae.mail.send_mail(','.join(tolist), m_subject, m_html,(MAIL_SMTP, int(MAIL_PORT), MAIL_FROM, MAIL_PASSWORD, True))          
                        
                    except:
                        pass
            else:
                rspd['msg'] = '错误： 未知错误'
        else:
            rspd['msg'] = '错误： 未知错误'
        self.write(json.dumps(rspd))

class CategoryDetailShort(BaseHandler):
    @client_cache(3600, 'public')
    def get(self, id = ''):
        obj = Category.get_cat_by_id(id)
        if obj:
            self.redirect('%s/category/%s'% (BASE_URL, obj.name), 301)
            return
        else:
            self.redirect(BASE_URL)

class CategoryDetail(BaseHandler):
    def get(self, name = ''):
        objs = Category.get_cat_page_posts(name, 1)
        
        catobj = Category.get_cat_by_name(name)
        if catobj:
            pass
        else:
            self.redirect(BASE_URL)
            return
        
        allpost =  catobj.id_num
        allpage = allpost/EACH_PAGE_POST_NUM
        if allpost%EACH_PAGE_POST_NUM:
            allpage += 1
            
        output = self.render('index.html', {
            'title': "%s - %s"%( catobj.name, SITE_TITLE),
            'keywords':catobj.name,
            'description':SITE_DECR,
            'objs': objs,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': 1,
            'allpage': allpage,
            'listtype': 'cat',
            'name': name,
            'namemd5': md5(name.encode('utf-8')).hexdigest(),
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        self.write(output)
        return output

class TagDetail(BaseHandler):
    
    def get(self, name = ''):
        objs = Tag.get_tag_page_posts(name, 1)
        
        catobj = Tag.get_tag_by_name(name)
        if catobj:
            pass
        else:
            self.redirect(BASE_URL)
            return
        
        allpost =  catobj.id_num
        allpage = allpost/EACH_PAGE_POST_NUM
        if allpost%EACH_PAGE_POST_NUM:
            allpage += 1
            
        output = self.render('index.html', {
            'title': "%s - %s"%( catobj.name, SITE_TITLE),
            'keywords':catobj.name,
            'description':SITE_DECR,
            'objs': objs,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': 1,
            'allpage': allpage,
            'listtype': 'tag',
            'name': name,
            'namemd5': md5(name.encode('utf-8')).hexdigest(),
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        self.write(output)
        return output
        

class ArticleList(BaseHandler):
    def get(self, listtype = '', direction = 'next', page = '1', name = ''):
        if listtype == 'cat':
            objs = Category.get_cat_page_posts(name, page)
            catobj = Category.get_cat_by_name(name)
        else:
            objs = Tag.get_tag_page_posts(name, page)
            catobj = Tag.get_tag_by_name(name)
        
        #
        if catobj:
            pass
        else:
            self.redirect(BASE_URL)
            return
        
        allpost =  catobj.id_num
        allpage = allpost/EACH_PAGE_POST_NUM
        if allpost%EACH_PAGE_POST_NUM:
            allpage += 1
            
        output = self.render('index.html', {
            'title': "%s - %s | Part %s"%( catobj.name, SITE_TITLE, page),
            'keywords':catobj.name,
            'description':SITE_DECR,
            'objs': objs,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_hot_tag_name(),
            'page': int(page),
            'allpage': allpage,
            'listtype': listtype,
            'name': name,
            'namemd5': md5(name.encode('utf-8')).hexdigest(),
            'comments': Comment.get_recent_comments(),
            'links':Link.get_all_links(),
        },layout='_layout.html')
        self.write(output)
        return output
        
        
class Robots(BaseHandler):
    def get(self):
        self.echo('robots.txt',{'cats':Category.get_all_cat_id()})

class Feed(BaseHandler):
    def get(self):
        posts = Article.get_post_for_homepage()
        output = self.render('index.xml', {
                    'posts':posts,
                    'site_updated':Article.get_last_post_add_time(),
                })
        self.set_header('Content-Type','application/atom+xml')
        self.write(output)        

class Sitemap(BaseHandler):
    def get(self, id = ''):
        self.set_header('Content-Type','text/xml')
        self.echo('sitemap.html', {'sitemapstr':Category.get_sitemap_by_id(id), 'id': id})


class Attachment(BaseHandler):
    def get(self, name):
        self.redirect('http://%s-%s.stor.sinaapp.com/%s'% (APP_NAME, STORAGE_DOMAIN_NAME, unquoted_unicode(name)), 301)
        return
        
########
