# -*- coding: utf-8 -*-

import os.path

import tornado.web


import tenjin

from tenjin.helpers import *

from setting import *


class BaseHandler(tornado.web.RequestHandler):
    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        context.update({
            'request':self.request,
        })
        if Engine.layout and (not layout):
            layout=Engine.layout  
        return Engine.render(template, context, globals, layout)
    
    def echo(self, template, context=None, globals=None, layout=False):
        self.write(self.render(template, context, globals, layout))    

