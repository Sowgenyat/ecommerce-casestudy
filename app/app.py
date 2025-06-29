from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.customer import Customer
from entity.product import Product

def main():
    repo = OrderProcessorRepositoryImpl()

    while True:
        print("\n====== E-Commerce Menu ======")
        print("1. Register Customer")
        print("2. Create Product")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Place Order")
        print("6. View Orders by Customer")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            name = input("Enter customer name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            customer = Customer(name=name, email=email, password=password)
            if repo.create_customer(customer):
                print(" Customer registered successfully.")
            else:
                print(" Failed to register customer.")

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

        elif choice == "3":
            customer_id = int(input("Enter your customer ID: "))
            product_id = int(input("Enter product ID to add to cart: "))
            quantity = int(input("Enter quantity: "))
            customer = Customer(customer_id=customer_id)
            product = Product(product_id=product_id)
            if repo.add_to_cart(customer, product, quantity):
                print(" Product added to cart.")
            else:
                print(" Failed to add to cart.")

        elif choice == "4":
            customer_id = int(input("Enter your customer ID: "))
            customer = Customer(customer_id=customer_id)
            cart_items = repo.get_all_from_cart(customer)
            print(" Cart Items:")
            for item in cart_items:
                print(f"{item['product_id']} | {item['name']} | {item['price']} | Qty: {item['quantity']}")

        elif choice == "5":
            customer_id = int(input("Enter your customer ID: "))
            customer = Customer(customer_id=customer_id)
            cart_items = repo.get_all_from_cart(customer)
            if not cart_items:
                print("Cart is empty!")
                continue

            shipping = input("Enter shipping address: ")
            product_quantity_list = []
            for item in cart_items:
                product = Product(product_id=item['product_id'], price=item['price'])
                product_quantity_list.append((product, item['quantity']))

            if repo.place_order(customer, product_quantity_list, shipping):
                print(" Order placed successfully.")
            else:
                print(" Failed to place order.")

        elif choice == "6":
            customer_id = int(input("Enter your customer ID: "))
            orders = repo.get_orders_by_customer(customer_id)
            print(" Order History:")
            for item in orders:
                print(f"OrderID: {item['order_id']} | {item['product_name']} | Qty: {item['quantity']} | Date: {item['order_date']} | Address: {item['shipping_address']}")

        elif choice == "7":
            print("Thank you")
            break

        else:
            print(" Invalid choice. Try again.")


if __name__ == "__main__":
    main()
