def test_add_to_cart(self):
    result = self.repo.addToCart(customer, product, 2)
    self.assertTrue(result)
