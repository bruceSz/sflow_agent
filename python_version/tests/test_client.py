#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_client.py
Author: baidu(baidu@baidu.com)
Date: 2015/10/20 20:43:03
"""

import sys
import os
import unittest
import logging
import json
import random
import time
import urllib2

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sflow_agent import config

UUID = 'sflow_agent_test'


class SflowTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "etc/test.conf")
    def setUp(self):
        conf = config.Conf()
        conf.init(self.__class__._CONF_FILE)
        self.conf = conf
        self.sflow_client = client.SflowClient(conf.yunhai)
        self.uuid = 'zs-test'

    def test_post_sflow_entry(self):
        data = {
           "uuid": "test."+str(self.uuid),
           "hostname": "test.baidu.com",
           "in_discard": -1,
           "in_error":-1,
           "in_bps":-1,
           "in_pps":-1,
           "out_discard":-1,
           "out_error":-1,
           "out_bps":-1,
           "out_pps":-1
        }
        self.sflow_client.add_sflow_entry(data)
                          

if __name__ == "__main__":
    log.init("test_client")
    unittest.main()