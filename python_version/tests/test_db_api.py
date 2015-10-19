#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_db_api.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/09/24 22:03:39
"""

import sys
import os
import unittest
import logging
import string
import random
import time

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sflow_agent.db import api
from sflow_agent.db.sqlalchemy import models
from sflow_agent import config
from sflow_agent import log

class DBApiTestCase(unittest.TestCase):
    _CONF_FILE = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'etc/test.conf')


    def setUp(self):
        #self.conf = config.make_config(self.__class__._CONF_FILE)
        #api.init(self.conf.db)
        config.init(self.__class__._CONF_FILE)

    def test_get_set(self):
        #TODO
        ar = models.AbnormalRecord()

        letter_digits = string.ascii_letters + string.digits
        ar.uuid = ''.join([letter_digits[random.randint(0,35)] for i in range(0,36)])
        ar.start = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        ar.end = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        ar.stats = 'test,this is just a test'

        api.abnormal_record_insert(ar)

        ret = api.abnormal_record_get_all()
        uuid_set = set(map(lambda x:x.uuid, ret))
        assert(ar.uuid in uuid_set)
        #import pdb
        #pdb.set_trace()
        api.abnormal_record_delete(ar.uuid)

        ret = api.abnormal_record_get_all()
        uuid_set = set(map(lambda x:x.uuid, ret))
        assert(ar.uuid not in uuid_set)


if __name__ == "__main__":
    log.init_log("test_db_api")
    unittest.main()
