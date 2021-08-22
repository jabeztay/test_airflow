CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    sale_value INTEGER NOT NULL,
    salesperson_id INTEGER NOT NULL
);