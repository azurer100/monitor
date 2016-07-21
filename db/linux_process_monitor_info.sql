/*
Navicat MySQL Data Transfer

Source Server         : Imseam
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : imseam

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2016-07-18 17:46:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `linux_process_monitor_info`
-- ----------------------------
DROP TABLE IF EXISTS `linux_process_monitor_info`;
CREATE TABLE `linux_process_monitor_info` (
  `oid` bigint(20) NOT NULL AUTO_INCREMENT,
  `access_time` datetime DEFAULT NULL,
  `process_status` varchar(100) DEFAULT NULL COMMENT '程序变化类型:启动(detected start of process),推出(detected exit of process)',
  `file_path` varchar(200) DEFAULT NULL COMMENT '文件路径',
  `pid` int(11) DEFAULT NULL,
  `process_name` varchar(80) DEFAULT NULL COMMENT '进程名',
  `ppid` int(11) DEFAULT NULL,
  `parent_process_name` varchar(80) DEFAULT NULL COMMENT '父进程名称',
  `exec_user` varchar(80) DEFAULT NULL COMMENT '执行账户',
  `original_user` varchar(80) DEFAULT NULL COMMENT '原始账户',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '本机IP地址',
  `file_md5` varchar(100) DEFAULT NULL,
  `container_oid` varchar(100) DEFAULT NULL COMMENT '业务系统Oid',
  `aciton` smallint(6) NOT NULL COMMENT '数据是否已经同步到 windows_process_info表中，true是，false没有',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Linux_主机层面进程层面监视';

-- ----------------------------
-- Records of linux_process_monitor_info
-- ----------------------------
INSERT INTO `linux_process_monitor_info` VALUES ('1', '2016-04-29 06:16:46', 'process start', '/usr/bin/id', '3172', '/bin/bash', '2445', '/bin/bash', 'root', 'root', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
