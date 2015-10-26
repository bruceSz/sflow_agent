#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: models.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/09/24 17:41:31
"""


from sqlalchemy import Column, String, Integer, TIMESTAMP, Text
#from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class AbnormalRecord(Base):
        # 表的名字:
    __tablename__ = 'abnormal_record'

        # 表的结构:
    aid = Column(Integer, primary_key=True )
    uuid = Column(String(36), nullable=False)
    start = Column(TIMESTAMP, nullable=True)
    end = Column(TIMESTAMP, nullable=True)
    stats = Column(Text, nullable=True)

    def to_json(self):
        return {
            'uuid' : self.uuid,
            'start' : self.start.isoformat() if self.start is not None else 'null',
            'end' : self.end.isoformat() if self.end is not None else 'null',
            'stats' : self.stats
        }

class VMNetworkFlowSummary(Base):

    __tablename__ = 'network_flow_summary'
    # sqlalchemy will set id as
    nfid = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=True)
    ctime = Column(TIMESTAMP, nullable=True)
    summary = Column(Text, nullable=True)

    
