create table future_basics
(
	goods_type varchar(6) not null comment ' 商品类型（1=能源化工,2=黑色金属,3=贵金属,4=有色金属,5=农产品,6=金融板块）',
	code varchar(6) not null comment '代码',
	name varchar(15) null comment '名称',
	symbol varchar(18) not null comment 'sina code',
	low decimal(10,2) not null comment '最低价',
	high decimal(10,2) not null comment '最高价',
	alert_on tinyint null comment '提醒设置（0=关，1=开）',
	alert_price varchar(64) null comment '提醒价格',
	alert_change varchar(20) null comment '提醒涨跌幅',
	alert_mobile varchar(18) null comment '接收提醒手机号',
	amount int not null comment '每手单位数',
	unit varchar(3) not null comment '单位',
	`limit` tinyint not null comment '涨跌幅限制%',
	margin_std tinyint default 0 null comment '标准保证金率',
	margin tinyint default 0 null comment '保证金率',
	fee_type tinyint null comment '1-按合约价值；2-按手数',
	fee_std decimal(8,6) null comment '标准费用',
	fee decimal(8,6) null comment '开平费用',
	lqd_fee decimal(8,6) null comment '平今费用',
	night tinyint default 0 null comment '是否支持夜盘（0=否，1=是）',
	exchange varchar(10) not null comment '所属交易所',
	target tinyint default 0 null comment '0=否 1=是',
	deleted tinyint default 0 null comment '删除（不关注）1=删除',
	update_remark varchar(32) null comment '更新备注',
	update_time datetime null comment '系统更新价格时间',
	constraint future_basics_pk
		unique (goods_type, name)
)
comment 'future基本信息';

create index future_basics_code_index
	on future_basics (code);

create index future_basics_symbol_index
	on future_basics (symbol);



create table future_log
(
	id bigint auto_increment comment 'id'
		primary key,
	name varchar(20) not null comment '合约名称',
	type varchar(10) null comment '类型',
	content varchar(64) null comment '内容',
	price decimal(10,2) null comment '当前价格',
	pct_change decimal(10,2) null comment '当前涨跌幅',
	position int null comment '相对位置',
	log_time datetime not null comment '时间',
	remark varchar(32) null comment '备注'
)
comment '日志';



create table future_daily
(
	trade_date varchar(10) not null comment '交易日期',
	name varchar(20) not null comment '合约名称',
	s_change decimal(10,2) null comment '结算价涨跌幅',
	p_change decimal(10,2) null comment '昨收盘价涨跌幅',
	close decimal(10,2) null comment '收盘价',
	settle decimal(10,2) null comment '结算价',
	open decimal(10,2) null comment '开盘价',
	high decimal(10,2) null comment '最高价',
	low decimal(10,2) null comment '最低价',
	hl_diff decimal(10,2) null comment '高低价差',
	amplitude decimal(10,2) null comment '振幅',
	pre_close decimal(10,2) null comment '昨收盘价',
	pre_settle decimal(10,2) null comment '昨结算价',
	deal_vol int null comment '交易量',
	hold_vol int null comment '持仓量',
	exchange varchar(10) null comment '交易所',
	constraint idx_future_daily_trade_date_name
		unique (trade_date, name)
)
comment '每日数据';

create index idx_future_daily_name
	on future_daily (name);

create table future_monitor_log
(
	id bigint auto_increment comment 'id'
		primary key,
	sno varchar(16) not null comment 'serial no.',
	code varchar(8) not null comment 'code',
	name varchar(20) not null comment 'contract name',
	type varchar(10) not null comment 'log type',
	content varchar(64) not null comment 'log contents',
	price decimal(10,2) not null comment 'logged current price',
	pct_change decimal(10,2) not null comment 'logged percentage change',
	position int not null comment 'relative position',
	position_lvl tinyint not null comment '[0,33]=1,[33,66]=2,[66,100]=3',
	`option` tinyint not null comment '1=call 2=put',
	suggest_price decimal(10,2) not null comment 'suggest price',
	log_time datetime not null comment 'log time',
	remark varchar(32) null comment 'remark contents',
	constraint uidx_future_monitor_log_code
		unique (code),
	constraint uidx_future_monitor_log_sno
		unique (sno)
)
comment '监控日志';

