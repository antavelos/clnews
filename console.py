
import re
import json

from colorama import init as colorama_init, Fore, Back, Style

from news import *
from exception import *
import config

COMMANDS = {
    '.help': ('.help', 'show this help message and exit'),
    '.list': ('.list', 'lists all the available channels'), 
    '.get': ('.get', 'retrieves the news of a given channel, e.g.: .get cnn')
}

class Command(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.buffer = None

    def execute(self):
        pass

    def print_output(self):
        pass


class CommandHelp(Command):

    def __init__(self):
        name, description = COMMANDS['.help']
        super(CommandHelp, self).__init__(name, description)

    def execute(self):
        '''
        Print the help message
        '''
        self.buffer = "CLI News %s \n\n" % config.VERSION
        self.buffer += "Options:\n"

        keys = COMMANDS.keys()
        for key in keys:
            self.buffer += "\t%10s\t%s\n" % (COMMANDS[key][0], COMMANDS[key][1])
        self.buffer += "\n"

    def print_output(self):
        print self.buffer


class CommandList(Command):

    def __init__(self):
        name, description = COMMANDS['.list']
        super(CommandList, self).__init__(name, description)

    def execute(self):
        '''
        List all the available channels
        '''
        self.buffer = [(ch, config.CHANNELS[ch]["name"]) 
                       for ch 
                       in config.CHANNELS.keys()]

    def print_output(self):
        for i, (short, name) in enumerate(self.buffer):
            print "%3d. %10s [%s]" % (i, name, short)


class CommandGet(Command):

    def __init__(self, channel_name, channel_url):
        name, description = COMMANDS['.get']
        super(CommandGet, self).__init__(name, description)
        self.channel_name = channel_name
        self.channel_url = channel_url

    def execute(self):
        '''
        Retrieve the events for the given channel
        '''
        ch = Channel(self.channel_name, self.channel_url)

        try:
            self.buffer = ch.get_events()
        except ChannelRetrieveEventsError:
            self.buffer = 'There was an error while retrieving the events.'

    def print_output(self):
        if isinstance(self.buffer, list):
            for i, event in enumerate(self.buffer):
                print "%3s. %s, %s\n     %s\n     %s\n" % \
                    (Fore.WHITE + Style.BRIGHT + str(i + 1), 
                     event.title, 
                     Fore.MAGENTA + event.date, 
                     Fore.WHITE + Style.DIM + event.url, 
                     Fore.YELLOW + Style.NORMAL + event.summary)
            
            print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        else:
            print self.buffer
    
class Console(object):

    def __init__(self):
        self.command = None
        colorama_init()

    def _prompt(self, text):
        return raw_input(text)

    def _analyse_input(self, input):
        '''
        Analyse the user input per command
        '''
        if 'quit' == input:
            raise EOFError

        tokens = input.split()
        first = tokens[0]

        if first not in COMMANDS.keys():
            raise ConsoleCommandDoesNotExist

        if first == '.help':
            self.command = CommandHelp()

        if first == '.list':
            self.command = CommandList()

        if first == '.get':
            if len(tokens) < 2:
                raise ConsoleCommandChannelNotFound
            
            if tokens[1] not in config.CHANNELS.keys():
                raise ConsoleCommandChannelNotFound

            channel = config.CHANNELS[tokens[1]]
            self.command = CommandGet(channel['name'], channel['url'])

        return self.command

    def run(self):
        '''
        Infinite loop for the command line
        '''
        print "CLI News %s \n" % config.VERSION
        command = Command('name', 'description')
        while True:
            try:
                input = self._prompt("news> ")
                command = self._analyse_input(input)
            except EOFError:
                print 
                exit()
            except ConsoleCommandDoesNotExist, e:
                print str(e), 'Use .help to see the available options'
            except ConsoleCommandChannelNotFound:
                print ('The channel was not found. ' 
                       'Use .list to see the available ones.')

            command.execute()
            command.print_output()
