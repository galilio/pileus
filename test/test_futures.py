import unittest
import signal

from pileus import async
import time

def print_now(prefix, timeout = 10):
    print('{} current time {}'.format(prefix, time.ctime()))

    try:
        time.sleep(timeout)
    except:
        return timeout

    print('{} end time {}'.format(prefix, time.ctime()))
    return timeout

def add(a, b):
    return a + b

def exception():
    raise Exception()

def handler(sig, strace):
    raise Exception('test')

class TestAsync(unittest.TestCase):
    def test_add(self):
        self.assertEqual([3, 10], async(2).do(add, 1, 2).do(add, 4, 6)())
        self.assertNotEqual([4, 4], async(2).do(add, 4, 2).do(add, 4, 1)())
        with self.assertRaises(Exception):
            async(2).do(add, 1, 3).do(exception)()
    
    def test_do_async(self):
        self.assertEqual([3, 2], async(2).do(print_now, 'first', 3).do(print_now, 'second', 2)())
        with self.assertRaises(Exception):
            async(4).do(print_now,'exception', 3).do(exception)()
        print('end time {}'.format(time.ctime()))
        signal.signal(signal.SIGHUP, handler)

if __name__ == '__main__':
    unittest.main()