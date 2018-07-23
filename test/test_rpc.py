import unittest

from pileus import rpc, proxy

proxy.config('localhost', 'guest', 'guest')

@rpc
def call_rpc_method():
    print(proxy)
    print(proxy.rpc_proxy)
    proxy.authorize_service.register('test5', 'test')

class TestAsync(unittest.TestCase):
    def test_rpc(self):
        call_rpc_method()

if __name__ == '__main__':
    unittest.main()