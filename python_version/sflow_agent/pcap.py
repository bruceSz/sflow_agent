#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: pcap.py
Author: baidu(baidu@baidu.com)
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


def raw_pcap_parser():
    file_name = "./x.cap"
    with open(file_name, "r") as f:
        text = f.read()
        head = struct.unpack("IHHiIII", text[:24])



if __name__ == "__main__":
    main()
