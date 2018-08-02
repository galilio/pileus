from nameko.extensions import DependencyProvider
from functools import wraps
from nameko.rpc import Rpc
from redis.client import StrictRedis
import inspect

import pickle

def __generate_redis_key(keys, *args, **kwargs):
    parts = []

    for key in keys:
        if isinstance(key, int):
            parts.append(str(args[key]))
        elif isinstance(key, str):
            parts.append(str(kwargs[key]))

    return parts

def __is_redis(obj):
    return isinstance(obj, StrictRedis)

def cache(prefix = 'bayesba', keys = [], timeout = 10 * 60):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < 1:
                raise Exception('只能用在nameko service的方法上')

            redis = None
            for _, member in inspect.getmembers(args[0], __is_redis):
                redis = member

            if not redis:
                raise Exception('需要引入redis依赖')

            parts = __generate_redis_key(keys, *args, **kwargs)
            parts.insert(0, func.__name__)
            if prefix:
                parts.insert(0, prefix)

            key = '-'.join(parts)
            if key:
                v = redis.get(key)
                if v:
                    return pickle.loads(v)

            v = func(*args, **kwargs)
            if v and key:
                redis.set(key, pickle.dumps(v))

            return v
        
        return wrapper
    return decorate
