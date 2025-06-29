class ProductNotFoundException(Exception):
    def __init__(self, message="Product ID not found"):
        super().__init__(message)
