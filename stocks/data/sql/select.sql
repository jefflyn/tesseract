select * from select_result_all where code='300210';
select * from select_result_all where name like '%风范%';

-- check
select uld.trade_date,uld.combo_times as cc, sra.* from select_result_all sra
    join limit_up_stat uld on sra.code = uld.code
where uld.trade_date='2020-02-07'
order by sra.wave_a;
select * from select_result_all where concepts like '%军工%' and (wave_a < -50 and wave_b < 15 or wave_b <= -50);
select * from select_result_all where code in ('000587','600929','300555', '000862');
select * from hist_ma_day where code in ('000587','600929','300555','000862');
# 条件查询 selection data
select *
from select_result_all
where 1 = 1
  and name not like '%ST%'
#   and code in ('300099')
# and call_diff = ''
  and last_f_date <> ''
#     and call_diff
# and industry like '%证券%'
# and list_date < 20190101
  and pe_ttm is not null
# and name like '%三川%'
# and c.concepts like '%油%'
# and area like '%甘肃%'
# and count > 0
  and (wave_a <= -33 and wave_b < 15 or wave_b <= -33)
# and code in (select code from my_stock_pool where platform in ('cf')) -- self position
# and code in (select code from hist_trade_day where trade_date>='2019-09-01' and trade_date<='2019-12-31' and pct_change>9.9-- and high=low
#     group by code
#     having count(1) > 3) -- 时间区间的一字
order by last_f_date desc, count desc, wave_a;

-- 1、超跌选股，不含次新股（低风险，长线投资）
select *
from select_result_all
where 1=1
  and list_date < 20190101
  and pe > 0 and pe_ttm > 0
  and (wave_a < -50 and wave_b < 15 or wave_b <= -50)
  and count between 1 and 7
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

-- 2.1
select *
from select_result_all
where list_date < 20190201
  and last_f_date <> ''
  and pe > 0
  and call_diff between -10 and 10
  and count > 3
  and count_ >= 2
order by last_f_date desc, call_diff, count desc;

-- 3、本月涨停选股，不含次新股（高风险，适合超短线）
select *
from select_result_all
where code in
      (select code from hist_trade_day where pct_change > 9.8 and code not like '688%' and trade_date >= '2019-08-01')
  and c30d > 2
  and list_date < 20190101
  and pe > 0
order by wave_a;

select * from select_result_all where name like '%ST%' order by wave_a;
select * from select_result_all where list_date > 20190114;

-- nice
select *
from select_result_all
where name not like '%ST%'
  and list_date < 20190101
  and (wave_a < -33 and wave_b < 15)
  and map >= 8
  and pe > 0 and pe_ttm > 0
#   and count > 0
order by wave_a;

select * from hist_ma_day where code='600929';

select *
from select_result_all
where code in (select code from select_wave_all where `change` <=-80);

select * from select_wave_all where code in (select code
from select_result_all
where name like '%ST%' or code='000587')


