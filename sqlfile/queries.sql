create database ecommercedb;
USE  ecommercedb;

#customer table
create table customers (
    customer_id int auto_increment primary key,
    name varchar(100) not null,
    email varchar(100) unique not null,
    password varchar(100) not null
);

alter table customers
add total_orders int default 0,
add total_products_ordered int default 0;
alter table customers add username varchar(30) unique;

select * from customers;

#products table
create table products (
    product_id int auto_increment primary key,
    name varchar(100) not null,
    price decimal(10, 2) not null,
    description text,
    stock_quantity int not null
);

select * from products;


#cart table
create table cart (
    cart_id int auto_increment primary key,
    customer_id int not null,
    product_id int not null,
    quantity int not null,
    foreign key (customer_id) references customers(customer_id),
    foreign key (product_id) references products(product_id)
);

select * from cart;

show create table cart;

alter table cart
drop foreign key cart_ibfk_1;
alter table cart
add constraint cart_ibfk_1
foreign key (customer_id) references customers(customer_id)
on delete cascade;

#orders table
create table orders (
    order_id int auto_increment primary key,
    customer_id int not null,
    order_date date not null,
    total_price decimal(10, 2) not null,
    shipping_address text not null,
    foreign key (customer_id) references customers(customer_id)
);

show create table orders;

alter table orders
drop foreign key orders_ibfk_1;

alter table orders
add constraint orders_ibfk_1
foreign key (customer_id) references customers(customer_id)
on delete cascade;

select * from orders;

#order_items table
create table order_items (
    order_item_id int auto_increment primary key,
    order_id int not null,
    product_id int not null,
    quantity int not null,
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id)
);

show create table order_items;

alter table order_items
drop foreign key order_items_ibfk_1;

alter table order_items
add constraint order_fk
foreign key (order_id) references orders(order_id)
on delete cascade;


