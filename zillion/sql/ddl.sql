create table auth_group
(
	id int auto_increment
		primary key,
	name varchar(150) not null,
	constraint name
		unique (name)
);

create table auth_user
(
	id int auto_increment
		primary key,
	password varchar(128) not null,
	last_login datetime(6) null,
	is_superuser tinyint(1) not null,
	username varchar(150) not null,
	first_name varchar(150) not null,
	last_name varchar(150) not null,
	email varchar(254) not null,
	is_staff tinyint(1) not null,
	is_active tinyint(1) not null,
	date_joined datetime(6) not null,
	constraint username
		unique (username)
);

create table auth_user_groups
(
	id bigint auto_increment
		primary key,
	user_id int not null,
	group_id int not null,
	constraint auth_user_groups_user_id_group_id_94350c0c_uniq
		unique (user_id, group_id),
	constraint auth_user_groups_group_id_97559544_fk_auth_group_id
		foreign key (group_id) references auth_group (id),
	constraint auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table basic
(
	symbol varchar(4) not null comment '商品代号'
		primary key,
	name varchar(16) not null comment '商品名',
	type varchar(8) not null comment '分类',
	amount int not null comment '合同每单位数量',
	unit varchar(4) not null comment '单位',
	step decimal(6,2) not null comment '每跳点数',
	profit int not null comment '每跳毛利',
	exchange varchar(16) not null comment '所属交易所',
	night tinyint not null comment '是否夜盘（0=否 1=是）',
	relative varchar(128) null comment '相关联symbol',
	remark varchar(64) null comment 'remark',
	deleted tinyint default 0 not null,
	update_time timestamp not null on update CURRENT_TIMESTAMP comment '更新时间'
)
comment '合约基本信息';

create table collect
(
	id bigint auto_increment comment '主键id'
		primary key,
	trade_date varchar(10) not null comment '交易日期',
	code varchar(10) not null comment '合约代码',
	name varchar(20) not null comment '合约名称',
	type tinyint(1) not null comment '采集类型',
	price decimal(10,2) not null comment '现价',
	position tinyint default 0 not null comment '相对位置',
	high decimal(10,2) not null comment '最高价',
	low decimal(10,2) not null comment '最低价',
	deal_vol int null comment '交易量',
	hold_vol int null comment '持仓量',
	create_time timestamp default CURRENT_TIMESTAMP not null comment '创建时间',
	remark varchar(64) null
)
comment '定时数据采集分析';

create index idx_future_collect_trade_date
	on collect (trade_date);

create index idx_future_daily_collect_code_date
	on collect (code, trade_date);

create table contract
(
	symbol varchar(4) not null comment '商品代码',
	code varchar(8) not null comment '合约代码'
		primary key,
	ts_code varchar(12) not null comment 'ts code',
	main tinyint default 0 not null comment '主力=1',
	low decimal(10,2) not null comment '合约最低',
	high decimal(10,2) not null comment '合约最高',
	low_time varchar(20) null comment '新低时间',
	high_time varchar(20) null comment '新低时间',
	selected tinyint default 0 not null comment '0=否 1=是',
	create_time datetime not null comment '创建时间',
	update_time datetime not null on update CURRENT_TIMESTAMP comment '更新时间',
	deleted tinyint default 0 not null,
	constraint uidx_contract_symbol_code
		unique (symbol, code),
	constraint uidx_contract_symbol_ts_code
		unique (symbol, ts_code)
)
comment '合约信息';

create index idx_contract_selected
	on contract (selected);

create table contract_hist
(
	symbol varchar(4) not null comment '商品代码',
	code varchar(8) not null comment '合约代码'
		primary key,
	ts_code varchar(12) not null comment 'ts code',
	main tinyint default 0 not null comment '主力=1',
	low decimal(10,2) not null comment '合约最低',
	high decimal(10,2) not null comment '合约最高',
	low_time varchar(20) null comment '新低时间',
	high_time varchar(20) null comment '新低时间',
	selected tinyint default 0 not null comment '0=否 1=是',
	create_time datetime not null comment '创建时间',
	update_time datetime not null comment '更新时间',
	deleted tinyint default 0 not null,
	constraint uidx_contract_symbol_code
		unique (symbol, code),
	constraint uidx_contract_symbol_ts_code
		unique (symbol, ts_code)
)
comment '历史合约信息';

create table django_content_type
(
	id int auto_increment
		primary key,
	app_label varchar(100) not null,
	model varchar(100) not null,
	constraint django_content_type_app_label_model_76bd3d3b_uniq
		unique (app_label, model)
);

create table auth_permission
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	content_type_id int not null,
	codename varchar(100) not null,
	constraint auth_permission_content_type_id_codename_01ab375a_uniq
		unique (content_type_id, codename),
	constraint auth_permission_content_type_id_2f476e4b_fk_django_co
		foreign key (content_type_id) references django_content_type (id)
);

create table auth_group_permissions
(
	id bigint auto_increment
		primary key,
	group_id int not null,
	permission_id int not null,
	constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
		unique (group_id, permission_id),
	constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
		foreign key (permission_id) references auth_permission (id),
	constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
		foreign key (group_id) references auth_group (id)
);

create table auth_user_user_permissions
(
	id bigint auto_increment
		primary key,
	user_id int not null,
	permission_id int not null,
	constraint auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
		unique (user_id, permission_id),
	constraint auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
		foreign key (permission_id) references auth_permission (id),
	constraint auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table django_admin_log
(
	id int auto_increment
		primary key,
	action_time datetime(6) not null,
	object_id longtext null,
	object_repr varchar(200) not null,
	action_flag smallint unsigned not null,
	change_message longtext not null,
	content_type_id int null,
	user_id int not null,
	constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
		foreign key (content_type_id) references django_content_type (id),
	constraint django_admin_log_user_id_c564eba6_fk_auth_user_id
		foreign key (user_id) references auth_user (id)
);

create table django_migrations
(
	id bigint auto_increment
		primary key,
	app varchar(255) not null,
	name varchar(255) not null,
	applied datetime(6) not null
);

create table django_session
(
	session_key varchar(40) not null
		primary key,
	session_data longtext not null,
	expire_date datetime(6) not null
);

create index django_session_expire_date_a5c62663
	on django_session (expire_date);

create table future_user
(
	id int auto_increment
		primary key,
	username varchar(100) not null,
	password varchar(100) not null
);

create table gap_log
(
	ts_code varchar(20) not null,
	code varchar(16) null comment 'code',
	start_date varchar(10) null comment '产生缺口日期',
	end_date varchar(10) not null comment '缺口结束日期',
	gap_type varchar(10) not null comment '类型',
	start_price decimal(10,2) not null comment '缺口开始价格',
	cpos decimal(10,1) not null comment '合约位置',
	end_price decimal(10,2) not null comment '缺口结束价格',
	gap_rate decimal(10,2) not null comment '缺口大小%',
	is_fill tinyint default 0 not null comment '是否已回补（0=未回补，1=已回补）',
	fill_date varchar(10) null comment '回补日期',
	`check` tinyint null,
	create_time datetime null comment '插入时间',
	update_time datetime null comment '更新时间',
	constraint idx_gap_log_code_date
		unique (code, start_date)
)
comment '缺口记录';

create table gap_log_test
(
	ts_code varchar(20) not null,
	code varchar(16) null comment 'code',
	start_date varchar(10) null comment '产生缺口日期',
	end_date varchar(10) not null comment '缺口结束日期',
	gap_type varchar(10) not null comment '类型',
	start_price decimal(10,2) not null comment '缺口开始价格',
	end_price decimal(10,2) not null comment '缺口结束价格',
	gap_rate decimal(10,2) not null comment '缺口大小%',
	is_fill tinyint default 0 not null comment '是否已回补（0=未回补，1=已回补）',
	fill_date varchar(10) null comment '回补日期',
	`check` tinyint null,
	create_time datetime null comment '插入时间',
	update_time datetime null comment '更新时间',
	constraint idx_gap_log_code_date
		unique (code, start_date)
)
comment '缺口记录';

create table live
(
	trade_date varchar(10) not null comment 'trade date',
	code varchar(8) not null comment '合约code'
		primary key,
	type varchar(8) not null comment '品种',
	name varchar(16) not null comment '合约名',
	price decimal(10,2) not null comment '现价',
	`change` decimal(10,2) not null comment '涨跌幅%',
	position tinyint default 0 not null comment '相对位置%',
	bid1 decimal(10,2) null comment 'buy 1',
	ask1 decimal(10,2) null comment 'sell 1',
	open decimal(10,2) null comment '开',
	low decimal(10,2) null comment '最低',
	high decimal(10,2) null comment '最高',
	amp decimal(10,2) null comment '振幅%',
	lowest_change decimal(10,2) null comment '历史最低涨跌幅%',
	highest_change decimal(10,2) null comment '历史最高涨跌幅%',
	wave varchar(64) null comment '波动',
	update_time time not null comment '最新更新时间'
)
comment '实时';

create index idx_future_live_trade_date_code
	on live (trade_date, code);

create table n_stat
(
	code text null,
	close_change double null,
	settle_change double null,
	up tinyint(1) null,
	days bigint null,
	`3d_change` double null,
	`5d_change` double null,
	`7d_change` double null,
	price double null,
	settle double null,
	avg5d bigint null,
	avg10d bigint null,
	avg20d bigint null,
	avg60d bigint null,
	p5t10 double null,
	pt5 double null,
	pt10 double null,
	pt20 double null,
	pt60 double null,
	trend_up tinyint(1) null,
	change_list text null,
	update_time datetime null
);

create table open_gap
(
	trade_date varchar(10) not null comment 'trade date',
	code varchar(8) not null,
	name varchar(10) not null comment 'name',
	category varchar(8) default '' not null comment 'category',
	pre_close decimal(10,2) not null comment 'pre close',
	pre_settle decimal(10,2) not null comment 'pre settle',
	pre_high decimal(10,2) null comment 'pre high',
	pre_low decimal(10,2) null comment 'pre low',
	open decimal(10,2) not null comment 'current open',
	open_change decimal(10,2) not null comment 'open change',
	gap_rate decimal(10,2) not null comment 'gap rate',
	day_gap tinyint null comment 'is day gap',
	contract_position tinyint not null comment 'contract relative pos',
	remark varchar(64) null comment 'remark',
	buy_low decimal(10,2) not null comment 'low price for buy',
	sell_high decimal(10,2) not null comment 'high price for sell',
	suggest tinyint default 0 not null comment '-1=sell, 0=none, 1=buy',
	suggest_price decimal(10,2) null comment 'suggest price',
	create_time timestamp default CURRENT_TIMESTAMP not null,
	constraint uidx_open_gap_code_trade_date
		unique (code, trade_date)
)
comment 'open gap log';

create index idx_open_gap_trade_date
	on open_gap (trade_date);

create table trade_daily
(
	id bigint auto_increment comment '主键id'
		primary key,
	symbol varchar(6) not null comment '商品代码',
	trade_date varchar(10) not null comment '交易日期',
	code varchar(10) null comment '合约代码',
	open decimal(10,2) null comment '开盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	close decimal(10,2) null comment '收盘价',
	settle decimal(10,2) null comment '结算价',
	pre_close decimal(10,2) null comment '昨收盘价',
	pre_settle decimal(10,2) null comment '昨结算价',
	close_change decimal(10,2) null comment '昨收盘价涨跌幅',
	settle_change decimal(10,2) null comment '结算价涨跌幅',
	deal_vol int null comment '交易量',
	hold_vol int null comment '持仓量',
	create_time datetime not null comment '创建时间',
	constraint uidx_future_daily_trade_date_contract_code
		unique (trade_date, code)
)
comment '每日行情';

create index idx_future_daily_code
	on trade_daily (symbol);

create index idx_future_daily_code_date
	on trade_daily (code, trade_date);

create table trade_log
(
	id bigint auto_increment comment 'id'
		primary key,
	trade_date varchar(10) not null comment 'trade date',
	code varchar(8) not null comment 'contract code',
	name varchar(10) not null comment '合约名称',
	type varchar(10) null comment '类型',
	factor int null comment '监控因子',
	diff decimal(10,2) null comment '监控值',
	content varchar(64) null comment '内容',
	`option` varchar(6) not null comment '操作选择',
	suggest decimal(10,2) not null comment '建议价格',
	pct_change decimal(10,2) null comment '当前涨跌幅',
	position int null comment '相对位置',
	log_time timestamp default CURRENT_TIMESTAMP not null comment '时间',
	remark varchar(32) null comment '备注'
)
comment '行情日志';

create index idx_future_log_code_date
	on trade_log (code, trade_date);

create index idx_future_log_trade_date
	on trade_log (trade_date);

create index uidx_future_log
	on trade_log (code, type, factor, suggest, position);

create table ts_contract
(
	ts_code varchar(16) not null comment '合约代码'
		primary key,
	symbol varchar(8) not null comment '交易标识',
	exchange varchar(8) not null comment '交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心',
	name varchar(16) null comment '中文简称',
	fut_code varchar(8) null comment '合约产品代码',
	type tinyint not null comment '合约类型（1=连续 2=主力）'
)
comment '合约列表';

create table ts_holding
(
	trade_date varchar(10) not null comment '日期',
	symbol varchar(10) not null comment '合约代码',
	broker varchar(10) not null comment '会员简称',
	vol int default 0 not null comment '成交量',
	vol_chg int default 0 not null comment '成交量变化',
	long_hld int default 0 not null comment '持买仓量',
	long_chg int default 0 not null comment '持买仓量变化',
	short_hld int default 0 not null comment '持卖仓量',
	short_chg int default 0 not null comment '持卖仓量变化',
	constraint idx_ts_future_holding_trade_date
		unique (trade_date, symbol, broker)
)
comment '持仓变化';

create table ts_trade_daily
(
	ts_code varchar(16) not null comment 'TS合约代码',
	trade_date varchar(10) not null comment '交易日期',
	pre_close decimal(10,2) null comment '昨收盘价',
	pre_settle decimal(10,2) null comment '昨结算价',
	open decimal(10,2) not null comment '开盘价',
	high decimal(10,2) not null comment '最高价',
	low decimal(10,2) not null comment '最低价',
	close decimal(10,2) not null comment '收盘价',
	settle decimal(10,2) not null comment '结算价',
	close_change decimal(10,2) not null comment '昨收盘价涨跌幅',
	settle_change decimal(10,2) not null comment '结算价涨跌幅',
	deal_vol int default 0 null comment '成交量(手)',
	deal_amount decimal(10,2) null comment '成交金额(万元)',
	hold_vol int default 0 null comment '持仓量(手)',
	hold_change int default 0 null comment '持仓量变化',
	create_time datetime not null comment '创建时间',
	constraint idx_ts_future_daily_code_date
		unique (ts_code, trade_date)
)
comment '日线数据';

create table ts_trade_daily_hist
(
	ts_code varchar(16) not null comment 'TS合约代码',
	trade_date varchar(10) not null comment '交易日期',
	pre_close decimal(10,2) null comment '昨收盘价',
	pre_settle decimal(10,2) null comment '昨结算价',
	open decimal(10,2) not null comment '开盘价',
	high decimal(10,2) not null comment '最高价',
	low decimal(10,2) not null comment '最低价',
	close decimal(10,2) not null comment '收盘价',
	settle decimal(10,2) not null comment '结算价',
	close_change decimal(10,2) not null comment '昨收盘价涨跌幅',
	settle_change decimal(10,2) not null comment '结算价涨跌幅',
	deal_vol int default 0 null comment '成交量(手)',
	deal_amount decimal(10,2) null comment '成交金额(万元)',
	hold_vol int default 0 null comment '持仓量(手)',
	hold_change int default 0 null comment '持仓量变化',
	create_time datetime not null comment '创建时间',
	constraint idx_ts_future_daily_code_date
		unique (ts_code, trade_date)
)
comment '历史日数据';

create table wave
(
	code text null,
	start text null,
	end text null,
	a double null,
	b double null,
	c double null,
	d double null,
	ap double null,
	bp double null,
	cp double null,
	dp double null,
	p double null,
	update_time datetime null
);

create table wave_detail
(
	code text null,
	begin text null,
	end text null,
	status text null,
	begin_price double null,
	end_price double null,
	`change` double null,
	days bigint null
);

create table wave_hist
(
	code text null,
	start text null,
	end text null,
	a double null,
	b double null,
	c double null,
	d double null,
	ap double null,
	bp double null,
	cp double null,
	dp double null,
	p double null
);

create table week_stat
(
	code varchar(16) not null,
	week varchar(10) not null,
	`change` decimal(10,1) null,
	pct_change decimal(10,2) null,
	constraint future_week_stat_pk
		unique (code, week)
);

