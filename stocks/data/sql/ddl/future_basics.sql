drop table future_basics if exists ;
create table future_basics
(
	code varchar(6) not null comment '代码'
		primary key,
	name varchar(10) null comment '名称',
	symbol varchar(6) not null comment 'sina code',
	amount int not null comment '每手单位数',
	unit varchar(3) not null comment '单位',
	`limit` tinyint not null comment '涨跌幅限制%',
	margin_rate tinyint default 10 null comment '保证金率',
	goods_type varchar(6) not null comment ' 商品类型（1=能源化工,2=黑色金属,3=贵金属,4=有色金属,5=农产品,6=金融板块）',
	night tinyint default 0 null comment '是否支持夜盘（0=否，1=是）',
	exchange varchar(10) not null comment '所属交易所',
	on_target tinyint default 0 null comment '0=否 1=是'
)
comment 'future基本信息';

create index idx_future_basics_symbol
	on future_basics (symbol);

-- data
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('AG', '白银', 'AG2012', 15, '千克', 8, null, '贵金属', 0, '上海期货交易所', 1);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('BU', '沥青', 'BU0', 10, '吨', 13, null, '能源化工', 0, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('CF', '棉花', 'CF0', 5, '吨', 6, null, '农产品', 1, '郑州商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('CU', '沪铜', 'CU0', 5, '吨', 8, null, '有色金属', 1, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('EB', '苯乙烯', 'EB0', 5, '吨', 11, null, '能源化工', 0, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('EG', '乙二醇', 'EG0', 10, '吨', 9, null, '能源化工', 0, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('FB', '纤维板', 'FB0', 10, '立方米', 5, null, '能源化工', 0, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('FG', '玻璃', 'FG2009', 20, '吨', 4, null, '能源化工', 0, '郑州商品交易所', 1);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('FU', '燃料油', 'FU0', 10, '吨', 13, null, '能源化工', 0, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('I', '铁矿石', 'I0', 100, '吨', 10, null, '黑色金属', 0, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('IH', '上证50股指期货', 'IH0', 300, '指数点', 10, null, '金融板块', 0, '中国金融期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('L', '塑料', 'L0', 5, '吨', 9, null, '能源化工', 1, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('LU', '低硫燃油', 'LU0', 10, '吨', 13, null, '能源化工', 1, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('MA', '郑醇', 'MA0', 10, '吨', 6, null, '能源化工', 1, '郑州商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('NR', '20号胶', 'NR0', 10, '吨', 9, null, '能源化工', 0, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('OI', '菜油', 'OI2009', 10, '吨', 5, null, '农产品', 1, '郑州商品交易所', 1);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('P', '棕榈油', 'P2009', 10, '吨', 8, null, '农产品', 1, '大连商品交易所', 1);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('PG', '液化石油气', 'PG0', 20, '吨', 10, null, '能源化工', 0, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('PP', '聚丙烯-PP', 'PP0', 5, '吨', 9, null, '能源化工', 1, '大连商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('RU', '橡胶', 'RU0', 10, '吨', 9, null, '能源化工', 1, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('SA', '纯碱', 'SA0', 20, '吨', 4, null, '能源化工', 1, '郑州商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('SC', '原油', 'SC0', 1000, '桶', 13, null, '能源化工', 0, '上海国际能源交易中心', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('SP', '纸浆', 'SP0', 10, '吨', 6, null, '能源化工', 1, '上海期货交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('TA', '精对苯二甲酸-PTA', 'TA0', 5, '吨', 7, null, '能源化工', 0, '郑州商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('UR', '尿素', 'UR0', 20, '吨', 4, null, '能源化工', 0, '郑州商品交易所', 0);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target) VALUES ('V', '聚氯乙烯-PVC', 'V0', 5, '吨', 8, null, '能源化工', 1, '大连商品交易所', 0);