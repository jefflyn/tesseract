create table wave_info
(
	code varchar(6) not null comment 'code'
		primary key,
	from_date varchar(10) not null comment '开始日期',
	to_date varchar(10) not null comment '结束时间',
	wave_a decimal(10,2) not null comment 'a波',
	wave_b decimal(10,2) null comment 'b波',
	wave_c decimal(10,2) null comment 'c波',
	adays int not null,
	bdays int null,
	cdays int null,
	update_time timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间'
)
comment '一波接一波';

