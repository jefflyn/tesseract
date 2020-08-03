create table select_x
(
	code varchar(6) not null
		primary key,
	name varchar(10) not null,
	industry varchar(8) not null,
	concept varchar(64) not null,
	pe decimal(10,2) default 0.00 not null,
	wave_a decimal(10,2) default 0.00 not null,
	wave_b decimal(10,2) default 0.00 not null,
	combo int default 0 not null,
	l_count int default 0 not null,
	map decimal(10,2) default 0.00 not null,
	issue_date int default 0 not null,
	issue_price decimal(10,2) not null,
	issue_space decimal(10,2) null,
	fire_price decimal(10,2) null,
	fire_space decimal(10,2) null,
	on_target tinyint default 1 null comment '0=否，1=是',
	wave_str varchar(100) null,
	select_type varchar(10) not null,
	select_time varchar(10) not null,
	update_time timestamp null
);

