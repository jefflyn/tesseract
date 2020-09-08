drop table future_basics if exists ;

create table future_basics
(
	code varchar(6) not null comment '代码'
		primary key,
	name varchar(15) null comment '名称',
	symbol varchar(6) not null comment 'sina code',
	amount int not null comment '每手单位数',
	unit varchar(3) not null comment '单位',
	`limit` tinyint not null comment '涨跌幅限制%',
	margin_rate tinyint default 10 null comment '保证金率',
	goods_type varchar(6) not null comment ' 商品类型（1=能源化工,2=黑色金属,3=贵金属,4=有色金属,5=农产品,6=金融板块）',
	night tinyint default 0 null comment '是否支持夜盘（0=否，1=是）',
	exchange varchar(10) not null comment '所属交易所',
	on_target tinyint default 0 null comment '0=否 1=是',
	alert_price varchar(20) null comment '提醒价格',
	alert_change varchar(20) null comment '提醒涨跌幅',
	alert_on tinyint null comment '提醒设置（0=关，1=开）',
	alert_mobile varchar(18) null comment '接收提醒手机号'
)
comment 'future基本信息';

create index idx_future_basics_symbol
	on future_basics (symbol);

INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('AG', '白银', 'AG2012', 15, '千克', 8, 10, '贵金属', 1, '上海期货交易所', 1, '6700', '-9,-6,3,6,9,9.9', 1, '18507550586');
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('AL', '沪铝', 'AL0', 5, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('AP', '鲜苹果', 'AP2010', 10, '吨', 6, 8, '农产品', 0, '郑州商品交易所', 1, '7230', '-1,2', null, '18507550586');
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('AU', '黄金', 'AU2012', 1000, '克', 6, 8, '贵金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('BU', '沥青', 'BU0', 10, '吨', 8, 10, '能源化工', 0, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('CF', '棉花', 'CF0', 5, '吨', 6, 7, '农产品', 1, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('CU', '沪铜', 'CU0', 5, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('EB', '苯乙烯', 'EB0', 5, '吨', 11, 12, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('EG', '乙二醇', 'EG0', 10, '吨', 9, 11, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('FB', '纤维板', 'FB0', 10, '立方米', 5, 10, '能源化工', 0, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('FG', '玻璃', 'FG2101', 20, '吨', 7, 10, '能源化工', 1, '郑州商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('FU', '燃油', 'FU0', 10, '吨', 10, 12, '能源化工', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('HC', '热轧卷板', 'HC0', 10, '吨', 6, 8, '黑色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('I', '铁矿石', 'I0', 100, '吨', 10, 11, '黑色金属', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('IH', '上证50股指期货', 'IH0', 300, '指数点', 10, 10, '金融板块', 0, '中国金融期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('J', '焦炭', 'J0', 100, '吨', 8, 9, '黑色金属', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('JM', '焦煤', 'JM0', 60, '吨', 8, 9, '黑色金属', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('L', '塑料', 'L0', 5, '吨', 9, 11, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('LU', '低硫燃油', 'LU0', 10, '吨', 10, 12, '能源化工', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('MA', '郑醇（甲醇）', 'MA0', 10, '吨', 6, 10, '能源化工', 1, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('NI', '沪镍', 'NI0', 1, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('NR', '20号胶', 'NR0', 10, '吨', 6, 11, '能源化工', 0, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('OI', '菜油', 'OI2010', 10, '吨', 5, 6, '农产品', 1, '郑州商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('P', '棕榈', 'P2101', 10, '吨', 8, 9, '农产品', 1, '大连商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('PB', '沪铅', 'PB0', 5, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('PG', '液化石油气', 'PG0', 20, '吨', 10, 11, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('PP', 'PP(聚丙烯)', 'PP0', 5, '吨', 9, 11, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('RB', '螺纹钢', 'RB0', 10, '吨', 6, 8, '黑色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('RU', '橡胶', 'RU0', 10, '吨', 6, 8, '能源化工', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SA', '纯碱', 'SA2101', 20, '吨', 4, 5, '能源化工', 1, '郑州商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SC', '原油', 'SC0', 1000, '桶', 10, 12, '能源化工', 1, '上海国际能源交易中心', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SF', '硅铁', 'SF0', 5, '吨', 6, 7, '黑色金属', 0, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SM', '锰硅', 'SM0', 5, '吨', 6, 7, '黑色金属', 0, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SN', '沪锡', 'SN0', 1, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SP', '纸浆', 'SP0', 10, '吨', 5, 10, '能源化工', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('SS', '不锈钢', 'SS0', 5, '吨', 6, 8, '黑色金属', 1, '上海期货交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('TA', 'PTA(精对苯二甲酸)', 'TA0', 5, '吨', 5, 6, '能源化工', 1, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('UR', '尿素', 'UR2101', 20, '吨', 4, 5, '能源化工', 0, '郑州商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('V', 'PVC(聚氯乙烯)', 'V0', 5, '吨', 8, 9, '能源化工', 1, '大连商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('Y', '豆油', 'Y2101', 10, '吨', 7, 8, '农产品', 1, '大连商品交易所', 1, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('ZC', '动力煤', 'ZC2010', 100, '吨', 4, 5, '黑色金属', 1, '郑州商品交易所', 0, null, null, null, null);
INSERT INTO stocks.future_basics (code, name, symbol, amount, unit, `limit`, margin_rate, goods_type, night, exchange, on_target, alert_price, alert_change, alert_on, alert_mobile) VALUES ('ZN', '沪锌', 'ZN0', 5, '吨', 8, 10, '有色金属', 1, '上海期货交易所', 0, null, null, null, null);


