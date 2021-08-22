INSERT INTO sales (sale_date, sale_value, salesperson_id)
SELECT
    '{{ ds }}' AS sale_date,
    FLOOR(RANDOM() * 10000) AS sale_value,
    i AS salesperson_id
FROM
    generate_series(1, 10) AS i;