from wallet import *
from main import _goodColor, _badColor, _endColor, _neutralColor, colors, FEE, price, ticker
import datetime

class TransactionManager(object):

    def __init__(self, identifier, balance, strategy):
        self.identifier = identifier
        self.initialBalance = balance
        self.strategy = strategy
        self.usd = Wallet(balance)
        self.btc = Wallet(0.0)
        self.distributedBalance = self.usd.balance() // 10
        self.book = []
        self.log = []
        self.first_low = 0
        self.second_low = 0
        self.running = False

    def start(self):
        """ Starts the TM. """
        self.running = True

    def update(self, btcprice):
        """ The update loop. Grabs current price, buys then sells. Maintains
            a log of all transactions.
        """
        if btcprice <= self.buyPrice():
            if usd.hasFunds(self.distributedBalance):
                buy(self.distributedBalance, btcprice)
            else:
                self.usd.insufficientFunds()
        for transaction in self.book:
            if btcprice >= transaction.sellPrice():
                print 'Profit: ',
                self.sell(transaction, btcprice)
            if btcprice <= (transaction.initial_btcprice * 0.999):
                print 'Loss: ',
                self.sell(transaction, btcprice)

    def stop(self, btcprice):
        """ Sells all BTC then stops running the TM. """
        for transaction in self.book:
            transaction.sell(btcprice)
        self.running = False

    ##########
    # Status #
    ##########

    def status(self, p=price()):
        """ Returns the status of the TM - whether or not profitable. """
        val = self.value(p)
        if val > self.initialBalance:
            return _goodColor + 'Good' + _endColor
        elif val < self.initialBalance:
            return _badColor + 'Bad' + _endColor
        return _neutralColor + 'Neutral' + _endColor

    def value(self, p=price()):
        """ Returns the value in USD of the TM's holdings. Includes BTC and USD balances. """
        total = self.usd.balance() + \
            (self.btc.balance() * p)
        return total

    def currstrategy(self):
        """ Returns the strategy. For use in bot.py. """
        return self.strategy

    def negative(self):
        """ Returns whether this TransactionManager has reached the negative profit threshold. """
        if self.value() <= (self.initialBalance * 0.995):
            return True
        return False

    def getLog(self):
        """ Returns an list of transactions with the following columns: 
        TransactionManager Identifier, Initial DateTime, Final DateTime, Purchased BTC Amount, 
        Initial BTC-USD Price, Final BTC-USD Price, Initial USD Balance, Final USD Balance. """
        complete = []
        for transaction in self.log:
            history = []
            history.append(self.identifier)
            history.append(transaction.time_create)
            history.append(transaction.time_destroy)
            history.append(transaction.btc_balance)
            history.append(transaction.initial_btcprice)
            history.append(transaction.final_btcprice)
            history.append(transaction.initial_usd)
            history.append(transaction.final_usd)
            complete.append(history)
        return complete

    ############
    # Analysis #
    ############

    def buyPrice(self):
        """Determine the optimal buy price."""
        if self.first_low == 0:
            self.first_low = float(ticker()['ticker']['low'])
        elif self.second_low == 0:
            next_low = float(ticker()['ticker']['low'])
            if self.first_low != next_low:
                self.second_low = next_low
        else:
            next_low = float(ticker()['ticker']['low'])
            if self.second_low != next_low:
                self.third_low = next_low
                if self.first_low > self.second_low:
                    if self.second_low < self.third_low:
                        return True
                self.first_low = self.second_low
                self.second_low = self.third_low
        return False

    ###################
    # Trade Execution #
    ###################

    def buy(self, usd_balance, btcprice):
        """ Buys USD_BALANCE amount of BTC. Creates a new Transaction object. Updates
            the balance of USD by subtracting the BALANCE. Returns a Transaction.
        """
        transaction = Transaction(usd_balance, self.strategy, btcprice)
        self.usd.subtract(usd_balance + (usd_balance * FEE))
        self.btc.add(transaction.btc_balance)
        self.book.append(transaction)
        print "TM" + str(self.identifier) + ": Purchased " + str(usd_balance / btcprice) + " BTC at $" + str(btcprice)

    def sell(self, transaction, btcprice):
        """ Instructs the Transaction to sell. Adds to balance. """
        self.usd.add(transaction.sell(btcprice))
        self.btc.subtract(transaction.btc_balance)
        self.log.append(transaction)
        self.book.remove(transaction)
        print "TM" + str(self.identifier) + ": Sold " + str(transaction.final_usd / btcprice) + " at $" + str(btcprice)


class Transaction(object):

    def __init__(self, usd_balance, strategy, initial_btcprice):
        self.initial_usd = usd_balance
        self.final_usd = 0.0
        self.btc_balance = self.initial_usd / initial_btcprice
        self.time_create = datetime.datetime.now()
        self.time_destroy = 0
        self.strategy = strategy
        self.initial_btcprice = initial_btcprice
        self.final_btcprice = 0

    def sellPrice(self):
        """Determine the optimal BTC market price for selling the transaction.
           Must make a profit that exceeds the percent return dictated by self.strategy
           plus the fee (0.002) incurred from the market. 
           """
        return self.initial_btcprice * (1 + FEE + self.strategy)

    def sell(self, btcprice):
        """Completes the Transaction. Records time sold """
        self.final_btcprice = btcprice
        self.time_destroy = datetime.datetime.now()
        self.final_usd = self.btc_balance * btcprice
        return self.final_usd

