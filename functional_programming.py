class FunctionalProgramming:
    def __init__(self):
        pass

    def map(self, func, iterable):
        return [func(item) for item in iterable]
    
    def find_maxprofit(self, prices, min_price, max_profit):
        if len(prices) < 1:
            return max_profit
        else:
            current_price = prices[0]
            if current_price - min_price > max_profit:
                max_profit = current_price - min_price
            if current_price < min_price:
                min_price = current_price
            return self.find_maxprofit(prices[1:], min_price, max_profit)
    