#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: pcap.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/22 21:29:50
"""

"""
    Flow extractor: 
        1 dump flow with limited packet num specified in config(using tcpdump).
        2 parse packets.
        3 extract target info from packet,build flow_summary info ,persist it into analyzer db.
"""

import time
import commands
import logging
import pcap
import socket

class FlowExtractor(object):
    def __init__(self, conf):
        self.pcap_suffix_name = conf.suffix_name 
        self.pcap_packet_num = conf.packet_num

    def _dump_flow(self, dev_name):
        # TODO: need add try catch here.
        self.pcap_eth_dev_name = dev_name
        self.pcap_file_name = dev_name + "_" + str(int(time.time())) + "." + self.pcap_suffix_name
        status, output = commands.getstatusoutput("sudo tcpdump -i %s -c %s -w %s"\
                                                  % (self.pcap_eth_dev_name, \
                                                    self.pcap_packet_num, \
                                                    self.pcap_file_name))
        self.pcap = pcap.Pcap(self.pcap_file_name)

    def _extract_summary_info(self, ip_data):
        """
            packet_summary: (src, dst, proto, flags)
            flags: none for udp
            proto: tcp; udp
        """
        src = socket.inet_ntoa(ip_data.src)
        dst = socket.inet_ntoa(ip_data.dst)

        if ip_data.data.__class__.__name__ == "TCP":
            tcp = ip_data.data
            flags = tcp.flags
            packet_summary = (src, dst, "TCP", flags)

        elif ip_data.data.__class__.__name__ == "UDP":
            packet_summary = (src, dst, "UDP", None)
        else:
            # ignore other L4 protocol
            logging.info("Ignore unsupported L4 packet type: %s " % ip_data.data.__class__.__name__)
            packet_summary = None

        return packet_summary

    def extract(self, dev_name):
        """ 
            Extract proto type info, flag info  for each packet.
        """
        self._dump_flow(dev_name)
        for ether_pac in self.pcap.parse():
            if ether_pac.data.__class__.__name__ == "IP":
                ip = ether_pac.data
                packet_summary = self._extract_summary_info(ip)
                if packet_summary is not None:
                    yield packet_summary
            else:
                # ignore other L3 protocol
                logging.info("Ignore unsupported L3 packet type: %s " % ether_pac.data.__class__.__name__)
                pass
        







