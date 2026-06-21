# Role

你是一名资深全栈工程师，擅长使用现代技术栈快速构建最小可行产品（MVP）。

# Task

帮我开发一个【期货领域】的 MVP，核心功能是【数据定期抓取、数据分析和邮件通知】。

1、功能模块1：独立运行，一次性获取商品信息

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
`limit`     int           default -1   not null comment 'limit up/down',
exchange    varchar(16)   default ''   not null comment '所属交易所',
night       tinyint       default -1   not null comment '是否夜盘（0=否 1=是）',
deleted     tinyint       default 0    not null,
update_time timestamp                  not null on update CURRENT_TIMESTAMP comment '更新时间'
)
comment '基本信息';

2、功能二：获取当前所有主力合约信息，一次性获取作为基础数据，字段包含

create table future.contract
(
symbol      varchar(4)        not null comment '商品代码',
code        varchar(8)        not null comment '合约代码'
primary key,
ts_code     varchar(12)       not null comment 'ts code',
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
selected    tinyint default 0 not null comment '0=否 1=是',
create_time datetime          not null comment '创建时间',
update_time datetime          not null on update CURRENT_TIMESTAMP comment '更新时间',
deleted     tinyint default 0 not null,
constraint uidx_contract_symbol_code
unique (symbol, code),
constraint uidx_contract_symbol_ts_code
unique (symbol, ts_code)
)
comment '合约信息';

create index idx_contract_selected
on future.contract (selected);


3、独立功能：一次性获取主力合约的历史日k数据，每天工作日下午4点定时增量更新日k数据


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

# Tech Stack

- 前端：Vue3 + ElementPlus
- 后端：python + akshare + sqlite
- 部署：本地运行

# Constraints

1. 代码简洁易运行，避免复杂依赖，提供完整的环境配置步骤（npm 指令/启动脚本）。
2. 实现核心流程即可，忽略边缘场景（如：密码加密可先用简单哈希，后续再优化）。
3. 自带基础的错误提示，无需复杂的异常处理。

# Deliverables

1. 完整的项目代码结构。
2. 启动步骤说明。
3. 核心功能测试方法。
4. 下一步优化建议。
