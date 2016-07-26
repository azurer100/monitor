#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''

import os ,pyinotify, logging, pwd, hashlib, io, time
from client import Syslog

class MyEventHandler(pyinotify.ProcessEvent):
    WHO = 'linux_fs'
    
    def __init__(self, ip, port):
        logging.info("linux file system monitor starting ...")
        self.syslog = Syslog(ip, port)
    
    def process_IN_CREATE(self, event):
        if event.dir:
            return
        file1_path = event.pathname
        stat_info = os.stat(file1_path)
        uid = stat_info.st_uid
        process = ""
        exec_user = pwd.getpwuid(uid)[0]
        ori_user = pwd.getpwuid(uid)[0]
        md5_value = md5(file1_path)
    
        log = "create %s %s %s %s %s" % (event.pathname, process, exec_user, ori_user, md5_value)
        self.syslog.send(MyEventHandler.WHO, log)
      
    def process_IN_DELETE(self, event):
        if event.dir:
            return
        process = ""
        exec_user = ""
        ori_user = ""
        md5_value = ""
        
        log = "delete %s %s %s %s %s" % (event.pathname, process, exec_user, ori_user, md5_value)
        self.syslog.send(MyEventHandler.WHO, log)
      
    def process_IN_MODIFY(self, event):
        if event.dir:
            return
        file1_path = event.pathname
        stat_info = os.stat(file1_path)
        uid = stat_info.st_uid
        process = ""
        exec_user = pwd.getpwuid(uid)[0]
        ori_user = pwd.getpwuid(uid)[0]
        md5_value = md5(file1_path)
        
        log = "modification %s %s %s %s %s" % (event.pathname, process, exec_user, ori_user, md5_value)
        self.syslog.send(MyEventHandler.WHO, log)
     
def md5(file_path):
    m = hashlib.md5()
    file1 = io.FileIO(file_path, 'r')
    bytes1 = file1.read(1024)
    while(bytes1 != b''):
        m.update(bytes1)
        bytes1 = file1.read(1024)
    file1.close()
    
    return m.hexdigest()
     
def main():
    try:
        wm = pyinotify.WatchManager()
        wm.add_watch('/home/su/git/monitor/test', pyinotify.ALL_EVENTS, rec=True)
        eh = MyEventHandler()
     
        # notifier
        notifier = pyinotify.Notifier(wm, eh)
        notifier.loop()
        
    except Exception, e:
        logging.error("linux file system monitor stop: " + str(e.args))
        time.sleep(10)
        main()
 
if __name__ == '__main__':
    main()
