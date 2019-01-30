create table if not exists basics
(
  ts_code     varchar(10)  not null
  comment 'TS代码'
    primary key,
  code        varchar(6)   null
  comment '股票代码',
  name        varchar(8)   null
  comment '股票名称',
  area        varchar(10)  null
  comment '所在地域',
  industry    varchar(10)  null
  comment '所属行业',
  fullname    varchar(30)  null
  comment '股票全称',
  enname      varchar(100) null
  comment '英文全称',
  market      varchar(10)  null
  comment '市场类型 （主板/中小板/创业板）',
  exchange    varchar(8)   null
  comment '交易所代码',
  curr_type   varchar(3)   null
  comment '交易货币',
  list_status varchar(1)   null
  comment '上市状态： L上市 D退市 P暂停上市',
  list_date   int(10)      null
  comment '上市日期',
  delist_date varchar(10)  null
  comment '退市日期',
  is_hs       varchar(1)   null
  comment '是否沪深港通标的，N否 H沪股通 S深股通',
  constraint ix_symbol
  unique (code)
)
  comment '基础信息数据';

create index ix_list_date
  on basics (list_date);
----------------------------------------------
create table if not exists hist_index_day
(
  trade_date varchar(10) default '' not null
  comment '交易日',
  ts_code    varchar(10) default '' not null
  comment 'ts code',
  pre_close  decimal(10, 4)         null
  comment '上一个交易日收盘价',
  open       decimal(10, 4)         null
  comment '开盘价',
  close      decimal(10, 4)         null
  comment '收盘价',
  high       decimal(10, 4)         null
  comment '最高价',
  low        decimal(10, 4)         null
  comment '最低价',
  vol        int                    null
  comment '交易量（手）',
  amount     decimal(15, 4)         null
  comment '交易额（千）',
  amt_change decimal(10, 4)         null
  comment '涨跌额',
  pct_change decimal(10, 4)         null
  comment '涨跌幅',
  primary key (trade_date, ts_code)
)
  comment '每日指数数据';

create index ix_pct_change
  on hist_index_day (pct_change);

create index ix_ts_code
  on hist_index_day (ts_code);
------------------------------------------------
create table if not exists hist_trade_day
(
  trade_date varchar(10) default '' not null
  comment '交易日',
  ts_code    varchar(10) default '' not null
  comment 'ts code',
  pre_close  decimal(10, 2)         null
  comment '上一个交易日收盘价',
  open       decimal(10, 2)         null
  comment '开盘价',
  close      decimal(10, 2)         null
  comment '收盘价',
  high       decimal(10, 2)         null
  comment '最高价',
  low        decimal(10, 2)         null
  comment '最低价',
  vol        int(9)                 null
  comment '交易量（手）',
  amount     decimal(15, 4)         null
  comment '交易额（千）',
  amt_change decimal(10, 2)         null
  comment '涨跌额',
  pct_change decimal(10, 4)         null
  comment '涨跌幅',
  primary key (trade_date, ts_code)
)
  comment '每日交易数据（前复权）';

create index ix_pct_change
  on hist_trade_day (pct_change);

create index ix_ts_code
  on hist_trade_day (ts_code);

------------------------------------------