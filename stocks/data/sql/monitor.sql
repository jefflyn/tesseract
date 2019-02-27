select l.*, i.hz, i.sz50, i.scz, i.zxb, i.cyb
from
(select trade_date, count(case when pct_change > 0 then 1 else null end) as limitup,
       count(case when pct_change < 0 then 1 else null end) as limitdown
from hist_trade_day
where trade_date >= '2018-01-01' and (close = round(pre_close * 1.1, 2) or close = round(pre_close * 0.9, 2))
group by trade_date) as l
left join
    (select trade_date,
       sum(case ts_code when '000001.SH' then pct_change else 0 end) 'hz',
       sum(case ts_code when '000016.SH' then pct_change else 0 end) 'sz50',
       sum(case ts_code when '399001.SZ' then pct_change else 0 end) 'scz',
       sum(case ts_code when '399005.SZ' then pct_change else 0 end) 'zxb',
       sum(case ts_code when '399006.SZ' then pct_change else 0 end) 'cyb'
      from hist_index_day where trade_date >= '2018-01-01' group by trade_date) as i
on l.trade_date = i.trade_date
order by l.trade_date desc;