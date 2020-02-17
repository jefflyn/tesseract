create table stocks.my_stock_pool
(
	code varchar(6) not null,
	platform varchar(10) null,
	share int default 100 not null,
	cost decimal(10,3) null,
	bottom decimal(10,2) null,
	is_hold tinyint default 1 null,
	grade varchar(3) default 'c' null,
	hold_date date null,
	close_date date null,
	remark varchar(255) null,
	alias varchar(4) null,
	concept varchar(20) null,
	constraint my_stock_pool_pk
		unique (code, platform)
);

INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000862', 'cf', 100, null, 4.91, 1, 'b', '2019-12-10', null, '-5500', '银星', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002555', 'cf', 100, null, 11.66, 1, 'c', null, null, '-19300', '三七', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('603881', 'cf', 100, null, 28.78, 1, 'b', null, null, '-2100', '数据港', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('601890', 'cf', 100, null, 5.36, 1, 'c', null, null, '-7400', '锚链', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002703', 'cf', 100, null, 4.96, 1, 'a', null, null, '-19800', '世宝', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002561', 'cf', 100, null, 7.96, 1, 'c', null, null, '-9600', '徐家汇', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600197', 'cf', 100, null, 14.51, 1, 'c', null, null, '-2600', '伊力特', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600958', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600570', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002468', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000709', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('601216', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000630', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600909', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('603885', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002340', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('601326', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000062', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000519', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000672', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600908', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002678', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002697', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('603323', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000019', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002488', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('603766', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('603113', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600831', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('601890', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002115', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000524', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000885', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600069', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002158', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000922', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000906', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600468', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002485', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000993', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002813', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000678', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002114', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600505', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000635', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600281', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002620', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000909', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000721', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000663', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000018', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600821', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600275', 'pa', 100, null, null, 1, 'c', null, null, null, null, null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('601700', 'df', 100, null, null, 1, 'c', null, null, null, '风范', null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('300210', 'cf', 100, 40.100, 9.00, 1, 'c', null, null, null, '森远', '');
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('000587', 'cf', 45400, 2.181, 1.58, 1, 'a', null, null, null, '慈航', null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('600929', 'df', 5700, 6.310, 5.00, 1, 'c', null, null, null, '湖盐', null);
INSERT INTO stocks.my_stock_pool (code, platform, share, cost, bottom, is_hold, grade, hold_date, close_date, remark, alias, concept) VALUES ('002167', 'df', 4200, 5.992, null, 1, 'c', null, null, null, '锆业', null);