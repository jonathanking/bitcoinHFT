class Wallet(object):
    """A virtual currency wallet, primarily for testing purposes.

    >>> c = Wallet(10)
    >>> c.add(400)
    >>> c.balance()
    410
    >>> c.hasFunds(500)
    False

    """

    def __init__(self, amount):
        self.amount = amount

    def add(self, n):
        """ Adds n amount to the wallet. """
        self.amount += n

    def subtract(self, n):
        """ Subtracts n amount from the wallet. """
        self.amount -= n

    def balance(self):
        return self.amount

    def hasFunds(self, n):
        """Returns True if a there are sufficient funds to remove n from the
        wallet and maintain a positive balance. False otherwise. """
        if (self.amount - n) < 0:
            return False
        return True
