/*
Navicat MySQL Data Transfer

Source Server         : Imseam
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : imseam

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2016-07-18 17:45:46
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `windows_regedit_monitor_info`
-- ----------------------------
DROP TABLE IF EXISTS `windows_regedit_monitor_info`;
CREATE TABLE `windows_regedit_monitor_info` (
  `oid` bigint(20) NOT NULL AUTO_INCREMENT,
  `access_time` datetime DEFAULT NULL,
  `regedit_status` varchar(100) DEFAULT NULL COMMENT '行为关键字(创建注册表KEY,删除注册表KEY,修改内容,删除具体键值)',
  `operator_path` varchar(200) DEFAULT NULL COMMENT '此处对应了操作的注册表的对象，包括4类：创建KEY的路径和名称,删除KEY的对象，所在的KEY的路径，所在的路径',
  `operatoar_object` varchar(100) DEFAULT NULL,
  `process_name` varchar(80) DEFAULT NULL COMMENT '操作的程序',
  `exec_user` varchar(80) DEFAULT NULL COMMENT '所使用的用户(JIESHEN-037914DAdministrator)',
  `original_user` varchar(80) DEFAULT NULL COMMENT '原始用户',
  `local_ip` varchar(20) DEFAULT NULL COMMENT '本机IP地址',
  `container_oid` varchar(100) DEFAULT NULL COMMENT '业务系统Oid',
  `aciton` smallint(1) NOT NULL COMMENT '数据是否已经同步到 windows_process_info表中，true是，false没有',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='主机注册表层面监视';

-- ----------------------------
-- Records of windows_regedit_monitor_info
-- ----------------------------
INSERT INTO `windows_regedit_monitor_info` VALUES ('1', '2016-04-19 20:18:54', 'detected creation of registry key', 'HKEY_LOCAL_MACHINE\\SAM\\New Key #1', null, 'C:\\WINDOWS\\regedit.exe', 'JIESHEN-037914D\\Administrator', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_regedit_monitor_info` VALUES ('2', '2016-04-21 05:35:56', 'detected deletion of registry key', 'HKEY_LOCAL_MACHINE\\SAM\\New Key #1', null, 'C:\\WINDOWS\\regedit.exe', 'JIESHEN-037914D\\AdministratorJIESHEN-037914D\\Administrator', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_regedit_monitor_info` VALUES ('3', '2016-04-22 05:37:47', 'detected modification to registry', 'HKEY_LOCAL_MACHINE\\SAM\\New Key #1', '\'New Value #1\' of type \'SZ\'', 'C:\\WINDOWS\\regedit.exe', 'JIESHEN-037914D\\Administrator', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
INSERT INTO `windows_regedit_monitor_info` VALUES ('4', '2016-04-21 05:42:06', 'detected deletion of registry value', 'HKEY_LOCAL_MACHINE\\SAM\\New Key #1', 'New Value #1', 'C:\\WINDOWS\\regedit.exe', 'JIESHEN-037914D\\Administrator', 'JIESHEN-037914D\\Administrator', '192.168.10.231', 'cbb36801-c563-4a8f-a310-8f7fdce5542d', '1', null);
