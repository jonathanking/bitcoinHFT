class Wallet(object):
	"""A virtual bitcoin wallet, primarily for testing purposes.
	>>> c = Wallet(10)
	>>> c.add(400)
	>>> c.getBalance()
	410
	>>> c.hasFunds(500)
	False

	"""

	def __init__(self, amount):
		self.balance = amount

	def add(self, n):
		""" Adds n bitcoins to the wallet. """
		self.balance += n
	def subtract(self, n):
		""" Adds n bitcoins to the wallet. """
		self.balance -= n
	def getBalance(self):
		return self.balance
	def hasFunds(self, n):
		if (self.balance - n) < 0:
			return False
		return True


