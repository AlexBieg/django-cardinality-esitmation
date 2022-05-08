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
