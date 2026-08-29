SELECT
    EXTRACT(YEAR FROM date_time) AS year,
    AVG(value_mwh) AS avg_consumption_mwh
FROM {{ ref('stg_total_consumption') }}
GROUP BY EXTRACT(YEAR FROM date_time)
ORDER BY year