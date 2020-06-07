create table wave_data
(
	code varchar(6) null comment 'code',
	from_date varchar(10) null comment '开始日期',
	to_date varchar(10) null comment '结束时间',
	wave_a decimal(10,2) null comment 'a波',
	wave_b decimal(10,2) null comment 'b波',
	wave_c decimal(10,2) null comment 'c波',
	update_time timestamp null comment '更新时间',
	constraint wave_data_pk
		primary key (code)
)
comment '一波接一波';

