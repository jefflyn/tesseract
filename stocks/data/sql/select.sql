-- 条件查询 selection data
select * from select_result_all where code='300210';
select * from select_result_all where name like '%银星%';
select * from select_result_all where code in ('000587','600929','300555', '000862');
select * from select_result_all where concepts like '%黄金%' and pe > 0 order by wave_a;
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
where list_date < 20190202 and
      code in (select code from limit_up_stat where trade_date > '2020-01-01' group by code having max(combo_times) >= 2)
#   and (pe > 0 and pe_ttm > 0 or pe_ttm = 0)
and (wave_b < -33 or (wave_b > 0 and wave_b < 20) or (wave_a < -50 and wave_b < 30))
order by wave_b;


-- 多头排列趋势
select *
from select_result_all
where name not like '%ST%'
  and list_date < 20190101
  and (wave_a < -33 and wave_b < 15 or wave_b <= -33)
  and map > 9
#   and pe > 0 and pe_ttm > 0
#   and count > 0
order by wave_a;



