from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.Customer import Customer
from entity.Product import Product


def main():
    repo = OrderProcessorRepositoryImpl()

    while True:
        print("\n====== E-Commerce Menu ======")
        print("1. Register Customer")
        print("2. Create Product")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Place Order")
        print("6. View Orders")
        print("7. Delete customer")
        print("8. Delete Product")
        print("9. Remove from Cart")
        print("10. Viewby Orderid")
        print("11. View Customer Details")
        print("12. View Product Details")
        print("13. View All Products")
        print("14. View Orders By Customer")
        print("15. Exit")


        choice = input("Enter your choice: ")

# REGISTERING A CUSTOMER

        if choice == "1":
            name=input("Enter your name:")
            username = input("Enter user name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            customer = Customer(name=name,username=username, email=email, password=password)
            if repo.create_customer(customer):
                print(" Customer registered successfully.")
            else:
                print("Failed to register customer.")

# CREATING PRODUCT

        elif choice == "2":
            name = input("Enter product name: ")
            price = float(input("Enter price: "))
            description = input("Enter description: ")
            stock = int(input("Enter stock quantity: "))
            product = Product(name=name, price=price, description=description, stock_quantity=stock)
            if repo.create_product(product):
                print(" Product created successfully.")
            else:
                print("Failed to create product.")

# ADDING TO CART

        elif choice == "3":
            customer_username = input("Enter user name: ")
            product_name = input("Enter product name to add to cart: ")
            quantity = int(input("Enter quantity: "))
            if repo.add_to_cart(customer_username, product_name, quantity):
                print(" Product added to cart.")
            else:
                print("Failed to add to cart.")

# VIEWING CART
        elif choice == "4":
            customer_username = input("Enter user name: ")
            cart_items = repo.get_all_from_cart(customer_username)
            if cart_items:
                print("Cart Items:")
                for item in cart_items:
                    print(f"{item['product_id']} | {item['name']} | ₹{item['price']} | Qty: {item['quantity']}")
            else:
                print("Cart is empty or customer not found.")

# PLACING ORDER
        elif choice == "5":
            customer_username = input("Enter user name: ")
            customer = repo.get_customer_by_name(customer_username)
            if not customer:
                print(" Customer not found!")
                return
            cart_items = repo.get_all_from_cart(customer_username)
            if not cart_items:
                print(" Cart is empty!")
                return
            shipping = input("Enter shipping address: ")
            product_quantity_list = []
            for item in cart_items:
                product = Product(product_id=item['product_id'], price=item['price'])
                product_quantity_list.append((product, item['quantity']))
            if repo.place_order(customer, product_quantity_list, shipping):
                print("Order placed successfully.")
            else:
                print(" Failed to place order.")


# VIEWING ORDERS BY CUSTOMER NAME

        elif choice == "6":
            customer_username = input("Enter user name: ")
            orders = repo.get_orders_by_customer(customer_username)
            if not orders:
                print("No orders found for this customer.")
            else:
                for order in orders:
                    print(f"\nCustomer: {order['customer_username']}")
                    print(f"Order ID   : {order['order_id']}")
                    print(f"Date       : {order['order_date']}")
                    print(f"Total      : ₹{order['total_price']}")
                    print(f"Address    : {order['shipping_address']}")
                    print("Items:")
                    for item in order['items']:
                        print(f"  - {item['product_name']} | Price: ₹{item['price']} | Qty: {item['quantity']}")

# DELETING CUSTOMER

        elif choice == "7":
            username = input("Enter user Name to delete: ")
            if repo.delete_customer(username):
                pass
            else:
                print("Could not delete customer.")

# DELETING PRODUCT

        elif choice == "8":
            name = input("Enter Product Name to delete: ")
            if repo.delete_product(name):
                pass
            else:
                print(" Could not delete product.")


# REMOVING FROM CART
        elif choice == "9":
            customer_username = input("Enter user name: ")
            product_name = input("Enter product name to remove from cart: ")
            if repo.remove_from_cart(customer_username, product_name):
                pass
            else:
                print("Could not remove product from cart.")



# GETTING ORDER DETAILS BY ORDER ID
        elif choice == "10":
            try:
                order_id = int(input("Enter Order ID to view details: "))
                details = repo.get_order_details_by_order_id(order_id)

                if details:
                    print(f"\n Order Details for Order ID {order_id}:")
                    for item in details:
                        print(f"Customer: {item['customer_name']} | Product: {item['product_name']} | "
                              f"Quantity: {item['quantity']} | Date: {item['order_date']}")
                else:
                    print(" No order found or error retrieving order.")
            except ValueError:
                print("Invalid order ID format.")

#VIEWING CUSTOMER DETAILS
        elif choice == "11":
            customer_username= input("Enter user name: ")
            repo.view_details_by_customer(customer_username)

#VIEWING PRODUCT DETAILS
        elif choice == "12":
            product_name = input("Enter product name to view details: ")
            repo.view_products_details(product_name)

# VIEWING ALL PRODUCTS
        elif choice == "13":
            repo.view_all_products()


# VIEWING ORDERS BY CUSTOMER NAME
        elif choice == "14":
            username = input("Enter username to view orders: ")
            repo.get_orders_by_customer(username)

#EXITTING
        elif choice == "15":
            print(" Thank you ")
            break


if __name__ == "__main__":
    main()
