foo = """
with query as (
    with days as (select generate_series(
    date %(fromDate)s,
    date %(toDate)s,
    '1 day'
    ) as d )
        select days.d, logger_id, sensor_id, (CASE WHEN state = 3 THEN 0 ELSE state %% 10 END) as status from devicestatus, days
        where sensor_id in (select sensor_id from {meta_projectid}) and devicestatus.updated_at < d + interval '1 day - 1 sec'
    union
        select days.d ,logger_id, sensor_id, (CASE WHEN state = 3 THEN 0 ELSE state %% 10 END) as status from devicestatuslog, days
        where sensor_id in (select sensor_id from {meta_projectid}) and (devicestatuslog.valid_from, devicestatuslog.valid_to) overlaps (d , d + interval '1 day - 1 sec')  

)
select cast(replace(concat (sensor_id, ':', d), '+00', '') as varchar)  as matcher
    from query group by d, sensor_id  
    having min(status) > 0 
"""
