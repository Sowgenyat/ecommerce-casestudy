from dao.OrderProcessorRepository import OrderProcessorRepository
from util.DBConnUtil import get_connection
from datetime import date

class OrderProcessorRepositoryImpl(OrderProcessorRepository):

    def create_customer(self, customer):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            db.execute(query, (customer.get_name(), customer.get_email(), customer.get_password()))
            conn.commit()
            return True
        except Exception as e:
            print("Error creating customer:", e)
            return False
        finally:
            if conn:
                conn.close()

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

    def delete_product(self, product_id):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "DELETE FROM products WHERE product_id = %s"
            db.execute(query, (product_id,))
            conn.commit()
            return db.rowcount > 0
        except Exception as e:
            print("Error deleting product:", e)
            return False
        finally:
            if conn:
                conn.close()

    def delete_customer(self, customer_id):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = "DELETE FROM customers WHERE customer_id = %s"
            db.execute(query, (customer_id,))
            conn.commit()
            return db.rowcount > 0
        except Exception as e:
            print("Error deleting customer:", e)
            return False
        finally:
            if conn:
                conn.close()

    def add_to_cart(self, customer, product, quantity):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            check_query = "SELECT quantity FROM cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(check_query, (customer.get_customer_id(), product.get_product_id()))
            result = cursor.fetchone()

            if result:
                new_quantity = result[0] + quantity
                update_query = "UPDATE cart SET quantity = %s WHERE customer_id = %s AND product_id = %s"
                cursor.execute(update_query, (new_quantity, customer.get_customer_id(), product.get_product_id()))
            else:
                insert_query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (customer.get_customer_id(), product.get_product_id(), quantity))

            conn.commit()
            return True
        except Exception as e:
            print("Error adding to cart:", e)
            return False
        finally:
            if conn:
                conn.close()

    def remove_from_cart(self, customer, product):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(query, (customer.get_customer_id(), product.get_product_id()))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error removing from cart:", e)
            return False
        finally:
            if conn:
                conn.close()

    def get_all_from_cart(self, customer):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()
            query = """
            SELECT p.product_id, p.name, p.price, p.description, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            WHERE c.customer_id = %s
            """
            db.execute(query, (customer.get_customer_id(),))
            result = db.fetchall()

            product_list = []
            for row in result:
                product = {
                    "product_id": row[0],
                    "name": row[1],
                    "price": row[2],
                    "description": row[3],
                    "quantity": row[4]
                }
                product_list.append(product)

            return product_list
        except Exception as e:
            print("Error retrieving cart:", e)
            return []
        finally:
            if conn:
                conn.close()

    def place_order(self, customer, product_quantity_list, shipping_address):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()

            total_price = sum(p.get_price() * q for p, q in product_quantity_list)

            insert_order = "INSERT INTO orders (customer_id, order_date, total_price, shipping_address) VALUES (%s, %s, %s, %s)"
            db.execute(insert_order, (customer.get_customer_id(), date.today(), total_price, shipping_address))
            order_id = db.lastrowid

            for product, quantity in product_quantity_list:
                insert_item = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                db.execute(insert_item, (order_id, product.get_product_id(), quantity))

            clear_cart = "DELETE FROM cart WHERE customer_id = %s"
            db.execute(clear_cart, (customer.get_customer_id(),))

            conn.commit()
            return True
        except Exception as e:
            print("Error placing order:", e)
            return False
        finally:
            if conn:
                conn.close()

    def get_orders_by_customer(self, customer_id):
        conn = None
        try:
            conn = get_connection()
            db = conn.cursor()

            query = """
            SELECT o.order_id, o.order_date, o.total_price, o.shipping_address,
                   p.product_id, p.name, oi.quantity
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.customer_id = %s
            ORDER BY o.order_id
            """
            db.execute(query, (customer_id,))
            results = db.fetchall()

            order_details = []
            for row in results:
                order_details.append({
                    "order_id": row[0],
                    "order_date": row[1],
                    "total_price": row[2],
                    "shipping_address": row[3],
                    "product_id": row[4],
                    "product_name": row[5],
                    "quantity": row[6]
                })

            return order_details
        except Exception as e:
            print("Error fetching orders:", e)
            return []
        finally:
            if conn:
                conn.close()

