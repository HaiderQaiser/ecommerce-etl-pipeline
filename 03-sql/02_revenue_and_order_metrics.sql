-- What is the overall total gross revenue, total discount amount given,
-- net revenue, and total count of completed (delivered) orders for PakCart?

SELECT
	SUM(quantity * unit_price_pkr) AS gross_revenue,
	SUM(unit_price_pkr * discount_pct) AS total_discount,
	SUM(quantity * unit_price_pkr) - SUM(unit_price_pkr * discount_pct) AS net_revenue,
	COUNT(DISTINCT order_id) AS total_delivered_orders
FROM orders
WHERE order_status = 'Delivered'