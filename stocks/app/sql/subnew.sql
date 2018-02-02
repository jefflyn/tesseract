SELECT * FROM `wave_data` a
where (
select count(1) from `wave_data`
where `code` = a.`code` and end > a.`end`) < 2
and `status` = 'down'
order by p_change;

select w.*,b.* from wave_data_x w inner join basics b on (w.code = b.code)
where w.status = 'up'
and w.end >= '2017-12-25'
-- and w.p_change <= -30
order by w.p_change;

-- 每只第一个down
drop table wave_temp;
CREATE TEMPORARY TABLE wave_temp
SELECT * FROM `wave_subnew` a
where (
select count(1) from `wave_subnew`
where `code` = a.`code` and end < a.`end`) < 2
and `status` = 'down'

-- 3rd up
drop table if EXISTS wave_3;
CREATE TABLE wave_3
select * from wave_subnew
where code in(
select code
from wave_subnew
group by code
having count(1) = 3);

drop table if EXISTS wave_3_up;
CREATE TABLE wave_3_up
SELECT * FROM `wave_3` b
where (
select count(1) from `wave_3`
where `code` = b.`code` and end > b.`end`) < 2
and `status` = 'up'
order by `change`;

select s.*, u.*
from pickup_subnew_issue_space s
inner join wave_3_up u
on (s.code = u.code)
order by `change`;

-- 5th up
drop table if EXISTS wave_5;
CREATE TABLE wave_5
select * from wave_subnew
where code in(
select code
from wave_subnew
group by code
having count(1) = 5);

drop table if EXISTS wave_5_up;
CREATE TABLE wave_5_up
SELECT * FROM `wave_5` b
where (
select count(1) from `wave_5`
where `code` = b.`code` and end > b.`end`) < 2
and `status` = 'up'
order by `change`;

select s.*, u.*
from pickup_subnew_issue_space s
inner join wave_5_up u
on (s.code = u.code)
order by `change`;
