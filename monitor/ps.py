#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''

from subprocess import Popen
from subprocess import PIPE
import logging, time, re, copy

logging.basicConfig(level=logging.DEBUG)

class Ps:
    WHO = 'linux_ps'
    
    def __init__(self, syslog):
        logging.info("linux file process starting ...")
        self.__w_infos = {}
        self.__ps_cur = {}
        self.__ps_new = {}
        self.syslog = syslog
        
    def start(self, delay):
        while 1:
            try:
                self.__do_process()
                time.sleep(delay)
            except Exception, e:
                logging.error("linux process monitor error: " + str(e.args))
    
    def __do_process(self):
        ptn = re.compile("\s+")
        p1 = Popen(["ps", "-efc"], stdout=PIPE)
        p2 = Popen(["w", "-h"], stdout=PIPE)
        
        output = p2.communicate()[0];del p2
        itmes = output.strip().split("\n")
        for item in itmes:
            if item:
                infos = ptn.split(item)
                self.__w_infos[infos[0]+"-"+infos[1]] = infos[2]
                
        output = p1.communicate()[0];del p1
        processes = output.strip().split("\n")
        del_arr = []
        add_arr = []
        
        self.__ps_new = {}
        for process in processes[1:]:
            if process:
                infos = ptn.split(process)
                if infos[8] in ("w", "ps", "[w]", "[ps]", "/usr/bin/python", "python", "[python]"):
                    continue
                self.__ps_new[infos[1]] = infos
                
        if len(self.__ps_cur) != 0:
            for c_key in self.__ps_cur:
                if not self.__ps_new.has_key(c_key):
                    del_arr.append(self.__ps_cur[c_key])
            for n_key in self.__ps_new:
                if not self.__ps_cur.has_key(n_key):
                    add_arr.append(self.__ps_new[n_key])
                            
        logging.debug("current processes count: %d" % len(self.__ps_cur))
        logging.debug("new processes count: %d" % len(self.__ps_new))
        self.__ps_cur = copy.copy(self.__ps_new)
        
        for add in add_arr:
            if self.__w_infos.has_key(add[6]):
                add[6] = self.__w_infos.has_key(add[6])
            else:
                add[6] = '127.0.0.1'
                
            access_time = time.time()
            file_path = add[8]
            pid = add[1]
            process_name = add[8]
            ppid = add[2]
            if self.__ps_cur.has_key(ppid):
                ppname = self.__ps_cur[ppid][8]
            else:
                ppname = ''
            exec_user = original_user = add[0]
            
            log = "start %s %s %s %s %s %s %s %s" % (access_time, file_path, pid, process_name, ppid, ppname, exec_user, original_user)
            self.syslog.send(Ps.WHO, log)
        for d in del_arr:
            if self.__w_infos.has_key(d[6]):
                d[6] = self.__w_infos.has_key(d[6])
            else:
                d[6] = '127.0.0.1'
                
            access_time = time.time()
            file_path = d[8]
            pid = d[1]
            process_name = d[8]
            ppid = d[2]
            if self.__ps_cur.has_key(ppid):
                ppname = self.__ps_cur[ppid][8]
            else:
                ppname = ''
            exec_user = original_user = d[0]
            
            log = "stop %s %s %s %s %s %s %s %s" % (access_time, file_path, pid, process_name, ppid, ppname, exec_user, original_user)
            self.syslog.send(Ps.WHO, log)

def main():
    try:
        ps = Ps()
        ps.start(3)
    except Exception, e:
        logging.error("linux process monitor stop: " + str(e.args))
        main()
 
if __name__ == '__main__':
    main()
