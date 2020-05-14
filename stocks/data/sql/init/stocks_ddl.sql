create table concept_detail
(
	concept_code varchar(10) null comment '概念代码',
	ts_code varchar(10) null comment '股票代码',
	code varchar(6) null,
	name varchar(10) null comment '股票名称',
	in_date varchar(10) null comment '纳入日期',
	out_date varchar(10) null comment '剔除日期',
	constraint concept_detail_pk
		unique (concept_code, ts_code)
)
comment '概念股列表';

create index concept_detail_concept_code_code_index
	on concept_detail (concept_code, code);

create table concepts
(
	code varchar(6) not null
		primary key,
	concepts varchar(200) null
);

create table hist_index_day
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) null,
	pre_close decimal(10,4) null comment '上一个交易日收盘价',
	open decimal(10,4) null comment '开盘价',
	close decimal(10,4) null comment '收盘价',
	high decimal(10,4) null comment '最高价',
	low decimal(10,4) null comment '最低价',
	vol int null comment '交易量（手）',
	amount decimal(15,4) null comment '交易额（千）',
	amt_change decimal(10,4) null comment '涨跌额',
	pct_change decimal(10,4) null comment '涨跌幅',
	update_time timestamp default CURRENT_TIMESTAMP null,
	primary key (trade_date, ts_code)
)
comment '每日指数数据';

create index hist_index_day_code_index
	on hist_index_day (code);

create index ix_pct_change
	on hist_index_day (pct_change);

create index ix_ts_code
	on hist_index_day (ts_code);

create table hist_ma_day
(
	trade_date varchar(10) null,
	code varchar(10) not null,
	grade varchar(3) null,
	price decimal(10,2) null,
	ma5 decimal(10,2) null,
	ma10 decimal(10,2) null,
	ma20 decimal(10,2) null,
	ma30 decimal(10,2) null,
	ma60 decimal(10,2) null,
	ma90 decimal(10,2) null,
	ma120 decimal(10,2) null,
	ma250 decimal(10,2) null,
	constraint hist_ma_day_pk
		unique (trade_date, code)
);

create table hist_monthly
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) not null comment '代码',
	pre_close decimal(10,2) null comment '上一个交易日收盘价',
	open decimal(10,2) null comment '开盘价',
	close decimal(10,2) null comment '收盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	volume int null comment '交易量（手）',
	amount decimal(20,4) null comment '交易额（千）',
	amt_change decimal(10,2) null comment '涨跌额',
	pct_change decimal(10,4) null comment '涨跌幅',
	create_time timestamp default CURRENT_TIMESTAMP null,
	primary key (trade_date, ts_code),
	constraint idx_hist_monthly_date_code
		unique (trade_date, code)
)
comment '周交易数据（前复权）';

create index ix_code
	on hist_monthly (code);

create index ix_pct_change
	on hist_monthly (pct_change);

create index ix_ts_code
	on hist_monthly (ts_code);



create table hist_trade_day
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) null,
	pre_close decimal(10,2) null comment '上一个交易日收盘价',
	open decimal(10,2) null comment '开盘价',
	close decimal(10,2) null comment '收盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	vol int(9) null comment '交易量（手）',
	amount decimal(15,4) null comment '交易额（千）',
	amt_change decimal(10,2) null comment '涨跌额',
	pct_change decimal(10,4) null comment '涨跌幅',
	update_time timestamp default CURRENT_TIMESTAMP null,
	primary key (trade_date, ts_code)
)
comment '每日交易数据（前复权）';

create index hist_trade_day_date_index
	on hist_trade_day (trade_date);

create index ix_code
	on hist_trade_day (code);

create index ix_pct_change
	on hist_trade_day (pct_change);

create index ix_ts_code
	on hist_trade_day (ts_code);

create table hist_weekly
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) null,
	pre_close decimal(10,2) null comment '上一个交易日收盘价',
	open decimal(10,2) null comment '开盘价',
	close decimal(10,2) null comment '收盘价',
	low decimal(10,2) null comment '最低价',
	high decimal(10,2) null comment '最高价',
	vol bigint null comment '交易量（手）',
	amount decimal(20,4) null comment '交易额（千）',
	amt_change decimal(10,2) null comment '涨跌额',
	pct_change decimal(10,4) null comment '涨跌幅',
	update_time timestamp default CURRENT_TIMESTAMP null,
	primary key (trade_date, ts_code)
)
comment '周交易数据（前复权）';

create index ix_code
	on hist_weekly (code);

create index ix_pct_change
	on hist_weekly (pct_change);

create index ix_ts_code
	on hist_weekly (ts_code);

create table limitup_stat
(
	code varchar(6) null,
	period_type varchar(10) null comment '[y,q,m,w,d]',
	period varchar(10) null,
	times int null
);

create table monitor_pool
(
	name varchar(4) null,
	code varchar(6) not null
		primary key,
	alert_price varchar(80) null,
	percent_change varchar(20) null,
	receive_mobile varchar(20) null,
	is_valid int default 1 null
);

create table my_stock_pool
(
	code varchar(6) not null,
	platform varchar(10) null,
	share int default 100 not null,
	cost decimal(10,3) null,
	bottom decimal(10,2) null,
	is_hold tinyint default 1 null,
	grade varchar(3) default 'c' null,
	hold_date date null,
	close_date date null,
	remark varchar(255) null,
	alias varchar(4) null,
	concept varchar(20) null,
	constraint my_stock_pool_pk
		unique (code, platform)
);

create table profit_forecast
(
	code text null,
	name text null,
	type text null,
	report_date text null,
	pre_eps double null,
	`range` text null,
	range_from float null,
	range_to float null
);


