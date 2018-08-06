from pileus import cache
import unittest
from nameko.rpc import rpc
from nameko.testing.services import worker_factory
from functools import wraps
from pileus import Redis

class TestService(object):
    name = 'test_service'
    # cache = Cache()
    redis = Redis('default', decode_responses = False)

    @rpc
    @cache()
    def hello(self):
        print('fetch from func calls.')
        return ['test', 'test2']

class TestCache(unittest.TestCase):
    def test_cache(self):
        service = worker_factory(TestService)
        v = service.hello()
        print('xxxxxx', v)

if __name__ == '__main__':
    unittest.main()