class InvalidTotalWeightException(Exception):
    def __init__(self):
        super().__init__('\n   The sum of the weights of all baskets must be less than 100%')

class BadAPICallException(Exception):
    def __init__(self):
        super().__init__('\n   A problem occurred during the API call')