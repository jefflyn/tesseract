select l.*, i.hz, i.sz50, i.scz, i.zxb, i.cyb
from
(select trade_date, count(case when close >= round(pre_close * 1.1, 2) then 1 else null end) as limitup,
       count(case when close <= round(pre_close * 0.9, 2) then 1 else null end) as limitdown,
       count(case when pct_change > 0 then 1 else null end) as up,
       count(case when pct_change = 0 then 1 else null end) as flat,
       count(case when pct_change < 0 then 1 else null end) as down
from hist_trade_day
where trade_date >= '2019-01-01'
group by trade_date) as l
left join
    (select trade_date,
       sum(case ts_code when '000001.SH' then pct_change else 0 end) 'hz',
       sum(case ts_code when '000016.SH' then pct_change else 0 end) 'sz50',
       sum(case ts_code when '399001.SZ' then pct_change else 0 end) 'scz',
       sum(case ts_code when '399005.SZ' then pct_change else 0 end) 'zxb',
       sum(case ts_code when '399006.SZ' then pct_change else 0 end) 'cyb'
      from hist_index_day where trade_date >= '2019-01-01' group by trade_date) as i
on l.trade_date = i.trade_date
order by l.trade_date desc;