#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_client.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/20 20:43:03
"""

import sys
import os
import unittest
import commands
import time


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sflow_agent import log
from sflow_agent import net_flow
from sflow_agent import config



class SflowTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')
    def setUp(self):
        conf = config.Conf()
        self.conf = conf  q
        conf.init(self.__class__._CONF_FILE)
        self.flow_extractor = net_flow.FlowExtractor(conf.default)

    def test_pcap_parse(self):
        for pac_summary in self.flow_extractor.extract(self.conf.default.eth_dev):
            print pac_summary 
                          

if __name__ == "__main__":
    log.init_log("test_net_flow")
    unittest.main()