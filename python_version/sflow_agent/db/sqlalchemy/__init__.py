#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: __init__.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/09/24 18:15:51
"""

from sflow_agent import config
from sflow_agent.db.sqlalchemy import api
import logging

_CONF = config.CONF

_db_conf = _CONF.db if _CONF is not None else None

sqlalchemy_api = api.SqlalchemyWrapper(_db_conf, lazy=True)
