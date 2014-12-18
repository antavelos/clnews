import re
import json

import config
from news import *
from exception import *

class Console(object):

    def __init__(self):
        self.commands = [
            ('.help', 'show this help message and exit'), 
            ('.list', 'lists all the available channels'), 
            ('.get', 'retrieves the news of a given channel, e.g.: .get cnn')
        ]

        try:
            self.config = self._load_config('config.json')
        except ConsoleConfigFileDoesNotExist, e:
            print str(e) + "\nExiting..."
        except ConsoleConfigFileFormatError, e:
            print str(e) + "\nExiting..."

    def _load_config(self, filename):
        '''
        Load the config file contains into a dictionary
        '''

        data = {}
        try:
            with open(filename, 'r') as f:
                json_data = f.read()
            f.close()
            data = json.loads(json_data)
        except IOError:
            raise ConsoleConfigFileDoesNotExist
        except ValueError, e:
            raise ConsoleConfigFileFormatError

        return data


    def _prompt(self, text):
        return raw_input(text)

    def _help(self):
        '''
        Print the help message
        '''

        str = "CLI News (%s) \n" % self.config['version']
        str += "Options:"
        for com in commands:
            str += "\t%10s\t%s\n" %(com[0], com[1])
        str += "\n"

        return str

    def _list(self):
        '''
        List all the available channels
        '''
        channels = self.config['channels']
        keys = channels.keys()

        return [(ch, channels[ch]["name"]) for ch in keys]

    def _get(self, channel):
        '''
        Retrieve the events for the given channel
        '''

        ch = channel(channel['name'], channel['url'])

        return ch.get_events()

    def _analyse_input(self, input):
        '''
        Analyse the user input per command
        '''

        tokens = input.split()
        first = tokens[0]

        if first not in self.commands:
            raise ConsoleCommandDoesNotExist

        if first == '.help':
            return self._help()

        if first == '.list':
            channels_list = self._list()
            for ch, name in channels_list:
                print "%10s   %s" % (ch, name)

        if first == '.get':
            if len(tokens) < 2:
                raise ConsoleCommandChannelNotFound

            channels = [ch.keys[0] for ch, url in self.config['channels']]
            if tokens[1] not in channels:
                raise ConsoleCommandChannelNotFound

            return self._get(tokens[1])


    def run(self):
        '''
        Infinite loop for the command line
        '''
        while True:
            input = self._prompt("news>")
            try:
                output = self._analyse_input(input)
                print output
            except ConsoleCommandDoesNotExist, e:
                print str(e), 'Press .help to see the available options'


