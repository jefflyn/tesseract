-- index data
select * from hist_index_day where trade_date >= '2020-02-03' order by trade_date desc;
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '000001.SH', '000001', 2.28, now());
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '399001.SZ', '399001', 2.98, now());
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '399006.SZ', '399006', 3.72, now());

-- get_day_all获取不到数据，手动补充涨停数据，combo_times默认值1，
insert into limit_up_stat(trade_date, code, name, industry, area, combo_times, pe, wave_a, wave_b, turnover_rate, vol_rate, open_change)
select hist.trade_date, hist.code, s.name, s.industry, s.area, 1 combo, s.pe,
       ifnull(s.wave_a,0), ifnull(s.wave_b,0), a.turnover, round(a.volratio,2) volratio, round((hist.open-hist.pre_close)/hist.pre_close * 100,2) open_change
from hist_trade_day hist
left join select_result_all s on hist.code=s.code left join today_all a on hist.code = a.code
where hist.trade_date='2020-02-28' and (hist.close = round(hist.pre_close * 1.1, 2) or hist.pct_change >= 9.9);

delete from limit_up_daily where trade_date='2020-02-28';

-- 每天涨停数统计
select trade_date, count(1) from limit_up_daily group by trade_date order by trade_date desc;
select code, name, min(trade_date), max(trade_date), max(combo), count(1) from limit_up_daily group by code, name;

-- 更新基本信息
update limit_up_daily l inner join basics b on l.code = b.code set l.name=b.name where l.name='';
update limit_up_stat l inner join basics b on l.code = b.code set l.name=b.name, l.industry=b.industry, l.area=b.area, l.pe=b.pe
where l.name is null;

select *
from limit_up_stat
where combo > 1
  and (wave_a < -33 and wave_b < 30 or wave_b <= -33)
order by wave_a;

-- 涨停汇总
select lus.code, max(lus.name) name, count(lus.combo) total, max(lus.combo) max, c.concepts
from limit_up_stat lus inner join basics b on lus.code = b.code left join concepts c on lus.code = c.code
where b.list_date < 20190101 and lus.trade_date > '2020-01-01'
group by lus.code
having count(lus.combo) > 1
order by total desc;


