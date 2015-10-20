#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_virt.py
Author: baidu(baidu@baidu.com)
Date: 2015/10/20 20:47:02
"""

import sys
import os
import commands

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sflow_agent import virt

UUID = 'sflow_agent_test'


class VirtTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "etc/test.conf")
    def setUp(self):
        pass

    def test_ifindex_to_uuid(self):
        status, output = commands.getstatusoutput("ip link|grep qvo|awk -F':' '{print $1}'")
        ifindex_list = output.strip("\n").split("\n")
        for ifindex in ifindex_list:
            print virt.ifindex_to_uuid(ifindex)
                                  

if __name__ == "__main__":
    log.init("test_virt")
    unittest.main()