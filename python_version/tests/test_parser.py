#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_PC_gear.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/14 16:24:15
"""

import sys
import os
import unittest
import random
import logging
import time
import signal
from socket import socket, AF_INET, SOCK_DGRAM


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sflow_agent import utils
from sflow_agent import log
from sflow_agent import parser

class PCgearTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')

    def setUp(self):
        pass 

    def test_parser(self):
        logging.info("test parser begin.") 
        
        def func1():
            listen_addr = ("0.0.0.0", 6343)
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.bind(listen_addr)
            i = 0
            while True:
                data, addr = sock.recvfrom(65535)
                sflow_datagram = {}
                sflow_datagram["addr"] = addr
                sflow_datagram["data"] = data
                yield sflow_datagram
                i += 1
                if i >= 3:
                    break

        def func3(item):
            for rec in item:
                print(rec)
                #stdout.flush()
        pipeline = utils.Pipeline(1)
        pipeline.add_worker(func1)
        pipeline.add_worker(parser.parse)
        pipeline.add_worker(func3, tail=True)

        def kill(signum, frame):
            pipeline.stop()

        signal.signal(signal.SIGINT, kill)
        pipeline.start()
        print "gears: %d.. " % len(pipeline.gears)
        print "workers: %d.. " % len(pipeline.workers)
        #time.sleep(3)
        pipeline.join()
        logging.info("test parser end.")


if __name__ == "__main__":
    log.init_log("test_parser")
    unittest.main()


