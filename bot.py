"""
The bot class is the fundamental class of bitcoinHFT.
Bots will analyze the market data, execute trades, and handle the user's 
balance.
"""
from random import randint
from time import sleep

from main import colors, price
from texttable import Texttable
from TransactionManager import *
from wallet import *

_delay = 5

class Bot(object):
    """ Analyzes market data, executes trades, makes decisions, handles
    user's balance. """
    def __init__(self, live, balance, count):
        self.live = live
        self.wallet = Wallet(balance)
        self.count = count
        self.distributedBalance = self.wallet.balance() // self.count
        self.runningTMS = []
        self.strategies = []
        self.running = False

    def start(self):
        """Starts the bot and creates the COUNT number of transaction mangers."""
        self.running = True
        for i in range(self.count):
            self.createTM(i, self.balance(), self.strategy())
        for transactor in self.runningTMS:
            transactor.start()
        while self.running:
            self.update()
            sleep(_delay)

    def update(self):
        """Instructs each of the running TMs to update."""
        btcprice = price()
        for transactor in self.runningTMS:
            if transactor.negative():
                ID = transactor.identifier()
                self.destroyTM(transactor, btcprice)
                self.createTM(ID, self.balance(), self.strategy())
            else:
                transactor.update(btcprice)

    def stop(self):
        """Stops the bot and destroys all transaction managers."""
        self.running = False
        btcprice = price()
        for transactor in self.runningTMS:
            self.destroyTM(transactor, btcprice)

    ##########
    # Status #
    ##########

    def status(self):
        """Gets the current status of the transaction managers in this bot."""
        btcprice = price()
        table = Texttable()
        table.set_cols_align(['c', 'c'])
        table.set_cols_valign(['m', 'm'])
        table.header(['Current Balance', 'BTC Price'])
        table.add_row(['$' + str((self.value(btcprice))[0]), str(btcprice)])
        print table.draw()

        t = Texttable()
        t.set_cols_align(['c', 'c', 'c', 'c'])
        t.set_cols_valign(['m', 'm', 'm', 'm'])
        t.header(['TM ID', 'Status', 'Balance', 'Strategy'])
        for transactor in self.runningTMS:
            item = []
            item.append(str(transactor.identifier))
            item.append(str(transactor.status(btcprice)))
            item.append('$' + str(transactor.value(btcprice)))
            item.append(str(float(transactor.currstrategy()*100)) + '%')
            t.add_row(item)
        print t.draw()

    def value(self, p=price()):
        """Gets the aggregate value in USD of the bot by getting the value in
        each of the transaction managers."""
        total = []
        if self.running:
            value = 0
            usd = 0
            btc = 0
            for transactor in self.runningTMS:
                value += transactor.value(p)
                usd += transactor.usd.balance()
                btc += transactor.btc.balance()
            value += self.wallet.balance()
            usd += self.wallet.balance()
            total.append(value)
            total.append(usd)
            total.append(btc)
            return total
        return self.wallet.balance()

    def log(self):
        total = []
        for transactor in self.runningTMS:
            total.append(transactor.getLog())
        return total

    ##########################
    # Transaction Management #
    ##########################

    def createTM(self, identifier, balance, strategy):
        """Creates a new transaction manager."""
        transactor = TransactionManager(identifier, balance, strategy)
        self.runningTMS.append(transactor)
        self.wallet.subtract(balance)

    def balance(self):
        """Distributes the balance evenly among transaction managers."""
        if self.wallet.hasFunds(self.distributedBalance):
            return self.distributedBalance

    def strategy(self):
        """Creates a new strategy that is not current being used."""
        strategy = float(randint(1, 10))
        strategy = strategy / 1000
        if strategy not in self.strategies:
            self.strategies.append(strategy)
            return strategy
        return self.strategy()

    def destroyTM(self, transactor, btcprice):
        """Destroys a transaction manager and reintegrates the 
        transaction manager's wallet with the bot's wallet."""
        transactor.stop(btcprice)
        self.runningTMS.remove(transactor)
        self.wallet.add(transactor.usd.balance())

    def insufficientFunds(self):
        print "You've run out of funds, I'm afraid. Try using the leftover balance in your account."

    def userBuy(self, amount):
        """ A method called when the user requests a purchase manually. """
        funds = True
        for transactor in self.runningTMS:
            if not transactor.usd.hasFunds(amount):
                funds = False
        if funds:
            btcprice = price()
            for transactor in self.runningTMS:
                transactor.buy(amount, btcprice)
        else:
            self.insufficientFunds()
                
























    # def whatIDShouldIMake(self):
    # 	currentIDs = []
    # 	possibleIDs = []
    # 	for possible_num in range(TMcount):
    # 		for running_TM in running_TMs:
    # 			if running_TM.identifier() == possible_num:
    # 				continue
    # 			possibleIDs += possible_num

    # 	for tm in running_TMs:
    # 		currentIDs += tm.identifier()
        # now have list of all running TM #s
