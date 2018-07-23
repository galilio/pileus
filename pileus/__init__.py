#-*- encoding: utf-8
import bottle
from bottle import route, get, post, delete, put, response, abort, request, Bottle
from bottle import run
from bottle import HTTPError
from .async import async
from .rpc import rpc, proxy

app = bottle.default_app()


request_method = ['get', 'post', 'delete', 'put', 'response', 'abort', 'request', 'HTTPError']

def bp():
    return Bottle()

__all__ = ['async', 'route', 'app', 'run', 'bp', 'rpc', 'proxy'] + request_method