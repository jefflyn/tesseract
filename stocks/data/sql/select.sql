-- 条件查询 selection data
select * from select_result_all where code='300210';
select * from select_result_all where name like '%动力%';
select * from select_result_all where code in ('000587','600929','300555', '000862');
select * from select_result_all where concepts like '%区块链%' order by wave_a;
select * from select_result_all where list_date > 20190224;
-- 1、超跌机会，不含次新（低风险、适合长线）
select *
from select_result_all
where 1 = 1
  and list_date < 20190202
  and name not like '%ST%'
  and pe > 0
#   and pe_ttm > 0
  and (wave_a < -50 and wave_b < 15 or wave_b <= -50)
  and count > 0
order by wave_a;

-- 2、超跌活跃，不含次新（中风险，适合中短线）
select *
from select_result_all
where 1 = 1
  and list_date < 20190202
  and name not like '%ST%'
  and pe > 0
  and (wave_a < -40 and wave_b < 15 or wave_b <= -40)
  and count >= 8
order by wave_a;

-- 3、两月内至少连续涨停2次（高风险，适合超短线）
select *
from select_result_all
where 1 = 1
#     and list_date < 20190202
  and code in (select code from limit_up_stat where fire_date > '2020-01-01' and combo > 1)
  and pe > 0
  and (wave_b < -33 or (wave_b > 0 and wave_b < 20) or (wave_a < -40 and wave_b < 30))
order by wave_a;

-- 4、指定交易日涨停
select *
from select_result_all
where 1=1
    and code in (select code from limit_up_stat where late_date = '2020-03-03')
    and (wave_b < -33 or (wave_b > 0 and wave_b < 20) or (wave_a < -40 and wave_b < 30))
order by wave_a;

-- 5、跌落涨停价下方的
select *
from limit_up_stat
where 1=1
    and price <= fire_price * 1.05
    and combo > 1
    and fire_date >= '2020-02-01'
order by wave_a;



