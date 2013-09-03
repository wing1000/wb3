#!/usr/bin/env python
# coding=utf-8

from commons import BaseHandler
from time import time

class IndexAction(BaseHandler):
    def get(self):
        self.echo('home.html', {
            'title': "测试",
            'name': "name text",
            'timestamp':  int(time()),
            'html_text': "<h1>H1标签</h1>",
        })


class NotFoundPage(BaseHandler):
    def get(self):
        self.set_status(404)
        self.write("404: Not found")


class Timeline(BaseHandler):
    def get(self):
        self.echo('timeline.html', {
            'title': "测试",
            'name': "name text",
            'timestamp':  int(time()),
            'html_text': "<h1>H1标签</h1>",
        },layout="empty_layout.html")

class Test(BaseHandler):
    def get(self):
        self.echo('test.html', {
            'title': "测试",
            'name': "name text",
            'timestamp':  int(time()),
            'html_text': "<h1>H1标签</h1>",
        },layout="empty_layout.html")
        
class Timeline2(BaseHandler):
    def get(self):
        self.echo('timeline2.html', {
            'title': "测试",
            'name': "name text",
            'timestamp':  int(time()),
            'html_text': "<h1>H1标签</h1>",
        },layout=False)

