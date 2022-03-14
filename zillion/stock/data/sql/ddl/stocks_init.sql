create schema stocks collate utf8mb4_0900_ai_ci;

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

create index idx_basic_code
	on basic (code);

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

create table basics
(
	trade_date varchar(10) not null comment '交易日',
	code varchar(6) not null comment '股票代码'
		primary key,
	ts_code varchar(10) not null comment '股票ts代码',
	name varchar(8) not null comment '股票名称',
	industry varchar(10) null comment '行业',
	area varchar(8) null comment '地区',
	list_date int(8) null comment '上市日期',
	pe decimal(10,2) null comment '动态市盈率',
	circulate_shares decimal(10,2) null comment '流通股本',
	total_shares decimal(10,2) null comment '总股本(万)',
	total_assets decimal(10,2) null comment '总资产(万)',
	liquid_assets decimal(10,2) null comment '流动资产(万)',
	fixed_assets decimal(10,2) null comment '固定资产(万)',
	reserved decimal(10,2) null comment '公积金',
	reserved_per_share decimal(10,2) null comment '每股公积金(元)',
	esp decimal(10,3) null comment '每股收益(元)',
	bvps decimal(10,2) null comment '每股净资产(元)',
	bp decimal(10,2) null comment '市净率',
	undp decimal(10,2) null comment '未分配利润',
	undp_per_share decimal(10,2) null comment '每股未分配利润(元)',
	revenue decimal(10,2) null comment '营业总收入(亿)',
	profit decimal(10,2) null comment '利润(亿)',
	gpr decimal(10,2) null comment '毛利率(%)',
	npr decimal(10,2) null comment '资产净利率(%)',
	holders int(10) null comment '股东人数'
)
comment '上市公司基本情况';

create table concept
(
	code text null,
	name text null,
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
	grade decimal(10,2) null comment '等级分数（越高越靓）',
	price decimal(10,2) null,
	ma5 decimal(10,2) null,
	ma10 decimal(10,2) null,
	ma20 decimal(10,2) null,
	ma30 decimal(10,2) null,
	ma60 decimal(10,2) null,
	ma90 decimal(10,2) null,
	ma120 decimal(10,2) null,
	ma250 decimal(10,2) null,
	create_time datetime null,
	constraint hist_ma_day_pk
		unique (trade_date, code)
);

create index idx_hist_ma_day_code
	on hist_ma_day (code);



create index idx_hist_ma_day_code
	on hist_ma_day (code);

create table hist_monthly
(
	trade_date varchar(10) default '' not null comment '交易日',
	ts_code varchar(10) default '' not null comment 'ts code',
	code varchar(6) not null comment '代码',
	amt_change decimal(10,2) null comment '涨跌额',
	pct_change decimal(10,2) null comment '涨跌幅',
	pre_close decimal(10,2) null comment '上一个交易日收盘价',
	open decimal(10,2) null comment '开盘价',
	close decimal(10,2) null comment '收盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	volume int null comment '交易量（手）',
	amount decimal(20,4) null comment '交易额（千）',
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

create table index_hist_k
(
	trade_date varchar(10) not null,
	code varchar(10) not null,
	open decimal(10,2) not null,
	close decimal(10,2) not null,
	high decimal(10,2) not null,
	low decimal(10,2) not null,
	volume decimal(15,2) not null,
	pct_change decimal(10,2) not null,
	primary key (trade_date, code)
);

create table limit_up_daily
(
	trade_date varchar(10) not null comment '交易日',
	code varchar(6) not null comment '股票代码',
	name varchar(8) not null comment '名称',
	area varchar(8) null comment '区域',
	industry varchar(10) null comment '行业',
	open_change decimal(10,2) not null comment '开盘涨幅',
	close_change decimal(10,2) not null comment '涨幅',
	combo int not null comment '连涨次数',
	create_time timestamp default CURRENT_TIMESTAMP not null comment '创建时间',
	primary key (trade_date, code)
)
comment '每日涨停榜';

create index idx_limit_up_daily_code
	on limit_up_daily (code);

create table limit_up_stat
(
	fire_date varchar(10) not null comment '首次涨停交易日',
	late_date varchar(10) null comment '最近一次涨停日期',
	code varchar(6) not null comment '股票代码'
		primary key,
	name varchar(10) null comment '股票名称',
	industry varchar(10) null comment '行业',
	fire_price decimal(10,2) null comment '涨停日最低价',
	price decimal(10,2) null comment '开盘涨跌幅',
	combo int not null comment '连续涨停数',
	count int not null comment '总涨停次数',
	wave_a decimal(10,2) not null comment 'a波幅度',
	wave_b decimal(10,2) not null comment 'b波幅度',
	wave_str varchar(100) null comment 'wave_str',
	create_time datetime null
);

create table monitor_pool
(
	name varchar(4) null,
	code varchar(6) not null
		primary key,
	alert_price varchar(80) null,
	percent_change varchar(40) null,
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
	grade varchar(3) default '0' null,
	hold_date date null,
	close_date date null,
	remark varchar(255) null,
	alias varchar(8) null,
	concept varchar(255) null,
	constraint my_stock_pool_pk
		unique (code, platform)
);

create table period_change
(
	code text null,
	name text null,
	from_date text null,
	low_price double null,
	period_change double null,
	hz_change text null,
	sz_change text null,
	cy_change text null,
	`50_change` text null,
	`300_change` text null,
	zx_change text null
);

create table select_result_all
(
	concepts text null,
	code text null,
	name text null,
	industry text null,
	area text null,
	list_date text null,
	pe double null,
	pe_ttm double null,
	pct double null,
	wave_a double null,
	wave_b double null,
	map text null,
	count bigint null,
	count_ bigint null,
	wave_detail text null,
	a_days bigint null,
	b_days bigint null,
	bottom double null,
	uspace double null,
	dspace double null,
	top double null,
	position double null,
	w_gap double null,
	c_gap double null,
	gap double null,
	gap_space double null,
	sum_30d double null,
	c30d bigint null,
	cq1 bigint null,
	cq2 bigint null,
	cq3 bigint null,
	cq4 bigint null,
	fdate text null,
	last_f_date text null,
	price double null,
	call_price text null,
	call_diff double null,
	lup_low double null,
	lup_high double null,
	buy1 double null,
	buy2 double null,
	buy3 double null,
	change_7d text null,
	updays double null,
	sumup double null,
	vol_rate double null,
	multi_vol text null,
	turnover_rate bigint null,
	trade_date text null,
	select_time datetime null
);

create table select_wave_all
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

