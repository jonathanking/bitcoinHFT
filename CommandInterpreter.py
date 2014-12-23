import cmd
import sys

from blockchain import exchangerates

class CommandInterpreter(cmd.Cmd):
    """A command interpreter that reads and interprets a command
    from the input.
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '

    def do_balance(self, arg):
        """Returns the current balance of our bitcoin wallet."""
        print 'Balance: '

    def do_price(self, arg):
        """Returns the current price of 1 bitcoin in USD."""
        ticker = exchangerates.get_ticker()
        for curr in ticker:
            if arg:
                if curr == arg:
                    price = ticker[curr].p15min
            else:
                if curr == 'USD':
                    price = ticker[curr].p15min
        print 'BTC Price: ' + str(price)
    
    def do_start(self, arg):
        """Starts the trading bot."""
        print 'Starting the trading bot:'

    def do_stop(self, arg):
        """Stops the trading bot."""
        print 'Stopping the trading bot:'

    def do_market(self, arg):
        """Returns the current market data about bitcoins."""
        print 'Market Data: '

    def do_quit(self, arg):
        """Quit the trading system."""
        return True

    """Shortcut for quitting the program"""
    do_q = do_quit

CommandInterpreter().cmdloop()