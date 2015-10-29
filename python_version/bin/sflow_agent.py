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
import time
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
from sflow_agent.db import api

_CONF_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "etc/sflow_agent.conf")

def main():
    log.init_log("sflow_agent")
    config.init(_CONF_FILE)
    utils.security_start(config.CONF)
    sflow_client = client.SflowClient(config.CONF.yunhai)
    logging.info("Sflow agent start.")
    
    sflow_entry_cache = {}
    # uuid: (sflow_entry,timestamp)

    def func1():
        listen_addr = ("0.0.0.0", 6343)
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(listen_addr)
        while True:
            data, addr = sock.recvfrom(65535)
            sflow_datagram = {}
            sflow_datagram["addr"] = addr
            sflow_datagram["data"] = data
            yield sflow_datagram

    def func3(item):
        #logging.info("Emit sflow entry begin")
        for rec in item:
            for counter_record in rec:
                counter_data = counter_record.data
                sflow_entry = utils.IfCounters_to_sflow_entry(counter_data)
                if sflow_entry is not None:
                    logging.info("Sflow entry added: %s" % sflow_entry)
                    sflow_client.add_sflow_entry(sflow_entry)
                    yield sflow_entry
        #logging.info("Emit sflow entry end.")

    def func4(sflow_entry):
        uuid = sflow_entry["uuid"]
        if uuid not in sflow_entry_cache:
            sflow_entry_cache[uuid] = (sflow_entry, int(time.time()))
        else:
            curr_time = int(time.time())
            last_sflow_entry = sflow_entry_cache[uuid][0]
            last_time = sflow_entry_cache[uuid][1]
            in_pps_diff = int(sflow_entry["in_pps"] - last_sflow_entry["in_pps"])
            velocity = int(in_pps_diff / (curr_time - last_time))
            if velocity > int(config.CONF.alarm.pps_threshold):
                record = models.AbnormalRecord()
                record.uuid = uuid
                record.start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(curr_time))
                record.stats = json.dumps(sflow_entry)
                api.abnormal_record_insert(record)



    pipeline = utils.Pipeline(1)
    pipeline.add_worker(func1)
    pipeline.add_worker(parser.parse)
    pipeline.add_worker(func3, tail=True)

    def kill(signum, frame):
        logging.info("meet signal: %s"%str(signum))
        logging.info("sigterm/sigint received. remove status file and exist")
        prog_status_path = config.CONF.default.prog_status_path
        if os.path.exists(prog_status_path):
            utils.remove_status_file(prog_status_path)
        pipeline.stop()

    signal.signal(signal.SIGINT, kill)
    signal.signal(signal.SIGTERM, kill)
    pipeline.start()
    pipeline.join()
    logging.info("Sflow agent end.")


if __name__ == "__main__":
    main()

