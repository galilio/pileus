#-*- encoding: utf-8
import bottle
from bottle import route, get, post, delete, put, response, abort, request, Bottle
from bottle import HTTPError
from .async import async

app = bottle.default_app()


request_method = ['get', 'post', 'delete', 'put', 'response', 'abort', 'request', 'HTTPError']

def bp():
    return Bottle()

__all__ = ['async', 'route', 'app', 'bp'] + request_method