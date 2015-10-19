#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: utils.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/14 12:06:35
"""

import Queue
import threading
import thread
import time
import logging

from sys import stdout
from socket import ntohl
from math import floor, ceil, log
#

ether_type_description = { 0x0800 : 'IP',
                           0x0806 : 'ARP',
                           0x8100 : '802.1Q(VLAN)',
                           0x86DD : 'IPv6' }

ip_proto_name = { 0 : 'ip',
                  1 : 'icmp',
                  2 : 'igmp',
                  3 : 'ggp',
                  4 : 'ipencap',
                  5 : 'st',
                  6 : 'tcp',
                  8 : 'egp',
                  9 : 'igp',
                  12 : 'pup',
                  17 : 'udp',
                  20 : 'hmp',
                  22 : 'xns-idp',
                  27 : 'rdp',
                  29 : 'iso-tp4',
                  36 : 'xtp',
                  37 : 'ddp',
                  38 : 'idpr-cmtp',
                  41 : 'ipv6',
                  43 : 'ipv6-route',
                  44 : 'ipv6-frag',
                  45 : 'idrp',
                  46 : 'rsvp',
                  47 : 'gre',
                  50 : 'esp',
                  51 : 'ah',
                  57 : 'skip',
                  58 : 'ipv6-icmp',
                  59 : 'ipv6-nonxt',
                  60 : 'ipv6-opts',
                  73 : 'rspf',
                  81 : 'vmtp',
                  88 : 'eigrp',
                  89 : 'ospf',
                  93 : 'ax.25',
                  94 : 'ipip',
                  97 : 'etherip',
                  98 : 'encap',
                  103 : 'pim',
                  108 : 'ipcomp',
                  112 : 'vrrp',
                  115 : 'l2tp',
                  124 : 'isis',
                  132 : 'sctp',
                  133 : 'fc',
                  136 : 'udplite' }
#


def ether_type_to_string(ether_type):
    if ether_type in ether_type_description:
        return ether_type_description[ether_type]
    else:
        return 'unknown(%04X)' % ether_type


def mac_to_string(mac):
    """Returns an Ethernet MAC address in the form
    XX:XX:XX:XX:XX:XX."""

    return ('%02X:%02X:%02X:%02X:%02X:%02X' %
            (mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]))


def ip_to_string(ip):
    """Returns ip as a string in dotted quad notation."""
    #    ip = ntohl(ip)              
    # network byte order is big-endian
    # 0x12345678
    # buf[3] = 0x78
    # buf[2] = 0x56
    # buf[1] = 0x34
    # buf[0] = 0x12
    #
    return '%d.%d.%d.%d' % (ip & 0xff,
                            (ip >> 8) & 0xff,
                            (ip >> 16) & 0xff,
                            (ip >> 24) & 0xff)


def ip_proto_to_string(proto):
    if proto in ip_proto_name:
        return ip_proto_name[proto]
    else:
        return 'unknown(%d)' % proto


def speed_to_string(speed):
    speed_name = { 10000000 : '10Mb',
                   100000000 : '100Mb',
                   1000000000 : '1Gb',
                   10000000000 : '10Gb' }

    if speed in speed_name:
        return speed_name[speed]
    else:
        return str(speed)


def hexdump_escape(c):
    """Returns c if its ASCII code is in [32,126]."""
    if 32 <= ord(c) <= 126:
        return c
    else:
        return '.'






#helper func of pipeline.
class PCgear(object):
    """
        producer and consumer unit, form all producer and consumer 
        pipeline.
    """
    def __init__(self, size=10):
        self.queue = Queue.Queue(size)
        self.producers = []
        self.consumers = []
        
    def add_producer(self, producer):
        """
            add produce worker to this gear,
            initialize it's produce method.
            
            TODO: producer add name and gear 
            name for better debug experience.
        """
        self.producers.append(producer)
        producer.produce = self._produce
        producer.gear = self

    def _produce(self, item):
        """
        Try to put item into self.gear.queue.
        do nothing when the queue is full, which means drop item.
        Self here is the producer.
        """
        try:
            self.queue.put_nowait(item)
        except Queue.Full as full:
            logging.warning(full)
            pass
        except Exception as e:
            logging.fatal(e)
            raise e


    def add_consumer(self, consumer):
        """
            add consume worker to this gear,
            initialize it's condume method.

            TODO: consumer add name and gear 
            name for better debug experience.
        """
        self.consumers.append(consumer)
        consumer.consume = self._consume
        consumer.gear = self

    def _consume(self):
        """ 
        this will block if self.gear.queue is empty. 
        Self here is the consumer
        """
        return self.queue.get()



class Worker(threading.Thread):
    def __init__(self, head=False):
        threading.Thread.__init__(self)
        self.produce = None
        self.consume = None
        self.head = head
        self.working = False

    def init_worker(self, func):
        self.func = func


    def run(self):
        """

        """
        if not self.head:
            while True:
                # if a worker is head it should not has
                # consume method, vise versa.
                # hence the if here sees to be redundant
                # 

                # if block at consume func, working is False.
                
                # TODO: self.working is a critical area. make it
                # atomic. 
                item = self.consume()
                logging.info(' %d: start working' % thread.get_ident())
                self.working = True
                ret = self.func(item)
                if not self.produce is None:
                    self.produce(ret)
                self.working = False
                logging.info(' %d: end working' % thread.get_ident())

        else:
            if not self.produce is None:
                for item in self.func():
                    self.produce(item)


class Pipeline(object):
    def __init__(self, queue_size=10):
        self.workers = []
        self.gears = []
        self.head = None
        self.queue_size = queue_size

    def add_worker(self, func, tail=False, workers=1):
        """
        add worker to pipeline
        """
        gear = PCgear(self.queue_size)
        num = workers
        if self.head is None:
            assert(num == 1)
            worker = Worker(head=True)
            worker.init_worker(func)
            self.head = worker
            gear.add_producer(worker)
            self.gears.append(gear)
            self.workers.append(worker)

        else:
            pre_gear = self.gears[-1]

            while num > 0:
              worker = Worker()
              worker.init_worker(func)
              pre_gear.add_consumer(worker)
              num -= 1
              if not tail:
                  gear.add_producer(worker)
                  self.gears.append(gear)
              self.workers.append(worker)


    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        """
        Stop all the worker in pipeline.
        """
        for worker in self.workers:
            worker._Thread__stop()

    def join(self):
        """
        wait until head  worker is done and no middle worker is in 
        running state.
        """
        while True:
            time.sleep(1)
            if not self.head.isAlive():
                i = 0
                for i in range(1,len(self.workers)):
                    if self.workers[i].isAlive():

                        if self.gears[i-1].queue.empty() and \
                            not self.workers[i].working:
                            self.workers[i]._Thread__stop()
                        break

                # if tail worker is not running anymore.
                # return .
                if not self.workers[len(self.workers)-1].isAlive():
                    break
            else:
                # head is still running
                pass
