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

import os
import sys
import logging
import signal
from socket import socket, AF_INET, SOCK_DGRAM

sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sflow_agent import log
from sflow_agent import client
from sflow_agent import config
from sflow_agent import utils
from sflow_agent import parser

_CONF_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "etc/sflow_agent.conf")

    


def main():
    log.init_log("sflow_agent")
    config.init(_CONF_FILE)
    sflow_client = client.SflowClient(config.CONF.yunhai)
    logging.info("Sflow agent start.")
        
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
            if i >= 10:
                break
    def func3(item):
        for rec in item:
            for counter_record in rec:
                counter_data = counter_record.data
                sflow_entry = utils.IfCounters_to_sflow_entry(counter_data)
                if sflow_entry is not None:
                    logging.info("Sflow entry added: %s" % sflow_entry)
                    sflow_client.add_sflow_entry(sflow_entry)
            #stdout.flush()
    pipeline = utils.Pipeline(1)
    pipeline.add_worker(func1)
    pipeline.add_worker(parser.parse)
    pipeline.add_worker(func3, tail=True)
    def kill(signum, frame):
        pipeline.stop()
    signal.signal(signal.SIGINT, kill)
    pipeline.start()
    pipeline.join()
    logging.info("Sflow agent end.")


if __name__ == "__main__":
    main()

