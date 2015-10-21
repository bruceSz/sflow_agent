#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: client.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/19 23:24:18
"""


#from eventlet.green import urllib2
import urllib2
import json
import logging
import time


_USER_AGENT = "python-sflow-agent"



class HttpClient(object):

    def __init__(self):
        pass

    # as the urllib2 will deal with post and get automatically,
    # for put and delete ,we do the hack as folow.
    def _do_request(self, url, headers_dict=None, data=None, method=None):
        auth_req = urllib2.Request(url)
        
        if method is not None:
            auth_req.get_method = method

        if headers_dict is not None:
            for k,v in headers_dict.items():
                auth_req.add_header(k,v)
        
        if data is not None:
            
            json_data = json.dumps(data)
            auth_req.add_data(json_data)
        
        try:
            #print auth_req.data
            auth_res = urllib2.urlopen(auth_req)
            
            
        except urllib2.HTTPError as err:
            logging.error(err)
            return None
        except urllib2.URLError as url_err:
            logging.error(url_err)
            return None
        except Exception as err:
            logging.error("Unexpected error: %s" % err)
            return None
            
        res_data = auth_res.read()

        if len(res_data) == 0:
            res_data = None
        else:
            res_data  = json.loads(res_data)

        return res_data

    def delete(self,url,headers=None):
        delete_method = lambda : "DELETE"
        return self._do_request(url,headers,method=delete_method)

    def get(self,url,headers=None):
        return self._do_request(url,headers)

    def post(self,url,data,headers=None):
        assert(data is not None)
        return self._do_request(url,headers,data)


class SflowClient(HttpClient):

    _KEY_TRANSTER = {
        "in_discard": "inDiscard",
        "in_error": "inError",
        "in_bps": "inBps",
        "in_pps": "inPps",
        "out_discard": "outDiscard",
        "out_error": "outError",
        "out_bps": "outBps",
        "out_pps": "outPps"
    }
  
    def __init__(self,conf):
      
        self.base_post_url = conf.post_url
        self.username = conf.username
        self.password = conf.password

        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, self.base_post_url, self.username, self.password)
        handler = urllib2.HTTPBasicAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        super(SflowClient,self).__init__()

    
    def add_sflow_entry(self, data):
        """
            post_data format:
               
                post_data = {
                   "uuid":"xxx",
                   "host":"yyy",
                   "inDiscard":xx,
                   "inError":xx,
                   "inBps":xx,
                   "inPps":xx,   
                   "outDiscard":x,
                   "outError":x,
                   "outBps":x,
                   "outPps":x
               }

        """
        full_url = self.base_post_url 
        key_transter = self.__class__._KEY_TRANSTER

        headers = {}
        headers['Content-Type'] = 'application/json;charset=utf8'
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = _USER_AGENT

        post_data = {} 
        for k, v in data.items():
            if k in key_transter:
                new_k = key_transter[k]
                post_data[new_k] = v
            else:
                post_data[k] = v

        res = self.post(full_url, post_data, headers)
        return res


