/*
Navicat MySQL Data Transfer

Source Server         : Imseam
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : imseam

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2016-07-18 17:45:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `windows_process_monitor_info`
-- ----------------------------
DROP TABLE IF EXISTS `windows_process_monitor_info`;
CREATE TABLE `windows_process_monitor_info` (
  `oid` bigint(20) NOT NULL AUTO_INCREMENT,
  `access_time` datetime DEFAULT NULL,
  `process_status` varchar(100) DEFAULT NULL COMMENT '程序变化类型',
  `file_path` varchar(200) DEFAULT NULL COMMENT '文件路径',
  `pid` int(11) DEFAULT NULL,
  `process_name` varchar(80) DEFAULT NULL COMMENT '进程名',
  `ppid` int(11) DEFAULT NULL,
  `parent_process_name` varchar(80) DEFAULT NULL COMMENT '父进程名称',
  `file_md5` varchar(60) DEFAULT NULL COMMENT '校验和',
  `exec_user` varchar(80) DEFAULT NULL COMMENT '执行账户',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '本机IP地址',
  `container_oid` varchar(100) DEFAULT NULL COMMENT '业务系统Oid',
  `aciton` smallint(6) NOT NULL COMMENT '数据是否已经同步到 windows_process_info表中，true是，false没有',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='Windows_主机层面进程层面监视';

-- ----------------------------
-- Records of windows_process_monitor_info
-- ----------------------------
INSERT INTO `windows_process_monitor_info` VALUES ('1', '2016-07-18 16:45:12', 'process start', 'C:\\WINDOWS\\system32\\cmd.exe', '2720', 'C:\\WINDOWS\\explorer.exe', '1936', 'C:\\WINDOWS\\system32\\userinit.exe', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_process_monitor_info` VALUES ('2', '2016-04-20 14:18:10', 'process stop', 'C:\\WINDOWS\\system32\\cmd.exe', '2720', 'C:\\WINDOWS\\explorer.exe', '1936', 'C:\\WINDOWS\\system32\\userinit.exe', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_process_monitor_info` VALUES ('3', '2016-04-20 15:18:20', 'process start', 'C:\\WINDOWS\\system32\\cmd.exe', '2720', 'C:\\WINDOWS\\explorer.exe', '1936', 'C:\\WINDOWS\\system32\\net.exe', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_process_monitor_info` VALUES ('4', '2016-04-20 15:28:20', 'process start', 'C:\\WINDOWS\\system32\\cmd.exe', '2720', 'C:\\WINDOWS\\explorer.exe', '1936', 'C:\\WINDOWS\\system32\\net.exe', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
