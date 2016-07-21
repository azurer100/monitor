/*
Navicat MySQL Data Transfer

Source Server         : Imseam
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : imseam

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2016-07-18 17:45:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `linux_file_monitor_info`
-- ----------------------------
DROP TABLE IF EXISTS `linux_file_monitor_info`;
CREATE TABLE `linux_file_monitor_info` (
  `oid` bigint(20) NOT NULL AUTO_INCREMENT,
  `access_time` datetime DEFAULT NULL,
  `operator_status` varchar(100) DEFAULT NULL COMMENT '文件操作状态一共3中包括：detected creation of(创建)，detected deletion of(删除)，detected modification to(修改),在数据增加表中，我会翻译成添加，删除，修改3中状态',
  `operator_path` varchar(200) DEFAULT NULL COMMENT '文件路径(操作的文件路径)',
  `process_name` varchar(80) DEFAULT NULL COMMENT '操作的进程名（/bin/rm）',
  `exec_user` varchar(80) DEFAULT NULL COMMENT '所使用的用户(root)',
  `original_user` varchar(80) DEFAULT NULL COMMENT '原始用户root',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '本机IP地址',
  `file_md5` varchar(100) DEFAULT NULL,
  `container_oid` varchar(100) DEFAULT NULL COMMENT '业务系统Oid',
  `aciton` smallint(6) NOT NULL COMMENT '数据是否已经同步到 windows_process_info表中，true是，false没有',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Linux_主机层面文件变化监视';

-- ----------------------------
-- Records of linux_file_monitor_info
-- ----------------------------
INSERT INTO `linux_file_monitor_info` VALUES ('1', '2016-04-30 06:23:17', 'file/floder delete', '/123/1.txt', '/bin/rm', 'root', 'root', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `linux_file_monitor_info` VALUES ('2', '2016-04-30 05:26:31', 'file/floder modification', '/123/111.txt', '/bin/bash', 'root', 'root', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `linux_file_monitor_info` VALUES ('3', '2016-05-03 06:27:50', 'file/floder create', '/123/456', '/bin/touch', 'root', 'root', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
