select "name".name, aka_name.name from aka_name
join "name" on "name".id = aka_name.person_id
limit 100;

select * from comp_cast_type limit 100;

select cn.name, t.title, rt.role from cast_info ci
join title t on t.id = ci.movie_id
join "name" n on n.id = ci.person_id
join role_type rt on rt.id = ci.role_id
join char_name cn on cn.id = ci.person_role_id
where n.name = 'Pitt, Brad'
and rt.role = 'actor'
limit 100;

select * from pg_stat_all_tables
limit 100;

select * from pg_stat_all_tables psat
join pg_statistic ps on ps.starelid = psat.relid
where psat.relname = 'aka_name';

select * from pg_stats where tablename = 'aka_name';

SELECT
    *
FROM
    information_schema.columns
WHERE
    table_name = 'pg_statistic';


select * from pg_statistic ps
join pg_stat_all_tables psat on psat.relid = ps.starelid
where psat.relname = 'aka_name'
limit 100;

EXPLAIN ANALYZE SELECT "aka_name"."name" FROM "aka_name" INNER JOIN "name" ON ("aka_name"."person_id" = "name"."id") WHERE "name"."name" = 'Pitt, Brad' LIMIT 21;

SELECT COUNT(*), "name" FROM "name"
group by "name"
having COUNT(*) > 3;

select * from "name"
where "name" = 'Pratap';

select * from role_type;

