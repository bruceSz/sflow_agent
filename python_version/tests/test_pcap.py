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
from sflow_agent import pcap
from sflow_agent import config



class SflowTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')
    def setUp(self):
        conf = config.Conf()
        conf.init(self.__class__._CONF_FILE)
        self.conf = conf
        self.pcap_eth_dev_name = self.conf.default.eth_dev
        self.pcap_packet_num = self.conf.default.packet_num 

        self.pcap_file_name = str(int(time.time())) + "_" + self.pcap_eth_dev_name + ".pcap"
        status, output = commands.getstatusoutput("sudo tcpdump -i %s -c %s -w %s"\
                                                  % (self.pcap_eth_dev_name, \
                                                    self.pcap_packet_num, \
                                                    self.pcap_file_name))
        self.pcap_tool = pcap.Pcap(self.pcap_file_name)

    def test_pcap_parse(self):
        ethernet_packets = self.pcap_tool.parse()
        for pac in ethernet_packets:
            print pac
                          

if __name__ == "__main__":
    log.init_log("test_client")
    unittest.main()