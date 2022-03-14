create table stocks.basics
(
	trade_date varchar(10) not null comment '交易日',
	code varchar(6) not null comment '股票代码'
		primary key,
	ts_code varchar(10) not null comment '股票ts代码',
	name varchar(8) not null comment '股票名称',
	industry varchar(10) null comment '行业',
	area varchar(8) null comment '地区',
	pe decimal(10,2) null comment '动态市盈率',
	circulate_shares decimal(10,2) null comment '流通股本',
	total_shares decimal(10,2) null comment '总股本(万)',
	total_assets decimal(10,2) null comment '总资产(万)',
	liquid_assets decimal(10,2) null comment '流动资产(万)',
	fixed_assets decimal(10,2) null comment '固定资产(万)',
	reserved decimal(10,2) null comment '公积金',
	reserved_per_share decimal(10,2) null comment '每股公积金(元)',
	esp decimal(10,4) null comment '每股收益(元)',
	bvps decimal(10,2) null comment '每股净资产(元)',
	bp decimal(10,2) null comment '市净率',
	list_date int(8) null comment '上市日期',
	undp decimal(10,2) null comment '未分配利润',
	undp_per_share decimal(10,2) null comment '每股未分配利润(元)',
	revenue decimal(10,2) null comment '营业总收入(亿)',
	profit decimal(10,2) null comment '利润(亿)',
	gpr decimal(10,2) null comment '毛利率(%)',
	npr decimal(10,2) null comment '资产净利率(%)',
	holders int(10) null comment '股东人数'
)
comment '上市公司基本情况';

