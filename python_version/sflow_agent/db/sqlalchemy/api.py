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
Date: 2015/09/24 18:15:59
"""


import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc

from sflow_agent.db.sqlalchemy import models




class SqlalchemyWrapper(object):

    def __init__(self, conf, lazy=True):
        #TODO: try catch needs to be added.
        if lazy is True:
            # only for test case.
            self.conf = None
        else:
            self._init_with_conf(conf)

    def _init_with_conf(self, conf):
        self.conf = conf
        self._engine = create_engine('mysql://%s:%s@%s:%s/%s'\
        %(conf.username, conf.password, conf.host, conf.port, conf.db_name))
        logging.info("Create new database engine. ")

        DBSession = sessionmaker(bind=self._engine, autocommit=True)
        self._session = DBSession()
        logging.info("Create new database session. ")

    def is_set(self):
        """ check whether SqlalchemyWrapper has been initialized."""
        if not self.conf is None:
            return True
        else:
            return False

    def init(self, conf):
        """Init the SqlalchemyWrapper with conf """
        self._init_with_conf(conf)

    def abnormal_record_get_all(self):
        """Get all abnormal record """
        ret = self._session.query(models.AbnormalRecord).order_by(models.AbnormalRecord.start.desc())
        return ret.all()

    def abnormal_record_group_by_uuid(self):
        """ 
            Get abnormal record summary group by uuid
            default order by desc
        """
        ret = self._session.query(models.AbnormalRecord.uuid, func.count('*').label('abnormal_times'))\
                                .group_by(models.AbnormalRecord.uuid)\
                                .order_by(desc('abnormal_times'))
        return ret.all()

    def abnormal_record_by_uuid(self, uuid):
        """ 
            Get abnormal record details according to uuid
            default order by desc
        """
        ret = self._session.query(models.AbnormalRecord)\
                                .filter_by(uuid=uuid)\
                                .order_by(models.AbnormalRecord.start.desc())
        return ret.all()


    def abnormal_record_insert(self, record):
        """Insert into abnormal record"""
        self._session.add(record)

    def abnormal_record_delete(self, uuid):
        """Delete abnormal record according to uuid"""
        assert(type(uuid) == type(''))
        assert(len(uuid) == 36)
        all_record = self._session.query(models.AbnormalRecord).filter_by(uuid=uuid)
        for record in all_record.all():
            self._session.delete(record)









