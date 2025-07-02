import unittest
from entity.Product import Product
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.repo = OrderProcessorRepositoryImpl()

    def test_create_product(self):
        p = Product(101, "Phone", 50000, "iPhone 13", 10)
        result = self.repo.createProduct(p)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
