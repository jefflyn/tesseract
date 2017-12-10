SELECT * FROM `wave_data` a
where (
select count(1) from `wave_data` 
where `code` = a.`code` and end > a.`end`) < 2
and `status` = 'down'
order by p_change;

select w.*,b.* from wave_data w inner join basics b on (w.code = b.code)
where w.status = 'down' 
and w.end >= '2017-12-04'
and w.p_change <= -30
order by w.p_change;