"""
The bot class is the fundamental class of bitcoinHFT.
Bots will analyze the market data, execute trades, and handle the user's 
balance.
"""
from wallet import *

class Bot(object):
	""" Analyzes market data, executes trades, makes decisions, handles
	user's balance. """

	def __init__(self, user_wallet):
		self.wallet = user_wallet
		self.pendingTransactions = []


### Market Analysis ###

	def dayScore(self):
		pass


### Trade Execution ###

	def validTransaction(self, trans):
		"""Given a Transaction, returns True if the user wallet has sufficient funds."""
		if trans.value() >= 0:
			return True
		else:
			return self.wallet.hasFunds(trans.value())

	def executeTransaction(self, trans):
		self.wallet.add(trans.value())












class Transaction(object):
	""" Represents a transaction of bitcoins. Amount can be negative if the 
	bot is selling. """
	def __init__(self, amount):
		self.val = amount

	def type(self):
		""" Returns a string representation of the transaction type, buy or sell. """
		if self.val >= 0:
			return "buy"
		return "sell"

	def value(self):
		""" Returns the value of the transaction, positive or negative. """
		return self.val



w = Wallet(999)
b = Bot(w)
t = Transaction(-99)

