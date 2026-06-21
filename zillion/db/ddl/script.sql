create table future.basic
(
    symbol      varchar(4)                 not null comment '商品代号'
        primary key,
    name        varchar(16)                not null comment '商品名',
    type        varchar(8)    default ''   not null comment '分类',
    amount      int           default 0    not null comment '合同每单位数量',
    unit        varchar(4)    default ''   not null comment '单位',
    step        decimal(6, 2) default 0.00 not null comment '每跳点数',
    profit      int           default 0    not null comment '每跳毛利',
    exchange    varchar(16)   default ''   not null comment '所属交易所',
    night       tinyint       default 1   not null comment '是否夜盘（0=否 1=是）',
    deleted     tinyint       default 0    not null
) comment 'F12基本信息';

create table future.contract
(
    symbol      varchar(4)        not null comment '商品代码',
    code        varchar(8)        not null comment '合约代码'
        primary key,
    main        tinyint default 0 not null comment '主力=1',
    `limit`     int               null comment 'limit up/down',
    low         decimal(10, 2)    not null comment '合约最低',
    high        decimal(10, 2)    not null comment '合约最高',
    low_time    varchar(20)       null comment '新低时间',
    high_time   varchar(20)       null comment '新低时间',
    h_low       decimal(10, 2)    null comment 'hist low',
    h_high      decimal(10, 2)    null comment 'hist high',
    h_low_time  varchar(20)       null,
    h_high_time varchar(20)       null,
    create_time datetime          not null comment '创建时间',
    update_time datetime          not null on update CURRENT_TIMESTAMP comment '更新时间',
    deleted     tinyint default 0 not null,
    constraint uidx_contract_symbol_code
        unique (symbol, code),
)
    comment '合约信息';

create table future.trade_daily
(
    id            bigint auto_increment comment '主键id'
        primary key,
    symbol        varchar(6)     not null comment '商品代码',
    trade_date    varchar(10)    not null comment '交易日期',
    code          varchar(10)    null comment '合约代码',
    open          decimal(10, 2) null comment '开盘价',
    high          decimal(10, 2) null comment '最高价',
    low           decimal(10, 2) null comment '最低价',
    close         decimal(10, 2) null comment '收盘价',
    settle        decimal(10, 2) null comment '结算价',
    pre_close     decimal(10, 2) null comment '昨收盘价',
    pre_settle    decimal(10, 2) null comment '昨结算价',
    close_change  decimal(10, 2) null comment '昨收盘价涨跌幅',
    settle_change decimal(10, 2) null comment '结算价涨跌幅',
    deal_vol      int            null comment '交易量',
    hold_vol      int            null comment '持仓量',
    create_time   datetime       not null comment '创建时间',
    constraint uidx_future_daily_trade_date_contract_code
        unique (trade_date, code)
)
    comment '每日行情';

create index idx_future_daily_code
    on future.trade_daily (symbol);

create index idx_future_daily_code_date
    on future.trade_daily (code, trade_date);

CREATE TABLE "gap_tactics"
(
    symbol      varchar(4)                not null,
    name        varchar(16)               not null,
    change      decimal(6, 2) default 0.5 not null,
    up_tactic   varchar(16),
    down_tactic varchar(16),
    gap_type    varchar(16),
    industry    varchar(8),
    action      varchar(32)
, top10 integer default 0 not null)



