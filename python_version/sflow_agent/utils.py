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

import logging

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

    def init_worker(self, func):
        self.func = func


    def run(self):
        if not self.head:
            while True:
                if not self.consume is None:
                    item = self.consume()
                    ret = self.func(item)
                else:
                    ret = self.func()
    
                if not self.produce is None:
                    self.produce(ret)
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

    def add_worker(self, func, tail=False):
        """
        add worker to pipeline
        """
        gear = PCgear(self.queue_size)
        if self.head is None:
            worker = Worker(head=True)
            worker.init_worker(func)
            self.head = worker
            gear.add_producer(worker)
            self.gears.append(gear)
        else:
            worker = Worker()
            worker.init_worker(func)
            pre_gear = self.gears[-1]
            pre_gear.add_consumer(worker)
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














