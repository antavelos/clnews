#!/usr/bin/env python

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

        str = "CLI News (%s) \n\n" % self.config['version']
        str += "Options:\n"
        for com in self.commands:
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

    def _print_channels_list(self, channels_list):
        '''
        Print the list of available channels
        '''
        for ch, name in channels_list:
            print "%10s   %s" % (ch, name)
        
        
    def _get(self, channel_name, channel_url):
        '''
        Retrieve the events for the given channel
        '''
        ch = Channel(channel_name, channel_url)

        return ch.get_events()

    def _analyse_input(self, input):
        '''
        Analyse the user input per command
        '''

        tokens = input.split()
        first = tokens[0]

        if first not in [ com for com, desc in self.commands]:
            raise ConsoleCommandDoesNotExist

        if first == '.help':
            return self._help()

        if first == '.list':
            return  self._list()            

        if first == '.get':
            if len(tokens) < 2:
                raise ConsoleCommandChannelNotFound

            channels = self.config['channels'].keys()
            if tokens[1] not in channels:
                raise ConsoleCommandChannelNotFound

            channel = self.config['channels'][tokens[1]]
            
            return self._get(channel['name'],
                             channel['url'])


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


if __name__ == '__main__':
    c = Console()
    c.run()