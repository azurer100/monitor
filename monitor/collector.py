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
import socket, time, string, logging
import MySQLdb
from encode import Encode

logging.basicConfig(level=logging.DEBUG,
                    filename='logs/collector.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
                    datefmt='%d %b %Y %H:%M:%S')

bufsize = 1500
port = 10514

sql_linux_fs = "INSERT INTO linux_file_monitor_info(`access_time`,`operator_status`,`operator_path`,`process_name`,`exec_user`,`original_user`,`local_ip`,`file_md5`,`container_oid`,`aciton`,`status`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_linux_ps = "INSERT INTO linux_process_monitor_info(`access_time`,`process_status`,`file_path`,`pid`,`process_name`,`ppid`,`parent_process_name`,`exec_user`,`original_user`,`local_ip`,`file_md5`,`aciton`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_linux_net = "INSERT INTO linux_network_monitor_info(`access_time`,`loacl_address`,`foreign_address`,`state`,`protolcol`,`pid`,`progame_name`,`network_status`,`container_oid`,`aciton`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_linux_cmd = "INSERT INTO linux_command_monitor_info(`access_time`,`exec_command`,`exec_result`,`exec_user`,`original_user`,`local_ip`,`user_ip`,`operator_status`,`container_oid`,`aciton`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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
    
def linux_fs(ip, syslog):
    items = syslog.split(" ")
    file_path_action = items[0]
    file_name = items[1]
    process_name = items[2]
    exec_user = items[3]
    ori_user = items[4]
    file_md5 = items[5]
    return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), file_path_action, file_name, process_name, exec_user, ori_user, 
             ip, file_md5, None, "1", None)
    
def linux_ps(ip, syslog):
    items = syslog.split(" ")
    return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(items[1]))), items[0], items[2], items[3], items[4], items[5],
            items[6], items[7], items[8], ip, "", "1")

def linux_net(ip, syslog):
    items = syslog.split(" ")
    return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(items[0]))), items[1], items[2], items[3], items[4], (items[5] if items[5] != "" else None),
            items[6], items[7], None, "1")
    
def linux_cmd(ip, syslog):
    items = syslog.split(" ")
    return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(items[0]))), items[1], items[2], items[3], items[4], ip, items[5],
            None, None, "1")
    
def main():
    logging.info("starting collector...")
    
    config = Config()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config.sl_host, config.sl_port))
    except Exception, e:
        logging.error("error bind syslog port: " + str(e.args))
    
    try:
        conn = MySQLdb.connect(host=config.db_host, db=config.db_name, port=config.db_port, user=config.db_user, passwd=config.db_pw,
                               connect_timeout=10, use_unicode=True, autocommit=True)
        curs = conn.cursor()
    except Exception, e:
        logging.error("mysql can not be connected: " + str(e.args))
        
    logging.info("syslog is start to collect")
    try:
        while 1:
            try:
                data, addr = sock.recvfrom(bufsize)
                syslog = str(data)
                logging.debug("syslog: %s" % syslog)
                
#               <131> Jul 26 11:34:47 2016 ubuntu linux_fs: hello 1 1 1 1 1 1 1
                n = syslog.find('>')
                serverty=string.atoi(syslog[1:n])&0x0007
                facility=(string.atoi(syslog[1:n])&0x03f8)>>3
                syslog_msg = syslog[27:]
                host = syslog_msg[:syslog_msg.find(' ')]
                syslog_msg = syslog[28+len(host) :]
                who = syslog_msg[:syslog_msg.find(': ')]
                syslog_msg = syslog[30+len(host + who) :]
                
                if (who == "linux_fs"):
                    param = linux_fs(addr[0], syslog_msg)
                    curs.execute(sql_linux_fs, param)
                    
                if (who == "linux_ps"):
                    param1 = linux_ps(addr[0], syslog_msg)
                    curs.execute(sql_linux_ps, param1)
                    
                if (who == "linux_net"):
                    param2 = linux_net(addr[0], syslog_msg)
                    curs.execute(sql_linux_net, param2)
                    
                if (who == "linux_cmd"):
                    param3 = linux_cmd(addr[0], syslog_msg)
                    curs.execute(sql_linux_cmd, param3)
                    
                logging.info("syslog: %s" % syslog_msg)
            except socket.error:
                logging.error("syslog collection failed")
                pass
    except Exception, e:
        logging.error("syslog stop: " + str(e.args))
        sock.close()
        curs.close()
        conn.close()
#         sys.exit()
        time.sleep(10)
        main()
        
if __name__ == '__main__':
    main()
    
syslog_serverty={ 0:"emergency",
                   1:"alert",
                   2:"critical",
                   3:"error",
                   4:"warning",
                   5:"notice",
                   6:"info",
                   7:"debug"
                 }
syslog_facility={ 0:"kernel",
                   1:"user",
                   2:"mail",
                   3:"daemaon",
                   4:"auth",
                   5:"syslog",
                   6:"lpr",
                   7:"news",
                   8:"uucp",
                   9:"cron",
                   10:"authpriv",
                   11:"ftp",
                   12:"ntp",
                   13:"security",
                   14:"console",
                   15:"cron",
                   16:"local 0",
                   17:"local 1",
                   18:"local 2",
                   19:"local 3",
                   20:"local 4",
                   21:"local 5",
                   22:"local 6",
                   23:"local 7"
                 }
