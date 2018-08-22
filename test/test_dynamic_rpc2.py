import unittest

from pileus import DynamicRpcProxy
from nameko.rpc import rpc, RpcProxy

from nameko.dependency_providers import Config

class ServiceB(object):
    name = 'service_b'

    a = RpcProxy('service_a')

    @rpc
    def hello(self):
        print('hello all')