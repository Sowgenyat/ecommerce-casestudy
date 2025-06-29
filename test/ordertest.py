def test_place_order(self):
    result = self.repo.placeOrder(customer, [{product: 1}], "Madurai")
    self.assertTrue(result)
