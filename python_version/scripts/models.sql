create database sflow;

use sflow;

DROP TABLE IF EXISTS abnormal_record;

create TABLE `abnormal_record` (
    `aid` int(11) NOT NULL auto_increment,
    `uuid` varchar(36),
    `start` datetime DEFAULT NULL,
    `end` datetime DEFAULT NULL,
    `stats` TEXT,
    PRIMARY KEY (`aid`)
);
create table network_flow_summary ( 
    `nfid` int(11) NOT NULL auto_increment, 
    `uuid` varchar(36), 
    `ctime` datetime DEFAULT NULL, 
    `summary` TEXT, 
    PRIMARY KEY (`nfid`) 
    );