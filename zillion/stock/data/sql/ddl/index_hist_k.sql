create table index_hist_k
(
	trade_date varchar(10) not null,
	code varchar(10) not null,
	open decimal(10,2) not null,
	close decimal(10,2) not null,
	high decimal(10,2) not null,
	low decimal(10,2) not null,
	volume decimal(15,2) not null,
	pct_change decimal(10,2) not null,
	primary key (trade_date, code)
);

