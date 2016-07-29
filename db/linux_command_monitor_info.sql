drop table if exists linux_command_monitor_info;

/*==============================================================*/
/* Table: linux_command_monitor_info                            */
/*==============================================================*/
create table linux_command_monitor_info
(
   oid                  bigint not null auto_increment,
   access_time          datetime comment '命令执行时间',
   exec_command         varchar(500) comment '用户执行命令',
   exec_result          varchar(2000) comment '执行结果',
   exec_user            varchar(80) comment '所使用的用户(如：root，jboss)',
   original_user        varchar(80) comment '原始用户root',
   local_ip             varchar(20) comment '本机IP地址',
   user_ip              varchar(20) comment '执行命令的用户来源IP',
   operator_status      varchar(100) comment '此字段可为空',
   container_oid        varchar(100) comment '业务系统Oid',
   aciton               smallint not null comment '数据是否已经同步到 linux_command_info表中，true是，false没有',
   status               int,
   primary key (oid)
);

alter table linux_command_monitor_info comment 'Linux_主机层面命令执行监视';