#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: virt.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/19 23:40:21
"""

"""
 Virtual Machine related opration.
"""

import commands
import logging

IFINDEX_TO_UUID = {}
TAP_TO_VM = {}
IFINDEX_TO_TAP = {}


def _assert_network_device_exists(device_name):
    status, output = commands.getstatusoutput("ip link|grep %s " % device_name)
    if output is None or len(output.strip("\n").strip()) == 0:
        logging.warning("Network device %s does not exist." % device_name)
        return False
    return True


def _ifindex_to_tap(ifindex):
    """
        Args:ifindex of qvo device.
        Returns: corresponding tap device name .None is returns when qvo/tap device do not exist.
    """
    if ifindex in IFINDEX_TO_TAP:
        return IFINDEX_TO_TAP[ifindex]
    status, output = commands.getstatusoutput("ip link|grep %d|awk -F: '{print $2}'" 
                                        % int(ifindex))
    qvo_name = output.strip("\n").strip()
    tap_name = "tap" + qvo_name[3:]
    if not _assert_network_device_exists(tap_name):
        IFINDEX_TO_TAP[ifindex] = None
        return None
    IFINDEX_TO_TAP[ifindex] = tap_name
    return tap_name


def _tap_to_vm(tap_name):
    if tap_name in TAP_TO_VM:
        return TAP_TO_VM[tap_name]

    status, output = commands.getstatusoutput("virsh list |awk '/running/ {print $2}' ")
    vm_list = output.strip().split("\n")
    vm_list = filter(lambda x:len(x)>0,vm_list)
    for vm in vm_list:
        # assume there is only on tap device inserted in the vm.
        status,output = commands.getstatusoutput("virsh domiflist %s|awk '/tap/ {print $1}'"
                                                    % vm)
        tmp_tap_name = output.strip()
        TAP_TO_VM[tmp_tap_name] = vm

    if tap_name not in TAP_TO_VM:
        logging.warning("Invalid tap device name %s provided, there is no vm with network \
            device named as it is. ")
        TAP_TO_VM[tap_name] = None
        return None
    return TAP_TO_VM[tap_name]


def ifindex_to_uuid(ifindex):
    """
    Args: ifindex of qvo
    Returns: returns vm uuid with qvo device corresponding to the ifindex
            None is returned, if exception happens.
    """
    if ifindex in IFINDEX_TO_UUID:
        return IFINDEX_TO_UUID[ifindex]

    tap_name = _ifindex_to_tap(ifindex)
    if tap_name is None:
        return None

    vm_name = _tap_to_vm(tap_name)
    if vm_name is None:
        return None

    status, output = commands.getstatusoutput("virsh domuuid %s" % vm_name)
    uuid = None if output is  None else output.strip("\n").strip()
    if uuid is None or len(uuid) == 0:
        return None
    IFINDEX_TO_UUID[ifindex] = uuid
    return IFINDEX_TO_UUID[ifindex]

