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

# logging.basicConfig(level=logging.DEBUG)

class Ps:
    WHO = 'linux_ps'
    WHO_NET = 'linux_net'
    WHO_CMD = 'linux_cmd'
    
    def __init__(self, syslog):
        logging.info("linux file process monitor starting ...")
        logging.info("linux netstat monitor starting ...")
        logging.info("linux command monitor starting ...")
        self.__w_infos = {}
        self.__ps_cur = {}
        self.__ps_new = {}
        self.__net_cur = {}
        self.syslog = syslog
        
    def start(self, config):
        while 1:
            try:
                self.__do_process(config.ps_excludes)
                self.__do_netstat(config.net_includes)
                time.sleep(config.delay)
            except Exception, e:
                logging.error("linux process monitor error: " + str(e.args))
    
    def __do_process(self, ps_excludes):
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
                if infos[8] in ps_excludes:
                    continue
                ps_flag = False
                for ps_exclude in ps_excludes:
                    if infos[8].find(ps_exclude) != -1:
                        ps_flag = True
                        break
                if ps_flag:
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
                ip = self.__w_infos.has_key(add[6])
            else:
                ip = '127.0.0.1'
                
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
                ip = self.__w_infos.has_key(d[6])
            else:
                ip = '127.0.0.1'
                
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
            
        for add in add_arr:
            if add[6].find("pts") == -1:
                continue
            if self.__w_infos.has_key(add[6]):
                ip = self.__w_infos.has_key(add[6])
            else:
                ip = '127.0.0.1'
            
            access_time = time.time()
            file_path = add[8]
            pid = add[1]
            process_name = add[8]
            if len(add) > 9:
                process_name = process_name + "\t" + add[9]
            ppid = add[2]
            if self.__ps_cur.has_key(ppid):
                ppname = self.__ps_cur[ppid][8]
            else:
                ppname = ''
            exec_user = original_user = add[0]
            
            log = "%s %s %s %s %s %s" % (access_time, process_name, "", exec_user, original_user, ip)
            self.syslog.send(Ps.WHO_CMD, log)
            
    def __do_netstat(self, includes):
        ptn = re.compile("\s+")
        p1 = Popen(["netstat", "-anp"], stdout=PIPE)
                
        output = p1.communicate()[0];del p1
        processes = output.strip().split("\n")
        
        add_arr = []
        net_new = {}
        for process in processes[2:]:
            if process:
                if process.find("Active UNIX domain soc") != -1:
                    break
                infos = ptn.split(process)
                net_new[infos[3] + "-" + infos[4]] = infos
        
        if len(self.__net_cur) != 0:
            for n_key in net_new:
                if not self.__net_cur.has_key(n_key):
                    add_arr.append(net_new[n_key])
                    
        logging.debug("current networks count: %d" % len(self.__net_cur))
        logging.debug("new networks count: %d" % len(net_new))
        self.__net_cur = copy.copy(net_new)
        
        for add in add_arr:
            if len(add) < 8:
                add.insert(5, "")
            
            access_time = time.time()
            ip = add[3][:add[3].rfind(":")]
            port = add[3][add[3].rfind(":")+1:]
            
            pn = add[6].split("/")
            if len(pn) == 2:
                pid = pn[0]
                pname = pn[1]
            else:
                pid = ""
                pname = ""
            
            if port in includes.strip().split(","):
                network_status = 1
            else:
                network_status = 2
            
            log = "%s %s %s %s %s %s %s %s" % (access_time, add[3], add[4], add[5], add[0], pid, pname, network_status)
            self.syslog.send(Ps.WHO_NET, log)
            
def main():
    try:
        ps = Ps(1)
        ps.start(10)
    except Exception, e:
        logging.error("linux process monitor stop: " + str(e.args))
        logging.error("linux command monitor stop: " + str(e.args))
        logging.error("linux networks monitor stop: " + str(e.args))
 
if __name__ == '__main__':
    main()
