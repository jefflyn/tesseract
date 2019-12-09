# 条件查询 select data
select *
from select_result_all
where 1 = 1
and name not like '%ST%'
and last_f_date <> ''
#     and call_diff

# and industry like '%证券%'
# and list_date < 20190101
# and pe_ttm is not null
# and name like '%津劝业%'
# and c.concepts like '%油%'
# and area like '%甘肃%'
# and count > 0
# and wave_a < 0
# and wave_b < 15
# and code in (select code from my_stock_pool where platform in ('cf')) -- self position
# and code in (select code from hist_trade_day where trade_date>='2019-09-01' and trade_date<='2019-12-31' and pct_change>9.9-- and high=low
#     group by code
#     having count(1) > 3) -- 时间区间的一字
order by count desc, wave_a;

-- 1、超跌选股，包含次新股（低风险，长线投资）
select *
from select_result_all
where name not like '%ST%' -- and list_date < 20180901
  and pe_ttm is not null
  and abs(pe - pe_ttm) <= 10
#   and pe_ttm < pe -- 价值向上趋势
  and (wave_a < -40 and wave_b < 15 or wave_b <= -30)
  and count > 0 and count < 7
# and concepts like '%黄金%'
order by wave_a;

-- 2、超跌活跃选股，不含次新股（中风险，适合中短线）
select * from select_result_all
where name not like '%ST%'
and (pe_ttm is not null or pe is not null)
#  and pe_ttm < pe -- 价值向上趋势
and (wave_a < -40 and wave_b < 15 or wave_b <= -30)
and count >= 8
and list_date < 20190101
order by count desc, wave_a;

-- 2.1 连续3天涨停回调
select * from select_result_all
where name not like '%ST%'
    and call_diff < 0
    and (wave_a < 15 and wave_b < 15 or wave_b <= -30)
    and pe_ttm is not null
#     and pe is not null
#   and pe_ttm < pe -- 价值向上趋势
    and list_date < 20181215
order by last_f_date desc, call_diff, count desc;

-- 3、本月涨停选股，不含次新股（高风险，适合超短线）
select *
from select_result_all
where code in (select code from hist_trade_day where pct_change > 9.8 and code not like '688%' and trade_date >= '2019-08-01')
and c30d > 2
and list_date < 20190101
and pe_ttm is not null
order by wave_a;

# 缺口选股
select * from daily_gap_trace_a where s_date='2019-06-21' order by position;
select * from daily_gap_trace_b where s_date='2019-06-18' order by s_date desc;

update daily_gap_trace_a g inner join hist_trade_day h on g.v_date=h.trade_date and g.code=h.code
set g.o_profit=(h.close-h.open)/h.open*100, g.l_profit=(h.close-h.low)/h.low*100;

update daily_gap_trace_b g inner join hist_trade_day h on g.v_date=h.trade_date and g.code=h.code
set g.o_profit=(h.close-h.open)/h.open*100, g.l_profit=(h.close-h.low)/h.low*100;

# delete from daily_gap_trace_a where s_date='2019-06-19';
-- 插入向上跳空缺口，并且当天涨幅大于9%
  insert into daily_gap_trace_a (s_date, v_date, code, name, industry, cost, bottom, share, b_up, position, gap, g_space, c30d, vol, uds)
select trade_date, '2019-06-25', code, name, industry, price, bottom, 100, `uspace%`, `position%`, gap, gap_space, c30d, vol_rate, updays
  from select_result_all
where list_date < 20190101 and name not like '%ST%' and pct > 9.9;

  insert into daily_gap_trace_b (s_date, v_date, code, name, industry, cost, bottom, share, b_up, position, gap, g_space, c30d, vol, uds)
select trade_date, '2019-06-22', code, name, industry, price, bottom, 100, `uspace%`, `position%`, gap, gap_space, c30d, vol_rate, updays
  from select_result_all
where list_date < 20190101 and name not like '%ST%' and pct > 9.9 and `position%` >= 40;
