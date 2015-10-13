#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: sflow_agent.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/13 21:03:42
"""

if __name__ == "__main__":
    conf = init()
    security_start(conf)
    grace_exit(conf)
    index_intance_name_map, lock = init_dev_index_pair()
    sff = sfilter.SFlowFilter(conf.default,index_intance_name_map, lock)
    sff.add_notifier(notifier.YunhaiNotifier(conf.yunhai))
    consume_loop(sff, conf)


