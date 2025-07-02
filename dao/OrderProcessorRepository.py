from abc import ABC, abstractmethod

class OrderProcessorRepository(ABC):

    @abstractmethod
    def create_product(self, product):
        pass

    @abstractmethod
    def view_details_by_customer(self, customer_name):
        pass

    @abstractmethod
    def create_customer(self, customer):
        pass

    @abstractmethod
    def login_customer(self, email, password):
        pass

    @abstractmethod
    def add_to_cart(self, customer, product, quantity):
        pass


    @abstractmethod
    def get_all_from_cart(self, customer):
        pass

    @abstractmethod
    def remove_from_cart(self, customer, product_name):
        pass


    @abstractmethod
    def delete_customer (self, name):
        pass

    @abstractmethod
    def delete_product(self, name):
        pass

    @abstractmethod
    def place_order(self, customer, product_quantity_list, shipping_address):
        pass
    @abstractmethod
    def view_products_details(self, product_name):
        pass
    @abstractmethod
    def get_orders_by_customer(self, customer_id):
        pass
    @abstractmethod
    def get_customer_by_name(self, name):
        pass
    @abstractmethod
    def get_order_details_by_order_id(self, order_id):
        pass

    @abstractmethod
    def view_all_products(self):
        pass
    @abstractmethod
    def get_orders_by_customer(self, customer_name):
        pass