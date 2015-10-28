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
import random
import json


sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sflow_agent import log
from sflow_agent import net_flow
from sflow_agent import config
from sflow_agent.db.sqlalchemy import models
from sflow_agent.db import api



class NetFlowTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')
    def setUp(self):
        config.init(self.__class__._CONF_FILE)
        self.flow_extractor = net_flow.FlowExtractor(config.CONF.default)

    def test_flow_summary_persist(self):
        for pac_summary in self.flow_extractor.extract(config.CONF.default.eth_dev,pcap_keep=False):
            nfs = models.VMNetworkFlowSummary()
            nfs.uuid = ''.join(chr(random.randint(97,122)) for i in range(0,36))
            nfs.ctime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            nfs.summary = json.dumps(pac_summary)
            api.network_flow_summary_insert(nfs)
            print api.network_flow_summary_get_by_uuid_ctime(nfs.uuid, nfs.ctime)





                          

if __name__ == "__main__":
    log.init_log("test_net_flow")
    unittest.main()