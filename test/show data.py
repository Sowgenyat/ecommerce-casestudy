from util.DBConnUtil import get_connection

def show_all_customers():
    conn = get_connection()
    if conn:
        db = conn.cursor()
        db.execute("SELECT * FROM customers")
        rows = db.fetchall()
        print("\n--- All Customers ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
        conn.close()

def show_all_products():
    conn = get_connection()
    if conn:
        db = conn.cursor()
        db.execute("SELECT * FROM products")
        rows = db.fetchall()
        print("\n--- All Products ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]} | Stock: {row[4]}")
        conn.close()

if __name__ == "__main__":
    show_all_customers()
    show_all_products()
