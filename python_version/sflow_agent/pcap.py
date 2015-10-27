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
    Pcap file format (24B): 
        magic u_int32
        version_major u_short
        version_minor u_short
        thiszone int32
        sigfigs u_int32
        snaplen u_int32
        linktype u_int32

    Packet header (16B):


"""

import struct
import dpkt
import logging
import os


class Pcap(object):
    def __init__(self, pcap_file):
        self.f = open(pcap_file)
        self.file_name = pcap_file
        self.pcap = dpkt.pcap.Reader(self.f)

    def parse(self):
        for ts, buf in self.pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                yield eth

            except Exception as err:
                logging.warning("Error when parsing pcap file. ts: %s, buf: %s. %s"\
                    % (ts, buf, err))

    def delete_pcap_file(self):
        os.remove(self.file_name)


def raw_pcap_parser():
    file_name = "./x.cap"
    with open(file_name, "r") as f:
        text = f.read()
        head = struct.unpack("IHHiIII", text[:24])



if __name__ == "__main__":
    main()
