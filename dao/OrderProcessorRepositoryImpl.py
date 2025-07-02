from dao.OrderProcessorRepository import OrderProcessorRepository
from util.DBConnUtil import get_connection
from entity.Customer import Customer
from datetime import date
from tabulate import tabulate
import re

class OrderProcessorRepositoryImpl(OrderProcessorRepository):

 #REGISTERING CUSTOMER
    def create_customer(self, customer):
     conn = None
     try:
        password = customer.get_password()
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
        if not re.match(pattern, password):
            print("Password should be 8 characters long and should contain an uppercase, lowercase letter and a digit")
            return False
        conn = get_connection()
        db = conn.cursor()
        db.execute("SELECT COUNT(*) FROM customers WHERE username = %s", (customer.get_username(),))
        if db.fetchone()[0] > 0:
            print("Username already exists.")
            return False
        db.execute("SELECT COUNT(*) FROM customers WHERE email = %s", (customer.get_email(),))
        if db.fetchone()[0] > 0:
            print("Email already registered.")
            return False
        insert_query = "INSERT INTO customers (name, username, email, password) VALUES (%s, %s, %s, %s)"
        db.execute(insert_query, (
            customer.get_name(),
            customer.get_username(),
            customer.get_email(),
            password
        ))
        conn.commit()
        print("Customer registered successfully.")
        return True
     except Exception as e:
        print("Error creating customer:", e)
        return False
     finally:
        if conn:
            conn.close()

#CREATING PRODUCT
    def create_product(self, product):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "INSERT INTO products (name, price, description, stock_Quantity) VALUES (%s, %s, %s, %s)"
            db.execute(query, (
                product.get_name(),
                product.get_price(),
                product.get_description(),
                product.get_stock_quantity()
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error creating product:", e)
            return False
        finally:
            if conn:
                conn.close()

#DELETING PRODUCT
    def delete_product(self, name):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "SELECT product_id, name, price FROM products WHERE name = %s"
            db.execute(query, (name,))
            product = db.fetchone()
            if not product:
                print("Product not found.")
                return False
            product_id, product_name, price = product
            check_query = "SELECT COUNT(*) FROM order_items WHERE product_id = %s"
            db.execute(check_query, (product_id,))
            if db.fetchone()[0] > 0:
                print("cant delete the product,it has been ordered")
                return False
            print(f"Found Product: ID = {product_id}, Name = {product_name}, Price = ₹{price}")
            confirm = input("Are you sure you want to delete this product? (yes/no): ")
            if confirm.lower() != "yes":
                print("Deletion cancelled")
                return False
            delete_query = "DELETE FROM products WHERE product_id = %s"
            db.execute(delete_query, (product_id,))
            conn.commit()
            if db.rowcount > 0:
                print(" Product deleted successfully.")
                return True
            else:
                print(" Failed to delete product.")
                return False
        except Exception as e:
            print("Error deleting product:", e)
            return False
        finally:
            if conn:
                conn.close()



#Deleting customer
    def delete_customer(self, username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "SELECT customer_id, name, email FROM customers WHERE username = %s"
            db.execute(query, (username,))
            customer = db.fetchone()
            if not customer:
                print("Customer not found")
                return False
            customer_id, name, email = customer
            print(f"Found Customer: ID = {customer_id}, Name = {name}, Username = {username}, Email = {email}")
            confirm = input("Are you sure you want to delete this customer? (yes/no): ")
            if confirm.lower() != "yes":
                print("Deletion cancelled")
                return False
            delete_query = "DELETE FROM customers WHERE username = %s"
            db.execute(delete_query, (username,))
            conn.commit()
            if db.rowcount > 0:
                print("Customer deleted successfully.")
                return True
            else:
                print("Failed to delete customer.")
                return False
        except Exception as e:
            print("Error deleting customer:", e)
            return False
        finally:
            if conn:
                conn.close()



#GETTING ORDER DETAILS BY ORDER ID
    def get_order_details_by_order_id(self, order_id):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = """
                SELECT c.name AS customer_name, p.name AS product_name, oi.quantity, o.order_date
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_id = %s
            """
            db.execute(query, (order_id,))
            rows = db.fetchall()
            if not rows:
                print("No order found with the given order ID")
                return []
            order_details = []
            for row in rows:
                order_details.append({
                    "customer_name": row[0],
                    "product_name": row[1],
                    "quantity": row[2],
                    "order_date": row[3]
                })
            return order_details
        except Exception as e:
            print("Error retrieving order details", e)
            return []
        finally:
            if conn:
                conn.close()


#ADDING TO CART
    def add_to_cart(self, customer_username, product_name, quantity):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("SELECT customer_id FROM customers WHERE username = %s", (customer_username,))
            c_row = db.fetchone()
            if not c_row:
                print(" Customer not found")
                return False
            customer_id = c_row[0]
            db.execute("SELECT product_id, stock_quantity FROM products WHERE name = %s", (product_name,))
            p_row = db.fetchone()
            if not p_row:
                print("Product not found")
                return False
            product_id, stock = p_row
            if stock < quantity:
                print(f"  Only {stock} stock is available. Cannot add {quantity}.")
                return False
            db.execute("SELECT quantity FROM cart WHERE customer_id = %s AND product_id = %s",
                       (customer_id, product_id))
            existing = db.fetchone()
            if existing:
                new_qty = existing[0] + quantity
                if new_qty > stock:
                    print(f"  Only {stock} units available. Cannot update cart to {new_qty}.")
                    return False
                db.execute("UPDATE cart SET quantity = %s WHERE customer_id = %s AND product_id = %s",
                           (new_qty, customer_id, product_id))
            else:
                db.execute("INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (customer_id, product_id, quantity))
            db.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                       (quantity, product_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error adding to cart:", e)
            return False
        finally:
            if conn:
                conn.close()


#VIEWING ORDERS BY CUSTOMER NAME
    def get_orders_by_customer(self, customer_username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            get_customer_query = "SELECT customer_id, name,username FROM customers WHERE username = %s"
            db.execute(get_customer_query, (customer_username,))
            customer_result = db.fetchone()
            if not customer_result:
                print("Customer not found")
                return []
            customer_id = customer_result[0]
            customer_name=customer_result[1]
            customer_username = customer_result[2]
            query = """
            SELECT o.order_id, o.order_date, o.total_price, o.shipping_address,
                   p.name, p.price, oi.quantity
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.customer_id = %s
            ORDER BY o.order_date DESC
            """
            db.execute(query, (customer_id,))
            results = db.fetchall()
            orders = {}
            for row in results:
                order_id = row[0]
                if order_id not in orders:
                    orders[order_id] = {
                        "customer_name": customer_name,
                        "customer_username":customer_username,
                        "order_date": row[1],
                        "total_price": row[2],
                        "shipping_address": row[3],
                        "items": []
                    }
                orders[order_id]["items"].append({
                    "product_name": row[4],
                    "price": row[5],
                    "quantity": row[6]
                })
            for order_id, data in orders.items():
                print(f"\nCustomer: {data['customer_name']}")
                print(f"\nCustomer: {data['customer_username']}")
                print(f"Order ID    : {order_id}")
                print(f"Order Date  : {data['order_date']}")
                print(f"Shipping To : {data['shipping_address']}")
                print(f"Total Price : ₹{data['total_price']:.2f}")
                item_table = []
                for item in data["items"]:
                    item_table.append([
                        item["product_name"],
                        f"₹{item['price']:.2f}",
                        item["quantity"],
                        f"₹{item['price'] * item['quantity']:.2f}"
                    ])
                print(tabulate(item_table, headers=["Product", "Price", "Qty", "Subtotal"], tablefmt="grid"))
            return list(orders.values())
        except Exception as e:
            print("Error fetching orders:", e)
            return []
        finally:
            if conn:
                conn.close()



#VIEWING CART
    def get_all_from_cart(self, customer_username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("SELECT customer_id FROM customers WHERE username = %s", (customer_username,))
            result = db.fetchone()
            if not result:
                print("Customer not found")
                return []
            customer_id = result[0]
            query = """
            SELECT p.product_id, p.name, p.price, p.description, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            WHERE c.customer_id = %s
            """
            db.execute(query, (customer_id,))
            rows = db.fetchall()
            product_list = []
            for row in rows:
                product_list.append({
                    "product_id": row[0],
                    "name": row[1],
                    "price": row[2],
                    "description": row[3],
                    "quantity": row[4]
                })
            return product_list
        except Exception as e:
            print("Error in retrieving cart", e)
            return []
        finally:
            if conn:
                conn.close()


#PLACING ORDER
    def place_order(self, customer, product_quantity_list, shipping_address):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            total_price = sum(p.get_price() * q for p, q in product_quantity_list)
            insert_order = """
                INSERT INTO orders (customer_id, order_date, total_price, shipping_address)
                VALUES (%s, %s, %s, %s)
            """
            db.execute(insert_order, (customer.get_customer_id(), date.today(), total_price, shipping_address))
            order_id = db.lastrowid
            total_items_this_order = 0
            for product, quantity in product_quantity_list:
                total_items_this_order += quantity
                insert_item = """
                    INSERT INTO order_items (order_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """
                db.execute(insert_item, (order_id, product.get_product_id(), quantity))
            clear_cart = "DELETE FROM cart WHERE customer_id = %s"
            db.execute(clear_cart, (customer.get_customer_id(),))
            db.execute("SELECT total_orders, total_products_ordered FROM customers WHERE customer_id = %s",
                       (customer.get_customer_id(),))
            row = db.fetchone()
            prev_orders = row[0] or 0
            prev_products = row[1] or 0
            updated_orders = prev_orders + 1
            updated_products = prev_products + total_items_this_order
            update_query = """
                UPDATE customers
                SET total_orders = %s,
                    total_products_ordered = %s
                WHERE customer_id = %s
            """
            db.execute(update_query, (updated_orders, updated_products, customer.get_customer_id()))
            conn.commit()

            print(f"\n Order placed")
            print(f" Total Items: {total_items_this_order}")
            print(f" Total Price: ₹{total_price}")
            print(f" Total orders by {customer.get_name()}: {updated_orders}")
            print(f"Total products ordered by {customer.get_name()}: {updated_products}")
            return True
        except Exception as e:
            print("Error placing order:", e)
            return False
        finally:
            if conn:
                conn.close()

#VIWING  PRODUCTS DETAILS
    def view_products_details(self, product_name):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("""
                SELECT product_id, name, price, description, stock_quantity
                FROM products
                WHERE name = %s
            """, (product_name,))
            product = db.fetchone()
            if not product:
                print(" Product not found")
                return
            product_id, name, price, description, stock = product
            db.execute("""
                SELECT SUM(quantity) FROM order_items WHERE product_id = %s
            """, (product_id,))
            sold = db.fetchone()[0] or 0
            print(f"\nProduct Details:")
            print(f"Name        : {name}")
            print(f"Price       : ₹{price}")
            print(f"Description : {description}")
            print(f"Available   : {stock}")
            print(f"Sold        : {sold}")
        except Exception as e:
            print("Error retrieving product details:", e)
        finally:
            if conn:
                conn.close()

#VIEWING ALL PRODUCTS
    def view_all_products(self):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("""
                SELECT p.name, p.price, p.stock_quantity, 
                       IFNULL(SUM(oi.quantity), 0) AS total_sold,
                       p.description
                FROM products p
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.name, p.price, p.description, p.stock_quantity
                ORDER BY p.name
            """)
            rows = db.fetchall()
            if not rows:
                print("No products found.")
                return
            headers = ["Product Name", "Price (₹)", "Stock", "Sold", "Description"]
            table = []
            for row in rows:
                name, price, stock, sold, desc = row
                table.append([name, f"₹{price:.2f}", stock, sold, desc])
            print("\n All Products:")
            print(tabulate(table, headers=headers, tablefmt="grid"))
        except Exception as e:
            print("Error retrieving product list:", e)
        finally:
            if conn:
                conn.close()

#REMOVING PRODUCT FROM CART
    def remove_from_cart(self, customer_username, product_name):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("SELECT customer_id FROM customers WHERE username = %s", (customer_username,))
            customer = db.fetchone()
            if not customer:
                print("Customer not found.")
                return False
            customer_id = customer[0]
            db.execute("SELECT product_id FROM products WHERE name = %s", (product_name,))
            product = db.fetchone()
            if not product:
                print("Product not found.")
                return False
            product_id = product[0]
            db.execute(
                "SELECT quantity FROM cart WHERE customer_id = %s AND product_id = %s",
                (customer_id, product_id)
            )
            cart_item = db.fetchone()
            if not cart_item:
                print("Product not found in cart.")
                return False
            quantity_in_cart = cart_item[0]
            db.execute(
                "DELETE FROM cart WHERE customer_id = %s AND product_id = %s",
                (customer_id, product_id)
            )
            db.execute(
                "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                (quantity_in_cart, product_id)
            )
            conn.commit()
            print(" Product removed from cart and stock restored.")
            return True
        except Exception as e:
            print(" Error removing from cart:", e)
            return False
        finally:
            if conn:
                conn.close()

#LOGING IN CUSTOMER
    def login_customer(self,username, email, password):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "SELECT customer_id, name FROM customers WHERE email = %s AND password = %s"
            db.execute(query, (email, password))
            result = db.fetchone()
            if result:
                customer_id, name = result
                print(f" Login successful! Welcome, {name}.")
                return Customer(customer_id=customer_id,username=username, name=name, email=email, password=password)
            else:
                print(" Invalid email or password.")
                return None
        except Exception as e:
            print("Error during login:", e)
            return None
        finally:
            if conn:
                conn.close()


#VIEWING CUSTOMER
    def get_customer_by_name(self, username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("SELECT customer_id, name,username, email, password FROM customers WHERE username = %s", (username,))
            row = db.fetchone()
            if row:
                return Customer(customer_id=row[0], name=row[1], email=row[2], password=row[3])
            return None
        except Exception as e:
            print("Error fetching customer:", e)
            return None
        finally:
            if conn:
                conn.close()


#VIEWING DETAILS OF THE CUSTOMER


    def view_details_by_customer(self, customer_username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("""
                    SELECT customer_id, name, username, email, total_orders, total_products_ordered
                    FROM customers
                    WHERE username = %s
                """, (customer_username,))
            customer = db.fetchone()
            if not customer:
                print("Customer not found.")
                return
            customer_id, name, username, email, total_orders, total_products = customer
            print(f"\nCustomer Details:")
            print(f"Name                   : {name}")
            print(f"Username               : {username}")
            print(f"Email                  : {email}")
            print(f"Total Orders           : {total_orders}")
            print(f"Total Products Ordered : {total_products}")
            print("\nProducts in Cart:")
            db.execute("""
                    SELECT p.name, p.price, p.description, c.quantity
                    FROM cart c
                    JOIN products p ON c.product_id = p.product_id
                    WHERE c.customer_id = %s
                """, (customer_id,))
            cart_items = db.fetchall()
            if cart_items:
                for item in cart_items:
                    print(f" - {item[0]} (₹{item[1]} x {item[3]}), Desc: {item[2]}")
            else:
                print("Cart is empty.")
            print("\n Orders Placed:")
            db.execute("""
                    SELECT o.order_id, o.order_date, o.total_price, o.shipping_address,
                           p.name, p.price, oi.quantity
                    FROM orders o
                    JOIN order_items oi ON o.order_id = oi.order_id
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE o.customer_id = %s
                    ORDER BY o.order_date DESC
                """, (customer_id,))
            order_rows = db.fetchall()
            if not order_rows:
                print("No orders placed.")
            else:
                current_order = None
                for row in order_rows:
                    order_id, order_date, total_price, shipping_address, product_name, price, qty = row
                    if current_order != order_id:
                        current_order = order_id
                        print(f"\n Order ID   : {order_id}")
                        print(f"   Date       : {order_date}")
                        print(f"   Shipping   : {shipping_address}")
                        print(f"   Total Bill : ₹{total_price}")
                        print(f"   Items:")
                    print(f"     - {product_name} (₹{price} x {qty})")
        except Exception as e:
            print(" Error fetching customer details:", e)
        finally:
            if conn:
                conn.close()




#VIEWING ORDERS PLACED BY THE CUSTOMER
    def get_orders_by_customer(self, customer_username):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            db.execute("SELECT customer_id, username FROM customers WHERE username = %s", (customer_username,))
            customer_result = db.fetchone()
            if not customer_result:
                print("Customer not found")
                return []
            customer_id = customer_result[0]
            query = """
            SELECT o.order_id, o.order_date, o.total_price, o.shipping_address,
                   p.name, p.price, oi.quantity
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.customer_id = %s
            ORDER BY o.order_date DESC
            """
            db.execute(query, (customer_id,))
            results = db.fetchall()
            if not results:
                print("No orders found")
                return []
            orders = {}
            for row in results:
                order_id = row[0]
                if order_id not in orders:
                    orders[order_id] = {
                        "order_id": order_id,
                        "customer_username": customer_username,
                        "order_date": row[1],
                        "total_price": row[2],
                        "shipping_address": row[3],
                        "items": []
                    }
                orders[order_id]["items"].append({
                    "product_name": row[4],
                    "price": row[5],
                    "quantity": row[6]
                })
            for order_id, data in orders.items():
                print(f"\n Order ID: {order_id}")
                print(f"Date        : {data['order_date']}")
                print(f"Shipping To : {data['shipping_address']}")
                print(f"Total Price : ₹{data['total_price']:.2f}")
                item_table = []
                for item in data["items"]:
                    item_table.append([
                        item["product_name"],
                        f"₹{item['price']:.2f}",
                        item["quantity"],
                        f"₹{item['price'] * item['quantity']:.2f}"
                    ])
                print(tabulate(item_table, headers=["Product", "Price", "Qty", "Subtotal"], tablefmt="grid"))
            return list(orders.values())
        except Exception as e:
            print("Error fetching orders:", e)
            return []
        finally:
            if conn:
                conn.close()

