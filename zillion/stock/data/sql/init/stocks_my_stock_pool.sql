CREATE TABLE `basic_a` (
  `code` varchar(8) NOT NULL COMMENT '代码',
  `name` varchar(8) NOT NULL COMMENT '名称',
  `industry` varchar(8) NOT NULL COMMENT '行业',
  `list_date` varchar(8) NOT NULL COMMENT '上市日期',
  `total_equity` bigint DEFAULT NULL COMMENT '总股本',
  `flow_equity` bigint DEFAULT NULL COMMENT '流通股',
  `total_capital` bigint DEFAULT NULL COMMENT '总市值',
  `flow_capital` bigint DEFAULT NULL COMMENT '流通市值',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='基础信息'

CREATE TABLE `basic_us` (
  `name` text COLLATE utf8mb3_unicode_ci,
  `cname` text COLLATE utf8mb3_unicode_ci,
  `category` text COLLATE utf8mb3_unicode_ci,
  `symbol` text COLLATE utf8mb3_unicode_ci,
  `price` text COLLATE utf8mb3_unicode_ci,
  `diff` text COLLATE utf8mb3_unicode_ci,
  `chg` text COLLATE utf8mb3_unicode_ci,
  `preclose` text COLLATE utf8mb3_unicode_ci,
  `open` text COLLATE utf8mb3_unicode_ci,
  `high` text COLLATE utf8mb3_unicode_ci,
  `low` text COLLATE utf8mb3_unicode_ci,
  `amplitude` text COLLATE utf8mb3_unicode_ci,
  `volume` text COLLATE utf8mb3_unicode_ci,
  `mktcap` text COLLATE utf8mb3_unicode_ci,
  `pe` text COLLATE utf8mb3_unicode_ci,
  `market` text COLLATE utf8mb3_unicode_ci,
  `category_id` text COLLATE utf8mb3_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `basic_us_selected` (
  `name` varchar(256) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cname` varchar(32) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `category` varchar(16) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `symbol` varchar(16) COLLATE utf8mb3_unicode_ci NOT NULL,
  `market` varchar(16) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `tag` varchar(128) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `daily_quote_a` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` varchar(16) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `code` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `open` decimal(10,2) DEFAULT NULL,
  `close` decimal(10,2) DEFAULT NULL,
  `high` decimal(10,2) DEFAULT NULL,
  `low` decimal(10,2) DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `turnover` bigint DEFAULT NULL,
  `amplitude` decimal(10,2) DEFAULT NULL,
  `change_percent` decimal(10,2) DEFAULT NULL,
  `change_amt` decimal(10,2) DEFAULT NULL,
  `turnover_rate` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hist_daily_quote_code_date_index` (`code`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `daily_quote_us` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT '合约代码',
  `date` varchar(10) COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '交易日期',
  `open` decimal(10,2) DEFAULT NULL COMMENT '开盘价',
  `high` decimal(10,2) DEFAULT NULL COMMENT '最高价',
  `low` decimal(10,2) DEFAULT NULL COMMENT '最低价',
  `close` decimal(10,2) DEFAULT NULL COMMENT '收盘价',
  `volume` int DEFAULT NULL COMMENT '交易量',
  PRIMARY KEY (`id`),
  KEY `idx_trade_daily_us` (`code`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci COMMENT='每日行情'

CREATE TABLE `gap_track` (
  `code` varchar(16) COLLATE utf8mb3_unicode_ci NOT NULL,
  `gap_date` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `direct` varchar(4) COLLATE utf8mb3_unicode_ci NOT NULL,
  `gap_from` decimal(10,2) NOT NULL,
  `gap_to` decimal(10,2) NOT NULL,
  `gap_size` decimal(10,2) DEFAULT NULL,
  `closed` int NOT NULL DEFAULT '0',
  `closed_date` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `days` int DEFAULT NULL,
  `curt_price` decimal(10,2) DEFAULT NULL,
  `curt_gap_size` decimal(10,2) DEFAULT NULL,
  UNIQUE KEY `gap_track_code_gap_date_uindex` (`code`,`gap_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci COMMENT='gap track'

CREATE TABLE `realtime_list_a` (
  `序号` bigint DEFAULT NULL,
  `代码` text COLLATE utf8mb3_unicode_ci,
  `名称` text COLLATE utf8mb3_unicode_ci,
  `最新价` double DEFAULT NULL,
  `涨跌幅` double DEFAULT NULL,
  `涨跌额` double DEFAULT NULL,
  `成交量` double DEFAULT NULL,
  `成交额` double DEFAULT NULL,
  `振幅` double DEFAULT NULL,
  `最高` double DEFAULT NULL,
  `最低` double DEFAULT NULL,
  `今开` double DEFAULT NULL,
  `昨收` double DEFAULT NULL,
  `量比` double DEFAULT NULL,
  `换手率` double DEFAULT NULL,
  `市盈率-动态` double DEFAULT NULL,
  `市净率` double DEFAULT NULL,
  `总市值` double DEFAULT NULL,
  `流通市值` double DEFAULT NULL,
  `涨速` double DEFAULT NULL,
  `5分钟涨跌` double DEFAULT NULL,
  `60日涨跌幅` double DEFAULT NULL,
  `年初至今涨跌幅` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `wave` (
  `code` text COLLATE utf8mb3_unicode_ci,
  `start` text COLLATE utf8mb3_unicode_ci,
  `end` text COLLATE utf8mb3_unicode_ci,
  `a` double DEFAULT NULL,
  `b` double DEFAULT NULL,
  `c` double DEFAULT NULL,
  `d` double DEFAULT NULL,
  `ap` double DEFAULT NULL,
  `bp` double DEFAULT NULL,
  `cp` double DEFAULT NULL,
  `dp` double DEFAULT NULL,
  `p` double DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `wave_baba` (
  `code` text COLLATE utf8mb3_unicode_ci,
  `start` text COLLATE utf8mb3_unicode_ci,
  `end` text COLLATE utf8mb3_unicode_ci,
  `a` double DEFAULT NULL,
  `b` double DEFAULT NULL,
  `c` double DEFAULT NULL,
  `d` double DEFAULT NULL,
  `ap` double DEFAULT NULL,
  `bp` double DEFAULT NULL,
  `cp` double DEFAULT NULL,
  `dp` double DEFAULT NULL,
  `p` double DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `wave_detail` (
  `code` text COLLATE utf8mb3_unicode_ci,
  `begin` text COLLATE utf8mb3_unicode_ci,
  `end` text COLLATE utf8mb3_unicode_ci,
  `status` text COLLATE utf8mb3_unicode_ci,
  `begin_price` double DEFAULT NULL,
  `end_price` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `days` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

CREATE TABLE `wave_detail_baba` (
  `code` text COLLATE utf8mb3_unicode_ci,
  `begin` text COLLATE utf8mb3_unicode_ci,
  `end` text COLLATE utf8mb3_unicode_ci,
  `status` text COLLATE utf8mb3_unicode_ci,
  `begin_price` double DEFAULT NULL,
  `end_price` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `days` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

