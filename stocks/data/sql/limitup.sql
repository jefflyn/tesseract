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
where trade_date = '2020-03-11'
  and combo = 1
group by trade_date, industry
order by cow desc;

-- 拣吓货
select *
from limit_up_stat
where 1=1
and late_date='2020-03-11'
# and industry in ('')
and combo > 1
order by wave_a;

-- overall超短*
select lus.fire_date, lus.late_date,lus.code,lus.name,lus.industry,sra.list_date issue,sra.pe,lus.fire_price fire,lus.price,lus.combo,lus.count,lus.wave_a,lus.wave_b,
       sra.count tc, sra.wave_a t_a, sra.wave_b t_b, sra.wave_detail, sra.concepts
       from limit_up_stat lus left join select_result_all sra on lus.code = sra.code
where lus.combo > 2
and lus.code not like '688%' -- and lus.code = 000020
and (sra.wave_b < -33 or (sra.wave_b > 0 and sra.wave_b < 20) or (sra.wave_a < -40 and sra.wave_b < 30))
order by lus.wave_a asc;

-- overall中长*
select lus.fire_date, lus.late_date,lus.code,lus.name,lus.industry,sra.list_date issue,sra.pe,lus.fire_price fire,lus.price,lus.combo,lus.count,lus.wave_a,lus.wave_b,
       sra.count tc, sra.wave_a t_a, sra.wave_b t_b, sra.wave_detail, sra.concepts
       from limit_up_stat lus left join select_result_all sra on lus.code = sra.code
where lus.fire_date >= '2020-03-01'
and lus.code not like '688%'
order by sra.wave_a asc;

select count(1) from limit_up_stat where combo > 1;
select count(1) from limit_up_stat where count > 2;

198176 0
176198 0