create table basic_a
(
    code          varchar(8) not null comment '代码'
        primary key,
    name          varchar(8) not null comment '名称',
    industry      varchar(8) not null comment '行业',
    list_date     varchar(8) not null comment '上市日期',
    total_capital bigint     null comment '总市值',
    flow_capital  bigint     null comment '流通市值',
    total_equity  bigint     null comment '总股本',
    flow_equity   bigint     null comment '流通股',
    update_time   timestamp  not null on update CURRENT_TIMESTAMP
)
    comment '基础信息';

create table basic_hk
(
    序号   bigint null,
    代码   text   null,
    名称   text   null,
    最新价 double null,
    涨跌额 double null,
    涨跌幅 double null,
    今开   double null,
    最高   double null,
    最低   double null,
    昨收   double null,
    成交量 double null,
    成交额 double null,
    time   text   null
);

create table basic_hk_sn
(
    symbol        text null,
    name          text null,
    engname       text null,
    tradetype     text null,
    lasttrade     text null,
    prevclose     text null,
    open          text null,
    high          text null,
    low           text null,
    volume        text null,
    amount        text null,
    ticktime      text null,
    buy           text null,
    sell          text null,
    pricechange   text null,
    changepercent text null
);

create table basic_us
(
    ts_code     text null,
    name        text null,
    enname      text null,
    classify    text null,
    list_status text null,
    list_date   text null,
    delist_date text null
);

create table basic_us_cn
(
    id       bigint auto_increment
        primary key,
    code     varchar(16)       not null,
    name     varchar(128)      null,
    selected tinyint default 0 not null,
    constraint basic_us_cn_code_uindex
        unique (code)
)
    comment '中概';

create table basic_us_selected
(
    id       bigint auto_increment
        primary key,
    code     varchar(16)       not null,
    name     varchar(128)      null,
    selected tinyint default 0 not null,
    constraint basic_us_selected_code_uindex
        unique (code)
)
    comment '精选';

create table gap_track
(
    code          varchar(16)    not null,
    gap_date      varchar(10)    null,
    direct        varchar(4)     not null,
    gap_from      decimal(10, 2) not null,
    gap_to        decimal(10, 2) not null,
    gap_size      decimal(10, 2) null,
    closed        int default 0  not null,
    closed_date   varchar(10)    null,
    days          int            null,
    curt_price    decimal(10, 2) null,
    curt_gap_size decimal(10, 2) null,
    constraint gap_track_code_gap_date_uindex
        unique (code, gap_date)
)
    comment 'gap track';

create table realtime_list_a
(
    序号           bigint null,
    代码           text   null,
    名称           text   null,
    最新价         double null,
    涨跌幅         double null,
    涨跌额         double null,
    成交量         double null,
    成交额         double null,
    振幅           double null,
    最高           double null,
    最低           double null,
    今开           double null,
    昨收           double null,
    量比           double null,
    换手率         double null,
    `市盈率-动态`  double null,
    市净率         double null,
    总市值         double null,
    流通市值       double null,
    涨速           double null,
    `5分钟涨跌`    double null,
    `60日涨跌幅`   double null,
    年初至今涨跌幅 double null
);

create table stock_a_daily
(
    日期   date   null,
    开盘   double null,
    收盘   double null,
    最高   double null,
    最低   double null,
    成交量 bigint null,
    成交额 double null,
    振幅   double null,
    涨跌幅 double null,
    涨跌额 double null,
    换手率 double null
);

create table trade_daily_us
(
    code   varchar(20) null,
    date   varchar(12) not null,
    open   double      null,
    high   double      null,
    low    double      null,
    close  double      null,
    volume double      null
);

create index trade_daily_us_code_index
    on trade_daily_us (code);

create table users
(
    id    int auto_increment
        primary key,
    name  varchar(255) null,
    email varchar(255) null
);

create table wave
(
    code        text     null,
    start       text     null,
    end         text     null,
    a           double   null,
    b           double   null,
    c           double   null,
    d           double   null,
    ap          double   null,
    bp          double   null,
    cp          double   null,
    dp          double   null,
    p           double   null,
    update_time datetime null
);

create table wave_cn
(
    code        text     null,
    start       text     null,
    end         text     null,
    a           double   null,
    b           double   null,
    c           double   null,
    d           double   null,
    ap          double   null,
    bp          double   null,
    cp          double   null,
    dp          double   null,
    p           double   null,
    update_time datetime null
);

create table wave_detail
(
    code        text   null,
    begin       text   null,
    end         text   null,
    status      text   null,
    begin_price double null,
    end_price   double null,
    `change`    double null,
    days        bigint null
);

create table wave_detail_cn
(
    code        text   null,
    begin       text   null,
    end         text   null,
    status      text   null,
    begin_price double null,
    end_price   double null,
    `change`    double null,
    days        bigint null
);

