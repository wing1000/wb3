#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-7-5

@author: tietang
'''
#!/usr/bin/python

#coding=utf-8
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
