class OrderNotFoundException(Exception):
    def __init__(self, message="Order ID not found"):
        super().__init__(message)
