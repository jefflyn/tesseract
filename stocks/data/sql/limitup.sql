-- index data
select * from hist_index_day where trade_date >= '2020-02-03' order by trade_date desc;
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '000001.SH', '000001', 2.28, now());
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '399001.SZ', '399001', 2.98, now());
INSERT INTO stocks.hist_index_day (trade_date, ts_code, code, pct_change, update_time)
VALUES ('2020-02-17', '399006.SZ', '399006', 3.72, now());

select trade_date, count(1) from limit_up_stat group by trade_date order by trade_date desc ;

# 不考虑【亏损股】、【B波涨幅过高】、【涨停数超过2】、【缩量】、【高开>4】（大盘较弱都要考虑不操作）
# 1、选【涨停开盘、缩量、换手率<3】，去除【亏损股、最大涨停数】
# 2、
select stat.trade_date 交易日期, stat.code 代码, stat.name 名称, stat.industry 行业, stat.area 地区, stat.pe 市盈率, stat.combo_times as 涨停数,
       stat.wave_a A波, stat.wave_b B波, stat.turnover_rate 换手率, stat.vol_rate 量比,
       case when vol_rate < 0.8 then '缩量（不活跃）'
           when vol_rate >= 0.8 and vol_rate < 1.5 then '正常水准（正常活动）'
           when vol_rate >= 1.5 and vol_rate < 2.5 then '柔和放量（相对健康）'
           when vol_rate >= 2.5 and vol_rate < 5 then '明显放量（突破机会）'
           when vol_rate >= 5 and vol_rate < 10 then '剧烈放量（低位好信号）'
           when vol_rate >= 10 then '巨量（反向操作）'
           when vol_rate >= 20 then '极端放量（死亡）'
           end as 量比解读,
       open_change 开盘幅度,
       next_low_than_open 次日低价, next_open_change 次日开盘幅度, next_low_change 次日底价幅度, next_open_buy_change 次日开盘买入涨幅,
       next_low_buy_change 次日底价买入涨幅, ref_index_change 大盘幅度, update_time
from limit_up_stat stat inner join basics b on stat.code = b.code where stat.trade_date='2020-02-18'
and b.pe > 0 and b.profit > 0
# and (stat.wave_a < -33 and stat.wave_b < 30 or stat.wave_b <= -33)
order by stat.wave_a;

select *
from limit_up_stat
where trade_date = '2020-02-19'
  and pe > 0
  and (wave_a < -33 and wave_b < 30 or wave_b <= -33)
order by wave_a;

-- 涨停汇总
select lus.code, max(lus.name) name, count(lus.combo_times) total, max(lus.combo_times) max, c.concepts
from limit_up_stat lus inner join basics b on lus.code = b.code left join concepts c on lus.code = c.code
where b.list_date < 20190101 and lus.trade_date > '2020-01-01'
group by lus.code
having count(lus.combo_times) > 1
order by total desc;

select * from concepts where code=000635;
select * from concepts where concepts like '%半导体%';
