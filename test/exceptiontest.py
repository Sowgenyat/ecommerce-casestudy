from exception.CustomerNotFoundException import CustomerNotFoundException

def test_customer_not_found_exception(self):
    with self.assertRaises(CustomerNotFoundException):
        self.repo.getOrdersByCustomer(99)
