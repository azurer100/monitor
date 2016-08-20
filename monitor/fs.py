#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''

import os ,pyinotify, logging, pwd, hashlib, io, time, threading

class MyEventHandler(pyinotify.ProcessEvent):
    WHO = 'linux_fs'
    
    def __init__(self, syslog):
        logging.info("linux file system monitor starting ...")
        self.syslog = syslog
        self.__m_hash = {}
        self.__c_hash = {}
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
    
    def process_IN_CREATE(self, event):
        if event.dir:
            return
        file1_path = event.pathname
        if file1_path.find(".swpx") != -1:
            return
        if file1_path.find("~") != -1:
            return
        if file1_path.find(".swp") != -1:
            return
        stat_info = os.stat(file1_path)
        uid = stat_info.st_uid
        process = ""
        exec_user = pwd.getpwuid(uid)[0]
        ori_user = pwd.getpwuid(uid)[0]
        md5_value = md5(file1_path)
        if self.__anti_same_md5(2, md5_value):
            return
    
        log = "create %s %s %s %s %s" % (event.pathname, process, exec_user, ori_user, md5_value)
        self.syslog.send(MyEventHandler.WHO, log)
      
    def process_IN_DELETE(self, event):
        if event.dir:
            return
        file1_path = event.pathname
        if file1_path.find(".swpx") != -1:
            return
        if file1_path.find("~") != -1:
            return
        if file1_path.find(".swp") != -1:
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
        if file1_path.find(".swpx") != -1:
            return
        if file1_path.find("~") != -1:
            return
        if file1_path.find(".swp") != -1:
            return
        
        stat_info = os.stat(file1_path)
        uid = stat_info.st_uid
        process = ""
        exec_user = pwd.getpwuid(uid)[0]
        ori_user = pwd.getpwuid(uid)[0]
        md5_value = md5(file1_path)
        if self.__anti_same_md5(1, md5_value):
            return
        
        log = "modification %s %s %s %s %s" % (event.pathname, process, exec_user, ori_user, md5_value)
        self.syslog.send(MyEventHandler.WHO, log)
        
    def __anti_same_md5(self, type, md5):
        if type == 1:
            t = time.time()
            
            if not self.__m_hash.has_key(md5):
                self.__m_hash[md5] = t
                return False
            else:
                return True
            
            self.lock1.acquire()
            tmp_m = {}
            for m_key in self.__m_hash:
                if t - self.__m_hash[m_key] < 6.0:
                    tmp_m[m_key] = self.__m_hash[m_key]
            self.__m_hash = tmp_m
            self.lock1.release()
            
        if type == 2:
            t = time.time()
            
            if not self.__c_hash.has_key(md5):
                self.__c_hash[md5] = t
                return False
            else:
                return True
            
            self.lock2.acquire()
            tmp_c = {}
            for c_key in self.__c_hash:
                if t - self.__c_hash[c_key] < 6.0:
                    tmp_c[c_key] = self.__c_hash[c_key]
            self.__c_hash = tmp_c
            self.lock2.release()
     
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
