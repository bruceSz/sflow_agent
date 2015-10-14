#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_PC_gear.py
Author: baidu(baidu@baidu.com)
Date: 2015/10/14 16:24:15
"""

import sys
import os
import unittest
import random
import logging
import time


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sflow_agent import utils
from sflow_agent import log

class PCgearTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')

    def setUp(self):
        log.init_log("test_PC_gear.log")

    def _serial_execution(self):

        def func1():
            return random.randint(1,10)
        def func2(i):
            print i


        worker1 = utils.Worker(head=True)
        worker1.init_worker(func1)
        worker2 = utils.Worker()
        worker2.init_worker(func2)

        gear1 = utils.PCgear()
        gear1.add_producer(worker1)
        gear1.add_consumer(worker2)
        worker1.start()
        print 'ha'
        worker2.start()
        worker1._Thread__stop()
        worker2._Thread__stop()
        #worker1.join()
        #worker2.kill()

    def _pipeline_serialize_execution(self):
        print 'serialize execution test begin'
        
        def func1():
            yield random.randint(1,10)
        def func2(i):
            print i

        pipeline = utils.Pipeline(1)
        pipeline.add_worker(func1)
        pipeline.add_worker(func2, tail=True)
        pipeline.start()
        time.sleep(1)
        pipeline.stop()
        print 'serialize execution test end'

    def test_pipeline_fast_slow_execution(self):
        print 'fast_slow execution test begin'
        def func1():
            i = 0
            while i < 5:
                yield random.randint(1,10)
                i += 1
                time.sleep(1)
        
        def func2(i):
            try:
                print "dfdfd" , i , "fjkdjfdkjfdk   "
            except Exception as err:
                print err

        pipeline = utils.Pipeline(0)
        pipeline.add_worker(func1)
        pipeline.add_worker(func2, tail=True)
        pipeline.start()
        #time.sleep(3)
        pipeline.stop()
        print 'fast_slow execution test end'


if __name__ == "__main__":
    unittest.main()


