class CustomerNotFoundException(Exception):
    def __init__(self, message="Customer ID not found"):
        super().__init__(message)
