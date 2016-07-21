/*
Navicat MySQL Data Transfer

Source Server         : Imseam
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : imseam

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2016-07-18 17:45:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `windows_file_monitor_info`
-- ----------------------------
DROP TABLE IF EXISTS `windows_file_monitor_info`;
CREATE TABLE `windows_file_monitor_info` (
  `oid` bigint(20) NOT NULL AUTO_INCREMENT,
  `access_time` datetime DEFAULT NULL,
  `operator_status` varchar(100) DEFAULT NULL COMMENT '文件操作状态一共3中包括：create(创建)，delte(删除)，change(修改)',
  `operator_path` varchar(200) DEFAULT NULL COMMENT '文件路径(操作的文件路径)',
  `process_name` varchar(80) DEFAULT NULL COMMENT '操作的程序（C:WINDOWSexplorer.exe）',
  `exec_user` varchar(80) DEFAULT NULL COMMENT '所使用的用户(JIESHEN-037914DAdministrator)',
  `original_user` varchar(80) DEFAULT NULL COMMENT '原始用户',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '本机IP地址',
  `file_md5` varchar(100) DEFAULT NULL,
  `container_oid` varchar(100) DEFAULT NULL COMMENT '业务系统Oid',
  `aciton` smallint(6) NOT NULL COMMENT '数据是否已经同步到 windows_process_info表中，true是，false没有',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='主机层面文件变化监视';

-- ----------------------------
-- Records of windows_file_monitor_info
-- ----------------------------
INSERT INTO `windows_file_monitor_info` VALUES ('1', '2016-04-27 05:54:39', 'file/floder delete', 'C:\\123\\file.txt', 'C:\\WINDOWS\\explorer.exe', 'JIESHEN-037914D\\Administrator', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_file_monitor_info` VALUES ('2', '2016-04-28 06:01:44', 'file/floder change', 'C:\\123\\file.txt', 'C:\\WINDOWS\\system32\\notepad.exe', ' JIESHEN-037914D\\Administrator', ' JIESHEN-037914D\\Administrator', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_file_monitor_info` VALUES ('3', '2016-04-28 06:10:15', 'file/floder create', 'C:\\123\\file.txt', 'C:\\WINDOWS\\explorer.exe', ' JIESHEN-037914D\\Administrator', ' JIESHEN-037914D\\Administrator', '192.168.10.231', 'dd47ff16176412ec2e170cda441b4a220ff52f46', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
