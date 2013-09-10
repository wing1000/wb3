# -*- coding: utf-8 -*-
from os import environ
import os.path
import os

import tenjin

from tenjin.helpers import *


WB3_VERSION = '1.0'  # 当前版本
APP_NAME = environ.get("APP_NAME", "WB3")
debug = not APP_NAME
HTTP_PORT = 9876
##下面需要修改
SITE_TITLE = u"博客标题" #博客标题
SITE_TITLE2 = u"博客标题2" #显示在边栏上头（有些模板用不到）
SITE_SUB_TITLE = u"一个简单的运行在SAE上的blog" #副标题
KEYWORDS = u"起床,吃饭,工作,睡觉" #博客关键字
SITE_DECR = u"这是运行在SAE上的个人博客，记录生活，记录工作。" #博客描述，给搜索引擎看
ADMIN_NAME = u"admin" #发博文的作者
NOTICE_MAIL = u"" #常用的，容易看到的接收提醒邮件，如QQ 邮箱，仅作收件用

###配置邮件发送信息，提醒邮件用的，必须正确填写，建议用Gmail
MAIL_FROM = '' #xxx@gmail.com
MAIL_SMTP = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_PASSWORD = 'xxx' #你的邮箱登录密码，用以发提醒邮件


# 设置theme 文件夹，均放在templates 下
# 注意：templates 里的模板文件是为了方便模板管理，
# 如果同时使用guest和admin，则不能包含相同的模板名称
# 否则只会调用THEMES 里第一个文件夹里出现的模板名，

THEMES = ['default']
THEME = 'default'

import socket

localIP = socket.gethostbyname(socket.gethostname())
print localIP

(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(socket.gethostname())

print "hostname %s" % hostname
print "ip address list:%s" % ipaddrlist
print aliaslist

BASE_URL = 'http://{0}:{1}'.format(localIP, HTTP_PORT)
####友情链接列表，在管理后台也实现了管理，下面的链接列表仍然有效并排在前面
LINK_BROLL = [
    {"text": 'SAEpy blog', "url": 'http://saepy.sinaapp.com'},
    {"text": 'Sina App Engine', "url": 'http://sae.sina.com.cn/'},
]
#使用SAE Storage 服务（保存上传的附件），需在SAE管理面板创建
STORAGE_DOMAIN_NAME = 'attachment'
# #配置Mysql 数据库信息

MasterDbConfig = {
    "host": "127.0.0.1:4000",
    "user": "root",
    "password": "",
    "database": "spruce"
}
SlaveDbConfig = {
    "host": "127.0.0.1:4000",
    "user": "root",
    "password": "",
    "database": "spruce"
}
poolConfig = {}


# redis
from redis_shard.shard import RedisShardAPI

RedisServers = {
    'node1': {'host': '127.0.0.1', 'port': 10000, 'db': 0},
    'node2': {'host': '127.0.0.1', 'port': 11000, 'db': 0},
    'node3': {'host': '127.0.0.1', 'port': 12000, 'db': 0},
}

redis = RedisShardAPI(RedisServers)

PATH = os.getcwd()
favicon_path = os.path.join(PATH, 'favicon.ico')

settings = {
    'debug': True,
    'static_path': os.path.join(PATH, 'static'),

}
Engine = tenjin.Engine(layout='_layout2.html', path=[os.path.join('views', theme) for theme in THEMES] + ['views'],
                       cache=tenjin.MemoryCacheStorage(), preprocess=True)
# if __name__ == "__main__":
#     html= Engine.render('home.html', {
#             'title': "测试",
#             'name': "name text",
#             'html_text': "<h1>H1标签</h1>",
#         },None,Engine.layout)
#     print html



LANGUAGE = 'zh-CN'
COMMENT_DEFAULT_VISIBLE = 1  # 0/1 #发表评论时是否显示 设为0时则需要审核才显示
EACH_PAGE_POST_NUM = 7  # 每页显示文章数
EACH_PAGE_COMMENT_NUM = 10  # 每页评论数
RELATIVE_POST_NUM = 5  # 显示相关文章数
SHORTEN_CONTENT_WORDS = 150  # 文章列表截取的字符数
DESCRIPTION_CUT_WORDS = 100  # meta description 显示的字符数
RECENT_COMMENT_NUM = 5  # 边栏显示最近评论数
RECENT_COMMENT_CUT_WORDS = 20  # 边栏评论显示字符数
LINK_NUM = 30  # 边栏显示的友情链接数
MAX_COMMENT_NUM_A_DAY = 10  # 客户端设置Cookie 限制每天发的评论数

PAGE_CACHE = not debug  # 本地没有Memcache 服务
PAGE_CACHE_TIME = 3600 * 24  # 默认页面缓存时间 

HOT_TAGS_NUM = 100  # 右侧热门标签显示数

MAX_IDLE_TIME = 5  # 数据库最大空闲时间 SAE文档说是30 其实更小，设为5，没问题就不要改了
