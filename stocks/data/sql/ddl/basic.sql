create table stocks.basic
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
	on stocks.basic (code);

create index ix_list_date
	on stocks.basic (list_date);

