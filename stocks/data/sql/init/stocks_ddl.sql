create schema stocks collate utf8_unicode_ci;

create table basic
(
	ts_code varchar(10) not null comment 'TS代码'
		primary key,
	code varchar(6) null comment '股票代码',
	name varchar(8) null comment '股票名称',
	area varchar(10) null comment '所在地域',
	industry varchar(10) null comment '所属行业',
	fullname varchar(30) null comment '股票全称',
	market varchar(10) null comment '市场类型 （主板/中小板/创业板）',
	exchange varchar(8) null comment '交易所代码',
	curr_type varchar(3) null comment '交易货币',
	list_status varchar(1) null comment '上市状态： L上市 D退市 P暂停上市',
	list_date int(10) null comment '上市日期',
	delist_date varchar(10) null comment '退市日期',
	is_hs varchar(1) null comment '是否沪深港通标的，N否 H沪股通 S深股通',
	constraint ix_symbol
		unique (code)
)
comment '基础信息数据';

create index ix_list_date
	on basic (list_date);

create table basic_daily
(
	ts_code text null,
	trade_date text null,
	close double null,
	turnover_rate double null,
	turnover_rate_f double null,
	volume_ratio double null,
	pe double null,
	pe_ttm double null,
	pb double null,
	ps double null,
	ps_ttm double null,
	total_share double null,
	float_share double null,
	free_share double null,
	total_mv double null,
	circ_mv double null,
	code text null
);

create table cctv_news
(
	date text null,
	title text null,
	content text null
);

create table concept
(
	code varchar(20) not null
		primary key,
	name varchar(50) null,
	src text null
);

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

create table daily_gap_trace_a
(
	s_date varchar(10) null,
	v_date varchar(10) null,
	code varchar(6) null,
	name varchar(10) null,
	industry varchar(10) null,
	cost decimal(10,2) null,
	share int null,
	bottom decimal(10,2) null,
	b_up decimal(10,2) null,
	position decimal(10,2) null,
	gap decimal(10,2) null,
	g_space decimal(10,2) null,
	c30d int null,
	vol decimal(10,2) null,
	uds int null,
	o_profit decimal(10,2) null comment '开盘价买入收益',
	l_profit decimal(10,2) null comment '最低价买入收益',
	constraint daily_gap_trace_pk
		unique (s_date, code)
);

create index daily_gap_trace_a_v_date_code_index
	on daily_gap_trace_a (v_date, code);

create table daily_gap_trace_b
(
	s_date varchar(10) null,
	v_date varchar(10) null,
	code varchar(6) null,
	name varchar(10) null,
	industry varchar(10) null,
	cost decimal(10,2) null,
	share int null,
	bottom decimal(10,2) null,
	b_up decimal(10,2) null,
	position decimal(10,2) null,
	gap decimal(10,2) null,
	g_space decimal(10,2) null,
	c30d int null,
	vol decimal(10,2) null,
	uds int null,
	o_profit decimal(10,2) null,
	l_profit decimal(10,2) null,
	constraint daily_gap_trace_b_pk
		unique (s_date, code)
);

create index daily_gap_trace_b_v_date_code_index
	on daily_gap_trace_b (v_date, code);

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
	ts_code varchar(10) null,
	`rank` varchar(3) null,
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
		unique (trade_date, ts_code)
);

create table hist_monthly
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) null,
	pre_close decimal(10,2) null comment '上一个交易日收盘价',
	open decimal(10,2) null comment '开盘价',
	close decimal(10,2) null comment '收盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	vol bigint null comment '交易量（手）',
	amount decimal(20,4) null comment '交易额（千）',
	amt_change decimal(10,2) null comment '涨跌额',
	pct_change decimal(10,4) null comment '涨跌幅',
	update_time timestamp default CURRENT_TIMESTAMP null,
	primary key (trade_date, ts_code)
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
	alias varchar(4) null,
	code varchar(6) not null,
	concept varchar(20) null,
	platform varchar(10) null,
	cost decimal(10,3) null,
	bottom decimal(10,2) null,
	share int default 100 not null,
	is_hold tinyint default 1 null,
	grade varchar(3) default 'c' null,
	hold_date date null,
	close_date date null,
	remark varchar(255) null,
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

create table select_result_
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_result_all
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_result_concept
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_result_region
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_result_temp
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap bigint null,
	gap_space bigint null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_result_wave
(
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date bigint null,
	price double null,
	pct double null,
	wave_detail text null,
	wave_a double null,
	wave_b double null,
	bottom double null,
	`uspace%` double null,
	`dspace%` double null,
	top double null,
	`position%` double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	count bigint null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	lldate text null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	`sumup%` double null,
	vol_rate double null,
	multi_vol text null,
	trade_date text null,
	select_time datetime null
);

create table select_wave_
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days double null,
	`change` double null
);

create table select_wave_all
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days double null,
	`change` double null
);

create table select_wave_concept
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days bigint null,
	`change` double null
);

create table select_wave_region
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days bigint null,
	`change` double null
);

create table select_wave_temp
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days double null,
	`change` double null
);

create table select_wave_wave
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days double null,
	`change` double null
);

create table stock_company
(
	ts_code text null,
	exchange text null,
	chairman text null,
	manager text null,
	secretary text null,
	reg_capital double null,
	setup_date text null,
	province text null,
	city text null,
	website text null,
	email text null,
	employees bigint null
);

create table wave_change_normal_ref
(
	`range` double null,
	avg_range double null,
	count bigint null,
	ratio double null,
	avg_change double null,
	min_change double null,
	max_change double null
);

create table wave_change_st_ref
(
	`range` double null,
	avg_range double null,
	count bigint null,
	ratio double null,
	avg_change double null,
	min_change double null,
	max_change double null
);

create table wave_change_subnew_ref
(
	`range` double null,
	avg_range double null,
	count bigint null,
	ratio double null,
	avg_change double null,
	min_change double null,
	max_change double null
);

create table wave_data_2019
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	days bigint null,
	`change` double null
);

create table weekly_gap
(
	code text null,
	name text null,
	industry text null,
	area text null,
	change_7_days text null,
	gap double null,
	gap_space double null,
	multi_vol text null,
	vol_rate double null
);

