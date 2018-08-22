#-*- encoding: utf-8
import bottle
from bottle import route, get, post, delete, put, response, abort, request, Bottle
from bottle import run
from bottle import HTTPError
from .async import async
from .rpc import rpc, proxy, DynamicRpcProxy, ServiceNotRegisterException
from .cache import cache
from .nameko_redis import Redis

app = bottle.default_app()


request_method = ['get', 'post', 'delete', 'put', 'response', 'abort', 'request', 'HTTPError']

def bp():
    return Bottle()



__all__ = ['async', 'route', 'app', 'run', 'bp', 'cache', 'Redis']
__all__ += request_method
__all__ += ['rpc', 'proxy', 'DynamicRpcProxy', 'ServiceNotRegisterException']
