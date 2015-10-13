#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: config.py
Author: baidu(baidu@baidu.com)
Date: 2015/10/13 21:14:18
"""

import os
import ConfigParser

import utils

CONF = None

class Conf(dict):
    __getattr__ = dict.__getitem__

    def __init__(self):
        super(Conf, self).__init__()

    def init(self, conf_file):
        """Init the Conf class with conf_file """
        conf = ConfigParser.ConfigParser()
        assert(os.path.isfile(conf_file))
        conf.read(conf_file)
        
        sections = conf.sections()
        for sec in sections:
            self[sec] = Conf()
            options = conf.options(sec)
            for opt in options:
                if opt.find("file") != -1:
                    file_path = utils.formalize(conf_file, conf.get(sec, opt))
                    self[sec][opt] = file_path
                else:
                    val = conf.get(sec,opt)
                    if "," in val:
                        self[sec][opt] = map(lambda x:x.strip(),val.split(","))
                    else:
                        self[sec][opt] = val


def init(filename):
    """ Init this module """
    global CONF
    if CONF is None:
        CONF = Conf()
        CONF.init(filename)

def make_config(filename):
    """
        Create one brand new Conf .
    """
    conf = Conf()
    conf.init(filename)
    return conf