select * from select_result_all where code='300210';
select * from select_result_all where name like '%轴承%';
select * from select_result_all where code in ('000587','600929','300555', '000862');
-- 条件查询 selection data
select *
from select_result_all
where 1 = 1
  and name not like '%ST%'
#   and code in ('300099')
# and call_diff = ''
#   and last_f_date <> ''
#     and call_diff
# and industry like '%证券%'
# and list_date < 20190101
#   and pe_ttm is not null
# and name like '%三川%'
and concepts like '%华为%'
# and area like '%甘肃%'
# and count > 0
#   and (wave_a <= -33 and wave_b < 15 or wave_b <= -33)
# and code in (select code from my_stock_pool where platform in ('cf')) -- self position
# and code in (select code from hist_trade_day where trade_date>='2019-09-01' and trade_date<='2019-12-31' and pct_change>9.9-- and high=low
#     group by code
#     having count(1) > 3) -- 时间区间的一字
order by wave_a;

-- 1、超跌选股，不含次新股（低风险，长线投资）
select *
from select_result_all
where 1=1
  and list_date < 20190101
  and pe > 0 and pe_ttm > 0
  and (wave_a < -50 and wave_b < 15 or wave_b <= -50)
#   and count between 1 and 7
order by wave_a;

-- 2、超跌活跃选股，不含次新股（中风险，适合中短线）
select *
from select_result_all
where 1 = 1
  and list_date < 20190101
  and pe > 0 and pe_ttm > 0
  and (wave_a < -40 and wave_b < 15 or wave_b <= -40)
  and count >= 8
order by wave_a;

-- 3、2020涨停选股（高风险，适合超短线）
select *
from select_result_all
where code in
      (select code from limit_up_stat where trade_date > '2020-01-01' group by code having max(combo_times) >= 2)
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

-- ST
select * from select_wave_all where code in (select code
from select_result_all
where name like '%ST%' or code='000587')

# 概念
select * from select_result_all where code in (select code from concepts where concepts like '%食品%')
and pe_ttm > 0
order by wave_a;
