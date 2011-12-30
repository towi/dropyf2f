#!/usr/bin/env python
"""test for existance of 'redis' and basic functionality"""

# std python
import unittest            # std
import time

# make local python available
import sys
sys.path = [ "../../main/python"] + sys.path

# dropy local
from dropy.sredis import SRedis


class TestRedis(unittest.TestCase):
    TESTKEY = 'unittest:testkey'
    def setUp(self):
        pass
    def tearDown(self):
        r = SRedis()
        r.delete(self.TESTKEY)

    def test01Connect(self):
        """check basic connection to redis"""
        r = SRedis()
        self.assertEquals(r.get(self.TESTKEY), None)

    def test10SetString(self):
        """check set a string value"""
        r = SRedis()
        r.set(self.TESTKEY, 'somevalue')

    def test20GetString(self):
        """check set and get a string value"""
        r = SRedis()
        # set, get
        r.set(self.TESTKEY, 'somevalue')
        self.assertEquals(r.get(self.TESTKEY), 'somevalue')
        # change, get
        newvalue = "value:%s" % time.time()
        r.set(self.TESTKEY, newvalue)
        self.assertEquals(r.get(self.TESTKEY),newvalue)

    def test30List(self):
        """check list workings"""
        r = SRedis()
        K = self.TESTKEY
        # push
        r.lpush(K, "v10")
        r.lpush(K, "v20")
        r.lpush(K, "v30")
        r.lpush(K, "v40")
        self.assertEquals(r.llen(K), 4)
        self.assertEquals(r.lpop(K), "v40")
        self.assertEquals(r.llen(K), 3)
        # trim
        r.ltrim(K, 0, 1) # would be [0:2] in python.
        self.assertEquals(r.llen(K), 2) # 'v10' was dropped
        # pop
        self.assertEquals(r.lpop(K), "v30")
        self.assertEquals(r.lpop(K), "v20")
        self.assertEquals(r.lpop(K), None)


if __name__ == "__main__":
    unittest.main()
