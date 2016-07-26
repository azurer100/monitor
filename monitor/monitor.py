#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''
import ConfigParser, logging, fs, time

logging.basicConfig(level=logging.INFO,
                    filename='/home/su/git/monitor/logs/monitor.log',
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
        
        self.fs_path = cf.get("fs", "path")
        self.sl_ip = cf.get("syslog", "ip")
        self.sl_port = cf.getint("syslog", "port")
        
def main():
    config = Config()
    
    try:
        wm = fs.pyinotify.WatchManager()
        wm.add_watch(config.fs_path, fs.pyinotify.ALL_EVENTS, rec=True)
        eh = fs.MyEventHandler(config.sl_ip, config.sl_port)
     
        # notifier
        notifier = fs.pyinotify.Notifier(wm, eh)
        notifier.loop()
        
    except Exception, e:
        logging.error("linux file system monitoring stop: " + str(e.args))
        time.sleep(10)
        main()
 
if __name__ == '__main__':
    main()
    
    