with customer_orders as (
  select
    o.order_id,
    c.customer_id,
    c.customer_name,
    c.email
  from
    (
      select
        order_id,
        customer_id
      from
        orders o
      where
        order_date > now () - interval '1 year'
    ) as o
    left join customers c on o.customer_id = c.customer_id
),
ordered_items as (
  select
    oi.order_id,
    p.category,
    (oi.quantity * p.unit_price) as total_spent
  from
    order_items oi
    left join products p on oi.product_id = p.product_id
),
customer_ordered_items as (
  select
    co.customer_id,
    co.customer_name,
    co.email,
    oi.category,
    oi.total_spent
  from
    customer_orders co
    left join ordered_items oi on oi.order_id = co.order_id
),
customer_ordered_items_per_category as (
  select
    customer_id,
    customer_name,
    category,
    sum(total_spent) as total_spent
  from
    customer_ordered_items
  group by
    customer_id,
    customer_name,
    category
),
grouped_data as (
  select
  distinct on (customer_id) customer_id,
  customer_name,
  total_spent as category_spent,
  sum(total_spent) over (partition by customer_id) as total_spent,
  category
from
  customer_ordered_items_per_category
order by
  customer_id,
  category_spent desc
)
select * from grouped_data limit 5;
