import unittest

from pileus import DynamicRpcProxy
from nameko.rpc import rpc
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.dependency_providers import Config

class ServiceA(object):
    name = 'service_a'
    drp = DynamicRpcProxy()

    @rpc
    def wawa(self):
        self.drp['service_b'].hello()

