import threading
import inspect
from functools import wraps
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.extensions import DependencyProvider
from nameko.rpc import ReplyListener, ServiceProxy
from nameko.utils.concurrency import SpawningSet

def local_property():
    ls = threading.local()
    def fget(self):
        try:
            return ls.var
        except AttributeError:
            raise RuntimeError("rpc context not initialized")
        
    def fset(self, value):
        if not value and hasattr(ls, 'var'):
            del ls.var
        
        if value:
            ls.var = value
    
    def fdel(self):
        del ls.var
    
    return property(fget, fset, fdel, 'Thread-local property')

def rpc(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        config = {
            'AMQP_URI': proxy.uri
        }
        with ClusterRpcProxy(config) as cluster_rpc:
            proxy.rpc_proxy = cluster_rpc
            ret = func(*args, **kwargs)
            proxy.rpc_proxy = None

        return ret
    return wrapped

class Proxy(object):
    rpc_proxy = local_property()
    def __init__(self):
        self.uri = "pyamqp://guest:guest@localhost"

    def config(self, host, user, pwd):
        self.uri = "pyamqp://{}:{}@{}".format(user, pwd, host)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            _proxy = super().__getattribute__('rpc_proxy')
            return _proxy.__getattr__(name)

proxy = Proxy()

class ServiceNotRegisterException(Exception):
    pass

class ClusterProxy(object):
    def __init__(self, worker_ctx, reply_listener):
        self.worker_ctx = worker_ctx
        self.reply_listener = reply_listener

    # pick your interface. this uses dict-like access to chose target service
    def __getitem__(self, name):
        return ServiceProxy(self.worker_ctx, name, self.reply_listener)


class DynamicRpcProxy(DependencyProvider):
    rpc_reply_listener = ReplyListener()

    def get_dependency(self, worker_ctx):
        return ClusterProxy(worker_ctx, self.rpc_reply_listener)

    
