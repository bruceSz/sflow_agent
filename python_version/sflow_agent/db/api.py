#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: api.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/09/24 17:43:17
"""

from sflow_agent.db.sqlalchemy import sqlalchemy_api
from sflow_agent import config

_IMPL = sqlalchemy_api


def _init():
    """Init the db api with conf """
    _IMPL.init(config.CONF.db)


def check_init(func):
    """ decorate to make funcs is initialized """
    def wrapper(*args):
        if not _IMPL.is_set():
            _init()
        return func(*args)
    return wrapper


@check_init
def abnormal_record_get_all():
    """Get all abnormal records"""
    return _IMPL.abnormal_record_get_all()


@check_init
def abnormal_record_group_by_uuid():
    """ Get all abnormal record group by uuid """
    return _IMPL.abnormal_record_group_by_uuid()


@check_init
def abnormal_record_by_uuid(uuid):
    """ Get all abnormal record filtered by uuid"""
    return _IMPL.abnormal_record_by_uuid(uuid)


@check_init
def abnormal_record_insert(record):
    """ Insert abnormal record """
    _IMPL.abnormal_record_insert(record)


@check_init
def abnormal_record_delete(uuid):
    """Delete abnormal record match uuid"""
    _IMPL.abnormal_record_delete(uuid)

