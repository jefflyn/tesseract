create table stocks.limit_up_stat
(
	trade_date varchar(10) not null comment '交易日',
	code varchar(6) not null comment '股票代码',
	name varchar(10) null comment '股票名称',
	industry varchar(10) null comment '行业',
	area varchar(10) null comment '地区',
	combo_times int not null comment '连续涨停数',
	pe decimal(10,2) null comment '动态市盈率',
	wave_a decimal(10,2) not null comment 'a波幅度',
	wave_b decimal(10,2) not null comment 'b波幅度',
	turnover_rate decimal(10,2) null comment '换手率',
	vol_rate decimal(10,2) null comment '量比',
	open_change decimal(10,2) null comment '开盘涨跌幅',
	next_low_than_open tinyint null comment '次日最低价是否小于开盘价(0-否，1-是)',
	next_open_change decimal(10,2) null comment '次日开盘涨跌幅',
	next_open_buy_change decimal(10,2) null comment '次日开盘价买入当天盈亏（T+1）',
	next_low_buy_change decimal(10,2) null comment '次日最低价买入当天盈亏（T+1）',
	ref_index_change decimal(10,2) null comment '对应大盘指数涨跌幅',
	create_time datetime null comment '插入时间',
	update_time datetime null comment '更新时间',
	constraint idx_limit_up_stat_trade_date_code
		unique (trade_date, code)
);

create index idx_limit_up_stat_code
	on stocks.limit_up_stat (code);

