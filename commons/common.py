# -*- coding: utf-8 -*-
# import logging
import re
import os.path
from traceback import format_exc
from urllib import unquote, quote, urlencode
from urlparse import urljoin, urlunsplit

from datetime import datetime, timedelta

import tenjin
from tenjin.helpers import *

from setting import *

import tornado.web



#####
def slugfy(text, separator='-'):
    text = text.lower()
    text = re.sub("[¿_\-　，。：；‘“’”【】『』§！－——＋◎＃￥％……※×（）《》？、÷]+", ' ', text)
    ret_list = []
    for c in text:
        ordnum = ord(c)
        if 47 < ordnum < 58 or 96 < ordnum < 123:
            ret_list.append(c)
        else:
            if re.search(u"[\u4e00-\u9fa5]", c):
                ret_list.append(c)
            else:
                ret_list.append(' ')
    ret = ''.join(ret_list)
    ret = re.sub(r"\ba\b|\ban\b|\bthe\b", '', ret)
    ret = ret.strip()
    ret = re.sub("[\s]+", separator, ret)
    return ret

def safe_encode(con):
    return con.replace("<", "&lt;").replace(">", "&gt;")

def safe_decode(con):
    return con.replace("&lt;", "<").replace("&gt;", ">")

def unquoted_unicode(string, coding='utf-8'):
    return unquote(string).decode(coding)

def quoted_string(unicode, coding='utf-8'):
    return quote(unicode.encode(coding))

def cnnow():
    return datetime.utcnow() + timedelta(hours= +8)

# get time_from_now
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def time_from_now(time):
    if isinstance(time, int):
        time = timestamp_to_datetime(time)
    # time_diff = datetime.utcnow() - time
    time_diff = cnnow() - time
    days = time_diff.days
    if days:
        if days > 730:
            return '%s years ago' % (days / 365)
        if days > 365:
            return '1 year ago'
        if days > 60:
            return '%s months ago' % (days / 30)
        if days > 30:
            return '1 month ago'
        if days > 14:
            return '%s weeks ago' % (days / 7)
        if days > 7:
            return '1 week ago'
        if days > 1:
            return '%s days ago' % days
        return '1 day ago'
    seconds = time_diff.seconds
    if seconds > 7200:
        return '%s hours ago' % (seconds / 3600)
    if seconds > 3600:
        return '1 hour ago'
    if seconds > 120:
        return '%s minutes ago' % (seconds / 60)
    if seconds > 60:
        return '1 minute ago'
    if seconds > 1:
        return '%s seconds ago' % seconds
    return '%s second ago' % seconds



def format_date(dt):
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')




def client_cache(seconds, privacy=None):
    def wrap(handler):
        def cache_handler(self, *args, **kw):
            self.set_cache(seconds, privacy)
            return handler(self, *args, **kw)
        return cache_handler
    return wrap


class Struct:
    '''
    if __name__ == '__main__':
    m = {"sss":3, "sss2":4, }
    s = Struct(**m)
    print s.sss2
    
    
    '''
    def __init__(self, **entries): 
        self.__dict__.update(entries)
