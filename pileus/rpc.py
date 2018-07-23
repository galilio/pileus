import threading
from functools import wraps
from nameko.standalone.rpc import ClusterRpcProxy

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
