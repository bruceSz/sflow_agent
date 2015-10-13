#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: sflow_agent.py
Author: zhangsong06(zhangsong06@baidu.com)
Date: 2015/10/13 21:03:42
"""

import commands
import os
import sys
import signal

import multiprocessing
import time
from eventlet.green import subprocess

from flow_stat import config
from flow_stat import sfilter
from flow_stat import notifier
from flow_stat import log


class ProcessManager(object):
    def __init__(self):
        self.pid = os.getpid()
        self.procs = []

    def addProcess(self, proc):
        if os.getpid() != self.pid:
            return
        self.procs.append(proc)

    def killAll(self):
        if os.getpid() != self.pid:
            return
        log.write("info","will kill %s"%str(self.procs))
        for proc in self.procs:
            # if the proc is Popen
            proc.terminate()

# below line must be run in the very earliest stage of the prog,
# at least before subprocess are started.
_PM = ProcessManager()

_CONF_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "etc/sflow.conf")

def clean():
    status,output = commands.getstatusoutput("ps -ef|grep sflowtool|grep -v grep |awk '{print $2}' ")
    sflowtool_pid  = output.strip()
    if not sflowtool_pid  == "":
        status,output = commands.getstatusoutput("kill -9 %s"%sflowtool_pid)
 



def consume_loop(flow_filter, conf):
    global _PM
    res = subprocess.Popen("./scripts/sflowtool",shell=True,\
                            stdout=subprocess.PIPE,\
                            stderr=subprocess.PIPE,\
                            close_fds=True)
    _PM.addProcess(res)
    while True:
        try:
            line = res.stdout.readline()
        except:
            log.write("error", "ERROR  reading sflowtool stdout. Err : %s"%err)
            log.write("error", "ERROR  reading sflowtool stdout. Err args: %s"%err.args)
            log.write("error", "ERROR  reading sflowtool stdout. Err message: %s"%err.message)
    
        if line == '':
            log.write("error","ERROR sflowtool read empty line")

        try:
            flow_filter.consume(line)
        except Exception as err:
            log.write("error", "ERROR post sflow data. Err : %s"%err)
            log.write("error", "ERROR post sflow data. Err args: %s"%err.args)
            log.write("error", "ERROR post sflow data. Err message: %s"%err.message)
    
    
   
def update_dev_index_pair(indx_ins_name_pair, lock):
    log.write("info","Enter update_dev_index_pair ")
    qvo_vm_map = {}
    vm_uuid_map = {}

    #lock.acquire()
    old_ifindex_set = set(indx_ins_name_pair.keys())
    #lock.release()

    new_ifindex_set = set()

    status,output = commands.getstatusoutput("ovs-vsctl list-ports br-int")
    log.write("info", "ovs-vsctl ret, status: %s,output %s."%(status, output))

    vm_ports = filter(lambda x:not x=="patch-tun",map(lambda y:y.strip(),output.split("\n")))
    vm_ports_s = set(vm_ports)


    status,output = commands.getstatusoutput("virsh list |awk '/running/ {print $2}' ")
    log.write("info", "virsh list ret, status: %s,output %s."%(status, output))

    vm_names = output.strip().split("\n")
    vm_names = filter(lambda x:len(x)>0,vm_names)
    
    for vm_n in vm_names:
        status,output = commands.getstatusoutput("virsh domiflist %s|awk '/tap/ {print $1}'"%vm_n)
        tap_name = output.strip()
        qvo_name = "qvo"+tap_name[3:]
        qvo_vm_map[qvo_name] = vm_n 

    for vm_n in vm_names:
        cmd = """ps aux|grep %s|grep -v grep|awk '{for(i=0;i<NF;i++)if($i=="-uuid")print $(i+1)}'"""%vm_n
        log.write("info", " get uuid from instance_name, status: %s,output %s."%(status, output))

        status,output = commands.getstatusoutput(cmd)
        uuid = output.strip()
        assert(len(uuid)==36)
        vm_uuid_map[vm_n] = uuid

    vm_qvo_names = qvo_vm_map.keys()
    valid_qvo_names = vm_ports_s & set(vm_qvo_names)
    ifindex_uuid_map = {}
    for qvo_dev_name in valid_qvo_names:
        index_path = "/sys/devices/virtual/net/%s/ifindex"%qvo_dev_name
        status,output = commands.getstatusoutput("cat %s"%index_path)
        ifindex = output.strip("\n").strip()
        if qvo_dev_name in qvo_vm_map:
            vm = qvo_vm_map[qvo_dev_name]
            if vm in vm_uuid_map:
                uuid = vm_uuid_map[vm]
            else:
                log.write("error","ERROR vm %s is not int vm uuid map %s"%(vm, vm_uuid_map))
                break
        else:
            log.write("error","ERROR qvo %s is not int qvo vm map %s"%(qvo_dev_name, qvo_vm_map))
            break

        ifindex_uuid_map[ifindex] = uuid
        # qvo_vm_map only counts running vm
        # hence there would be somw mismatch between vm_ports and qvo_vm_map ,
        # TODO: we should update this map constantly.
        #if qvo_dev_name in qvo_vm_map:
        #    instance_name = qvo_vm_map[qvo_dev_name]
        #    uuid = vm_uuid_map[instance_name]
        #    lock.acquire()
        #    indx_ins_name_pair[ifindex] = uuid
        #    log.write('info','add/update ifindex-uuid pair: %s'%indx_ins_name_pair[ifindex])
        #    lock.release()
        #else:
        #    pass

    for ifindex, uuid in ifindex_uuid_map.items():
        if ifindex not in indx_ins_name_pair:
            lock.acquire()
            # only add here ,don't remove
            indx_ins_name_pair[ifindex] = uuid
            log.write('info','add/update ifindex-uuid pair: %s'%indx_ins_name_pair[ifindex])
            lock.release()
    #garbage_set = old_ifindex_set - new_ifindex_set
    #lock.acquire()
    #for garbage in garbage_set:
    #    log.write('info',"remove old ifindex-uuid pair: %s"%indx_ins_name_pair[garbage])
    #    indx_ins_name_pair.pop(garbage)
    #lock.release()
    log.write("info","%s"%indx_ins_name_pair)
    log.write("info", "Exit update_dev_index_pair ")
    return indx_ins_name_pair

def start_index_pair_updator(index_pair, lock):
    global _PM
    def func():
        retries = 0
        while True:
            #parr = os.getppid()
            #if parr == 1:
            #    break
            try:
                update_dev_index_pair(index_pair, lock)
            except Exception as err:
                
                log.write("error", "ERROR when running index pair updator,will start it again. Err : %s"%err)
                log.write("error", "ERROR when running index pair updator,will start it again. Err args: %s"%err.args)
                log.write("error", "ERROR when running index pair updator,will start it again. Err message: %s"%err.message)
                retries +=1
            if retries > 3:
                sys.exit(1)
            time.sleep(60)



    p = multiprocessing.Process(target=func)
    _PM.addProcess(p)
    p.start()
        #DEV_INDX_HASH[port_dev_name] = ifindex 
def init_dev_index_pair():
    INDX_INS_NAME_HASH = multiprocessing.Manager().dict()
    lock = multiprocessing.Lock()
    INDX_INS_NAME_HASH = update_dev_index_pair(INDX_INS_NAME_HASH, lock)
    start_index_pair_updator(INDX_INS_NAME_HASH, lock)

    return INDX_INS_NAME_HASH,lock

def init():
    clean()
    conf = config.Conf()
    conf.init(_CONF_FILE)
    log.init("./flow_agent")
    return conf

def remove_status_file(path):
    if os.path.exists(path):
        os.remove(path)


def security_start(conf):
    fixed_path = conf.default.prog_status_path
    if os.path.isfile(fixed_path):
        log.write("info", "Prog already exists, stop spawning.")
        sys.exit(2)

    dirname = os.path.dirname(os.path.abspath(fixed_path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(fixed_path, "w") as f:
        f.write(str(os.getpid()))


def grace_exit(conf):
    
    def signal_handler(signum, frame):
        global _PM
        log.write("info", "meet signal: %s"%str(signum))
        log.write("info", "sigterm/sigint received. remove status file and exist")
        prog_status_path = conf.default.prog_status_path
        if os.path.exists(prog_status_path):
            remove_status_file(prog_status_path)

        _PM.killAll()
        sys.exit(0)


    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    conf = init()
    security_start(conf)
    grace_exit(conf)
    index_intance_name_map, lock = init_dev_index_pair()
    sff = sfilter.SFlowFilter(conf.default,index_intance_name_map, lock)
    sff.add_notifier(notifier.YunhaiNotifier(conf.yunhai))
    consume_loop(sff, conf)


