#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''
import ConfigParser, logging, fs, time, ps, threading
from client import Syslog

logging.basicConfig(level=logging.DEBUG,
                    filename='logs/monitor.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
                    datefmt='%d %b %Y %H:%M:%S')

logging.info("starting monitor...")

class Config:
    def __init__(self, path = "./monitor.ini"):
        cf = ConfigParser.ConfigParser()
        cf.read(path)
        
        #return all section
        secs = cf.sections()
        logging.info("config sections: %s" % secs)
        
        self.fs_path = cf.get("fs", "path").split(",")
        self.sl_ip = cf.get("syslog", "ip")
        self.sl_port = cf.getint("syslog", "port")
        
        self.ps_excludes = cf.get("ps", "excludes").split(",")
        
        self.net_includes = cf.get("net", "includes")
        
        self.delay = cf.getint("other", "delay")
        
def start_fs(config, syslog):
    try:
        wm = fs.pyinotify.WatchManager()
        wm.add_watch(config.fs_path, fs.pyinotify.ALL_EVENTS, rec=True)
        eh = fs.MyEventHandler(syslog)
         
        # notifier
        notifier = fs.pyinotify.Notifier(wm, eh)
        notifier.loop()
            
    except Exception, e:
        logging.error("linux file system monitoring stop: " + str(e.args))
        time.sleep(10)
        start_fs(config, syslog)
        
def start_ps(config, syslog):
    try:
        ps1 = ps.Ps(syslog)
        ps1.start(config)
    except Exception, e:
        logging.error("linux process monitor stop: " + str(e.args))
        time.sleep(10)
        start_ps(config, syslog)
        
def main():
    config = Config()
    syslog = Syslog(config.sl_ip, config.sl_port)

    threads = []
    t1 = threading.Thread(target=start_ps, args=(config, syslog))
    t2 = threading.Thread(target=start_fs, args=(config, syslog))
    threads.append(t1)
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
 
if __name__ == '__main__':
    main()
    
    