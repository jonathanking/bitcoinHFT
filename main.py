import cmd
import json
import requests
import threading
import urllib

from bot import *
from texttable import Texttable
from wallet import *

FEE = 0.000
_apiURL = "https://www.okcoin.com/api/ticker.do?ok=1"

def price():
    url = _apiURL
    r = requests.get(url)
    j = r.json()
    return float(j['ticker']['last'])
    # return float(getTicker('btc_usd').last)

def ticker():
    url = _apiURL
    r = requests.get(url)
    j = r.json()
    return j
    # return getTicker('btc_usd')

class colors:
    """ A list of ANSI coded colors for use in the terminal.
            Ex: print colors.WARNING + "IMMINENT FAILURE IS IMMINENT" +
            colors.ENDC.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

_botColor = colors.OKBLUE
_goodColor = colors.OKGREEN
_badColor = colors.FAIL
_simColor = colors.OKBLUE
_liveColor = colors.OKBLUE
_neutralColor = colors.WARNING
_endColor = colors.ENDC


class Main(cmd.Cmd, object):
    t = None
    bot = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.running = False
        self.prompt = _botColor + "Bot> " + _endColor
        self.bot = None
        self.simulation_balance = 100000.0
        self.live_balance = 100000.0
        self.simulation = True

    def do_start(self, arg):
        """Starts the trading bot."""
        if self.running:
            print 'Trading bot is already running.'
        else:
            if arg == "live":
                self.prompt = _liveColor + "Live> " + _endColor
                self.simulation = False
                self.bot = Bot(True, self.live_balance, 4)
            else:
                self.prompt = _simColor + "Simulation> " + _endColor
                self.bot = Bot(False, self.simulation_balance, 4)

            self.t = threading.Thread(target=self.bot.start)
            self.t.start()
            self.running = True
            print _goodColor + 'Trading bot is now running.' + _endColor

    def do_status(self, arg):
        """Get the current status of the Transaction Managers in our bot"""
        if self.running:
            self.bot.status()
        else:
            print 'Trading bot is not running.'

    def do_stop(self, arg):
        """Stops the trading bot."""
        self.bot.stop()
        if self.simulation:
            self.simulation_balance = self.bot.value()
        else:
            self.live_balance = self.bot.value()

        self.prompt = _botColor + "Bot> " + _endColor
        self.running = False
        self.simulation = True
        print _badColor + 'Trading bot is now stopped.' + _endColor

    def do_balance(self, arg):
        """When trading bot is running, the current USD and BTC balance is returned.
           Otherwise, returns the current USD balance."""
        if self.running:
            total = self.bot.value()
            print 'Total Balance (Converted to USD): $' + str(total[0])
            print 'USD Balance: $' + str(total[1])
            print 'BTC Balance: ' + str(total[2])
        else:
            if self.simulation:
                print 'Current Balance: $' + str(self.simulation_balance)
            else:
                print 'Current Balance: $' + str(self.live_balance)

    def do_log(self, arg):
        if self.running:
            t = Texttable()
            t.header(['ID', 'Initial Time', 'Final Time', 'BTC Amount', 'Initial BTC Price', 'Final BTC Price', 'Initial USD Balance', 'Final USD Balance'])

            log = self.bot.log()
            for i in log:
                for j in i:
                    item = []
                    for k in j:
                        item.append(str(k))
                    t.add_row(item)
            print t.draw()
        else:
            print 'Trading bot is not running.'

    def do_price(self, arg):
        """Returns the current price of 1 bitcoin in USD."""
        print 'BTC to USD Price: ' + str(price())

    def do_market(self, arg):
        """Returns the current market data about bitcoins."""

        print 'Market Data: Some numbers here, some numbers there, numbers, numbers everywhere!'

    def do_buy(self, arg):
        """ Instructs the bot to purchase ARG (USD) amount of BTC. """
        if arg:
            if self.running:
                self.bot.userBuy(float(arg))
            else:
                print 'Trading bot is not running.'
        else:
            print 'Purchase amount not specified.'

    def preloop(self):
        f = open('Data/welcome.txt', 'r')
        f2 = open('Data/art.txt', 'r')
        print f2.read()
        print f.read()
        super(Main, self).preloop()

    def emptyline(self):
        pass

    def postloop(self):
        print 'Goodbye!'
        super(Main, self).postloop()

    def do_quit(self, arg):
        """Quit the trading system."""
        if self.running:
            self.do_stop(0)
        return True

    """Shortcut for quitting the program"""
    do_q = do_quit
    do_exit = do_quit

if __name__ == '__main__':
    console = Main()
    console.cmdloop()
