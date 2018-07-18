#!/usr/bin/env python

from bottle import route, run
@route('/index')
def hello():
    return 'hello world'

run(host = '127.0.0.1', port = 8080, debug = True)

