class InvalidTotalWeightException(Exception):
    def __init__(self):
        super().__init__('\n\tThe sum of the weights of all baskets must be less than 100%')

class BadAPICallException(Exception):
    def __init__(self):
        super().__init__('\n\tA problem occurred during the API call')