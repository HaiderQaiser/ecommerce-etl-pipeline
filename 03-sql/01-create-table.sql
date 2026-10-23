-- CREATE DATABASE Karachi_ecommerce; -- only run it once
-- GO

USE Karachi_ecommerce;
GO

CREATE TABLE orders (
    order_id INT NOT NULL,
    order_line_id INT NOT NULL PRIMARY KEY, -- Primary Key enforced
    order_date DATE NOT NULL,
    customer_id NVARCHAR(100) NOT NULL,
    city VARCHAR(200),
    product_category VARCHAR(300),
    product_name VARCHAR(300),
    quantity INT NOT NULL,
    unit_price_pkr DECIMAL(10,2) NOT NULL,
    discount_pct DECIMAL(5,2) NOT NULL,    -- 0.00 to 1.00 representation
    payment_method NVARCHAR(200),
    order_status VARCHAR(100),
    delivery_days INT NULL,
    sales_channel VARCHAR(100)
);