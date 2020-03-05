-- 每日涨停统计
select * from limit_up_daily where trade_date='2020-03-02';
select trade_date, count(1) from limit_up_daily group by trade_date order by trade_date desc;
select code, name, min(trade_date), max(trade_date), max(combo), count(1) from limit_up_daily group by code, name;

-- 更新基本信息
delete from limit_up_daily where trade_date='2020-02-28';
update limit_up_daily d inner join basics b on d.code = b.code set d.name = b.name, d.industry= b.industry where d.industry is null or d.industry='' or d.name is null or d.name='';
# update limit_up_stat l inner join basics b on l.code = b.code set l.name=b.name, l.industry=b.industry where l.name is null or l.name='';

-- 边嗰行业掂吖？
select trade_date, industry, count(1) cow
from limit_up_daily
where trade_date = '2020-03-03'
  and combo = 1
group by trade_date, industry
order by cow desc;

-- 拣吓货
select *
from limit_up_stat
where code in (select code from limit_up_daily where trade_date='2020-03-04')
# and industry in ('')
and combo > 1
order by wave_a;



