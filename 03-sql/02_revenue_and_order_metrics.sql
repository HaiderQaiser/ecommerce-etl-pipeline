/*========================================================
  QUERY 1: Overall Revenue & Order Performance
  Purpose:
  Provides a high-level business summary showing
  gross revenue, discounts, net revenue, and the
  total number of successfully delivered orders.
=========================================================*/

SELECT
    SUM(quantity * unit_price_pkr) AS gross_revenue,
    SUM(unit_price_pkr * discount_pct) AS total_discount,
    SUM(quantity * unit_price_pkr)
        - SUM(unit_price_pkr * discount_pct) AS net_revenue,
    COUNT(DISTINCT order_id) AS total_delivered_orders
FROM orders
WHERE order_status = 'Delivered';



/*========================================================
  QUERY 2: Revenue Contribution by Product Category
  Purpose:
  Identifies the highest-performing product categories
  based on net revenue generated from delivered orders.
  Useful for management reporting and category analysis.
=========================================================*/

SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(
        SUM(quantity * unit_price_pkr * (1 - discount_pct)),
        2
    ) AS net_revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY product_category
ORDER BY net_revenue DESC;



/*========================================================
  QUERY 3: Sales Channel Performance Analysis
  Purpose:
  Compares revenue and order volume across different
  sales channels (Website, Mobile App, Marketplace)
  to determine the most effective source of sales.
=========================================================*/

SELECT
    sales_channel,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(
        SUM(quantity * unit_price_pkr * (1 - discount_pct)),
        2
    ) AS net_revenue,
    ROUND(
        AVG(quantity * unit_price_pkr * (1 - discount_pct)),
        2
    ) AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY sales_channel
ORDER BY net_revenue DESC;