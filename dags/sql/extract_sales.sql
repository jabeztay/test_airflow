SELECT
    sale_id,
    sale_date,
    sale_value,
    salesperson_id
FROM sales
WHERE sale_date = '{{ ds }}';