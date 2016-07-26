#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''
import socket, time
class Syslog:
    def __init__(self, ip, port):
        self.address = (ip, port)
         
        self.level = 3
        self.facility = 16
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, who, log):
        if len(log) == 0:
            return False
        msg = '<%d> %s %s %s: %s' % ((self.level + self.facility*8), time.strftime("%b %d %H:%M:%S %Y", time.localtime()), socket.gethostname(), who, log)
        self.s.sendto(msg, self.address)
        
    def __delete__(self):
        self.s.close()
    
def main():
    pass
    syslog = Syslog("127.0.0.1", 10514)
    syslog.send('linux_fs', "hello 1 1 1 1 1")

if __name__ == "__main__":
    main()
