#!/usr/bin/env python
# encoding: utf-8
'''
monitor.collector -- shortdesc

monitor.collector is a description

It defines classes_and_methods

@author:     Yi

@copyright:  2016 MY. All rights reserved.
'''

import ConfigParser
import socket, sys, time, logging
import MySQLdb
from encode import Encode

logging.basicConfig(level=logging.DEBUG, filename='/home/su/git/monitor/logs/collector.log')
logging.info("Starting collector...")

bufsize = 1500
port = 10514

class Config:
    def __init__(self, path = "./collector.ini"):
        
        cf = ConfigParser.ConfigParser()
        cf.read(path)

        #return all section
        secs = cf.sections()
        logging.info("config sections: %s" % secs)
 
        encode = cf.get("other", "encode")
 
        self.db_host = cf.get("db", "host")
        self.db_port = cf.getint("db", "port")
        self.db_user = cf.get("db", "user")
        if(encode == "0"):
            self.db_pw = cf.get("db", "pw")
            self.db_pw_b = Encode.encrypt(self.db_pw)
        else:
            self.db_pw_b = cf.get("db", "pw")
            self.db_pw = Encode.decrypt(self.db_pw_b)
            
        self.db_name = cf.get("db", "name")
        
        self.sl_host = cf.get("syslog", "host")
        self.sl_port = cf.getint("syslog", "port")
 
 
        #modify one value and write to file
        cf.set("db", "pw", self.db_pw_b)
        cf.set("other", "encode", "1")
        cf.write(open(path, "w"))
    
def main():
    config = Config()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config.sl_host, config.sl_port))
    except Exception, e:
        logging.error("error bind syslog port: " + str(e.args))
        sys.exit(1)
    
    try:
        sql_fs = "insert into linux_file_monitor_info values(%s,%s,%s,%s,%s,%s)"
        conn = MySQLdb.connect(host=config.db_host, db=config.db_name, port=config.db_port, user=config.db_user, passwd=config.db_pw,
                               connect_timeout=10, use_unicode=True, autocommit=True)
        curs = conn.cursor()
    except Exception, e:
        logging.error("mysql can not be connected: " + str(e.args))
        sys.exit(1)
        
    logging.info("syslog is start collect")
    try:
        while 1:
            try:
                data, addr = sock.recvfrom(bufsize)
                syslog = str(data)
                n = syslog.find('>')
                syslog_msg = syslog[26:]
                file_path_action = syslog_msg[:syslog_msg.find(' ')]
                file_name = syslog_msg[syslog_msg.find(' ')]
                process_name = syslog_msg[syslog_msg.find(' ')]
                exec_user = syslog_msg[syslog_msg.find(' ')]
                ori_user = syslog_msg[syslog_msg.find(' ')]
                file_md5 = syslog_msg[syslog_msg.find(' '):]
                param = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), file_path_action, file_name, process_name, exec_user, ori_user, 
                         addr[0], file_md5, None, '1', None)
                curs.execute(sql_fs, param)
                logging.info("syslog: %s" % syslog_msg)
            except socket.error:
                logging.error("syslog collection failed")
                pass
    except Exception, e:
        curs.close()
        conn.close()
        logging.error("syslog stop: " + str(e.args))
        sys.exit()
if __name__ == '__main__':
    main()
