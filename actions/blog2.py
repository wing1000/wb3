#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-28

@author: tietang
'''
from setting import *
from commons import BaseHandler
from time import time
from tornado.web import *
import os
from setting import *

class BlogPage(BaseHandler):
    def get(self):
        self.echo('add.html', {
            'title': "添加文章"
        })
        
    def post(self):
        context = {}
        self.echo("add.html", context=context)  

save_path = "uploads/"


class Img(StaticFileHandler):
 
    pass
      
class UploadPage(BaseHandler):
    def get(self):
        list = []
        for file in os.listdir(save_path): 
            path = os.path.join(save_path, file) 
            if not os.path.isdir(path): 
                list.append(path)
                
        self.echo('upload.html', {
            'title': "上传",
            "list":list
        })
        
    def post(self):
        files = self.request.files['filedata']
        for file in files:
            fname = file['filename']
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
            output_file = open(save_path + fname, 'wb')
            output_file.write(file['body'])

        self.finish({"success."})
        
        

class UploadHandler(RequestHandler):
 
 
    def post(self):
        files = self.request.files['imgFile']
        for file in files:
            fname = file['filename']
            if not os.path.isdir(save_path):
                os.makedirs(save_path)

            output_file = open(save_path + fname, 'wb')
            output_file.write(file['body'])
        #         //成功时
        
        s = {
                "error" : 0,
                "url" : BASE_URL + "/uploads/" + fname
        }
#         //失败时
        f = {
                "error" : 1,
                "message" : "错误信息"
        }
        self.finish(s)
