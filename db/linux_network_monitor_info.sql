drop table if exists linux_network_monitor_info;



/*==============================================================*/

/* Table: linux_network_monitor_info                            */

/*==============================================================*/

create table linux_network_monitor_info

(

   oid                  bigint not null auto_increment,

   access_time          datetime comment '命令执行时间',

   loacl_address        varchar(50) comment '本地ip,端口',

   foreign_address      varchar(50) comment '远程IP 端口',

   state                varchar(20) comment '端口隐射状态',

   protolcol            varchar(20) comment '使用的协议',

   pid                  int comment '进程ID',

   progame_name         varchar(100) comment '程序名',

   network_status       int comment '网络状态，1 默认启动（agent启动采集默认端口），2 新启动ip或端口（后期新增的端口）',

   container_oid        varchar(100) comment '业务系统Oid',

   aciton               smallint not null comment '数据是否已经同步到 linux_network_info表中，true是，false没有',

   status               int,

   primary key (oid)

);



alter table linux_network_monitor_info comment 'Linux_网络层面命令执行监视';