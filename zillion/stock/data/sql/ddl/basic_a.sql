CREATE TABLE `basic_a` (
  `code` varchar(8) NOT NULL COMMENT '代码',
  `name` varchar(8) NOT NULL COMMENT '名称',
  `industry` varchar(8) NOT NULL COMMENT '行业',
  `list_date` varchar(8) NOT NULL COMMENT '上市日期',
  `total_equity` bigint DEFAULT NULL COMMENT '总股本',
  `flow_equity` bigint DEFAULT NULL COMMENT '流通股',
  `total_cap` bigint DEFAULT NULL COMMENT '总市值',
  `flow_cap` bigint DEFAULT NULL COMMENT '流通市值',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='基础信息'

