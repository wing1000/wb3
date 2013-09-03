import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
from time import time
from datetime import date
from actions import *
from setting import *
########
 

urls = [
    (r"/", IndexAction),
    (r"/test", Test),
    (r"/upload", UploadPage),
    (r"/photos/(.*)", Img),
    (r"/blog", BlogPage),
    
    (r"/robots.txt", Robots),
    (r"/feed", Feed),
    (r"/index.xml", Feed),
    (r"/t/(\d+)$", PostDetailShort),
    (r"/topic/(\d+)/(.*)$", PostDetail),
    (r"/index_(prev|next)_page/(\d+)/(\d+)/$", IndexPage),
    (r"/c/(\d+)$", CategoryDetailShort),
    (r"/category/(.+)/$", CategoryDetail),
    (r"/tag/(.+)/$", TagDetail),
    (r"/(cat|tag)_(prev|next)_page/(\d+)/(.+)/$", ArticleList),
    (r"/sitemap_(\d+)\.xml$", Sitemap),
    (r"/attachment/(.+)$", Attachment),
    
     (r"/timeline", Timeline),
    (r"/timeline2", Timeline2),
    (r"/timeline3", Timeline2),
    (r".*", NotFoundPage),
]


def hk():
    print date.today()
    
    
application = tornado.web.Application(urls, **settings)



if __name__ == "__main__":
#     http_server = tornado.httpserver.HTTPServer(application)
#     http_server.listen(HTTP_PORT,address="172.17.20.98")
#     tornado.autoreload.add_reload_hook(hk)
    application.listen(HTTP_PORT);
    instance = tornado.ioloop.IOLoop.instance()
    logging.info("start python http server on port {0}.".format(HTTP_PORT))
    instance.start()

