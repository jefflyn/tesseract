select trade_date 交易日期, code 代码, name 名称, industry 行业, area 地区, pe 市盈率, combo_times as 涨停数,
       wave_a A波, wave_b B波, turnover_rate 换手率, vol_rate 量比,
       case when vol_rate < 0.8 then '缩量（不活跃）'
           when vol_rate >= 0.8 and vol_rate < 1.5 then '正常水准（正常活动）'
           when vol_rate >= 1.5 and vol_rate < 2.5 then '柔和放量（相对健康）'
           when vol_rate >= 2.5 and vol_rate < 5 then '明显放量（突破机会）'
           when vol_rate >= 5 and vol_rate < 10 then '剧烈放量（低位好信号）'
           when vol_rate >= 10 then '巨量（反向操作）'
           when vol_rate >= 20 then '极端放量（死亡）'
           end as 量比解读,
       open_change 开盘幅度,
       next_low_than_open 次日低价, next_open_change 次日开盘幅度, next_open_buy_change 次日开盘买入涨幅,
       next_low_buy_change 次日底价买入涨幅, ref_index_change 大盘幅度
from limit_up_stat where trade_date='2020-02-07' order by combo_times;

select * from limit_up_stat where trade_date='2020-02-07' and pe > 0
                              and (wave_a < -33 and wave_b < 30 or wave_b <= -33)
order by wave_a;

select trade_date 交易日期, code 代码, name 名称, industry 行业, area 地区, pe 市盈率, combo_times as 涨停数,
       wave_a A波, wave_b B波, turnover_rate 换手率, vol_rate 量比,
       case when vol_rate < 0.8 then '缩量（不活跃）'
           when vol_rate >= 0.8 and vol_rate < 1.5 then '正常水准（正常活动）'
           when vol_rate >= 1.5 and vol_rate < 2.5 then '柔和放量（相对健康）'
           when vol_rate >= 2.5 and vol_rate < 5 then '明显放量（突破机会）'
           when vol_rate >= 5 and vol_rate < 10 then '剧烈放量（低位好信号）'
           when vol_rate >= 10 then '巨量（反向操作）'
           when vol_rate >= 20 then '极端放量（死亡）'
           end as 量比解读,
       open_change 开盘幅度,
       next_low_than_open 次日低价, next_open_change 次日开盘幅度, next_open_buy_change 次日开盘买入涨幅,
       next_low_buy_change 次日底价买入涨幅, ref_index_change 大盘幅度
from limit_up_stat where trade_date='2020-02-07' and pe > 0
                              and (wave_a < -33 and wave_b < 30 or wave_b <= -33)
order by wave_a;



