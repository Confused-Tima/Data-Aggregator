# Documentation of this project + Experience while development

(If viewing in vs-code press `ctrl+shift+v`)

#### Personal Requst
Hi, Author here. Regardless of whether you like it or not. I would like to request you to send me a feedback on the project.

You can mail me on [Hello Author](mailto:thsibtima1999@gmail.com).
Or text me on [LinkedIn Profile](https://www.linkedin.com/in/amit-bisht-4b07b3201/)

Apologies for the rushed nature of this documentation. I appreciate your patience and understanding as I work through this.

First of all apologies for the delay. But I've been working 7 days of the week. It was already a very busy week on top of that I had 2 assignments. Yesterday I was working on another project as well. So this one got delayed.

Just in case you are interested in other project, then you can find it at [Image Processor](https://github.com/Confused-Tima/Image-Processor/blob/main/README.md).
Both these could give you a better idea of my coding skills. And don't worry the link has all the requirements for the project as wel as my personal experience while building it(will not cover it here).


It was a fine and simple project but did consume my time alot specifically because I've not worked in django for atleast 1 year now. Those configs and looking for best practices took just too long.

If you have any doubts or any things related to it. You can use the above links.

## 1st Assessment: The Query

You can find the:
- [First Answer here](UserCategorySpent.sql)
- [Second Answer here](UserTotalSpentQuery.sql)

I have tried dividing the queried in much smaller subqueries. And then combined them up to fetch the result out of it.

Originally I had planned to attach lots of images as well of test cases and sub-queries smaller results but now I don't have the time to attach all those. But will try to cover their details.

### 1st Sub Query (Order to Customer `customer_orders`)
(Sub query name: `customer_orders`)

It joins order table to customer. Used left join from orders -> customer table
So that those customer don't get fetched which are don't have any orders. And before joining I'm filtering out the orders within last year to keep the query optimized and not processing any uncessary data.

### 2nd Sub Query (OrderItems to Products `ordered_items`)
(Sub query name: `ordered_items`)

This sub-query joins order-items table to products table. It removes unncessary columns and only products which have been ordered until now.

### 3rd Sub Query ([Sub Query 1](#1st-sub-query-order-to-customer-customer_orders) to [Sub Query 2](#2nd-sub-query-orderitems-to-products-ordered_items))
(Sub query name: `customer_ordered_items`)

This sub-query connects both of those virtual tables. This fetches only those items which are not older than 1 year.

### 4th Sub Query (Groups [Sub Query 3](#3rd-sub-query-sub-query-1-to-sub-query-2))
(Sub query name: `customer_ordered_items_per_category`)

This sub-query groups the data based on categories. And these categories were present in product tables so we fetched these using [Sub Query 2](#2nd-sub-query-orderitems-to-products-ordered_items).

### Final result

Now here I was a bit confused. I didn't know whether `total_spent` was refering to the total spent in the most spent category or to the user's total spent. So I did both. First part of very easy. But for the second one I struggled a bit which wasted a lot of my time.

So I have added them both in separated files.
You can find them with the link or just find the .sql files in the root of the folder.


## Django Project

Actually there is alot to talk about but it's sunday night and almost 12, so I would like to wrap it up faster.

I have used postgresql database. Specifically because of this constraint:
- `Create a table to store the product data if it does not already exist.`

So if data exists then I have to make sure that it do not get entered again or generate some error.

I wanted to use `on conflict` clause of postgres, but unfortunately that was not present in django ORM.

I wanted to use sqlalchemy and probably in actual scenario I would pick that one up for it's flexibilty but if I had picked that one here then I would have passed the deadline. So earlier I was just making sure that primary keys are not present in the database tables. And inserting after that only.

That had a very big and simple flaw. I would like to give you some time to think as to what could it be??


