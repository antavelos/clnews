"""
.. module:: commands
   :platform: Unix
      :synopsis: This module contains the commands being used in shell.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """

import pickle

from colorama import Fore, Style

from clnews import config
from clnews.news import Channel
from clnews.decorators import less
from clnews.exception import ShellLoadDataIOError, ShellLoadDataCorruptedFile, \
ShellCommandOutputError, ChannelRetrieveEventsError, ShellCommandDoesNotExist, \
ShellCommandChannelNotFound


class Command(object):
    """ Abstract class implementing the shell commands.

    It implements the basic functionality of the shell commands and serves as a
    parent class.
    """
    name = None
    description = None
    data = None

    def __init__(self):
        """Initializes of the command."""

        # saves the output of the command
        self.buffer = None
        if self.data is None:
            self.data = self._load_data()

    def _load_data(self):
        try:
            self.data = pickle.load(open(config.CHANNELS_PATH, "rb"))
        except IOError:
            raise ShellLoadDataIOError
        except KeyError:
            raise ShellLoadDataCorruptedFile
        else:
            return self.data


    @classmethod
    def get_commands_data(cls):
        return [(cls.__dict__['name'], cls.__dict__['description'])
                for cls in Command.__subclasses__()]


    def execute(self, *args):
        """ Parent function
        """
        raise NotImplementedError

    def print_output(self):
        """ Parent function
        """
        raise NotImplementedError


class Help(Command):
    """ Implements the .help command.

    Derives from :class:`shell.Command` class and implements the .help command
    """

    name = ".help"
    description = "show this help message and exit"

    def execute(self, *args):
        """ Executes the command.

        Puts in the buffer the output of the command
        """

        self.buffer = "CLNews %s \n\n" % config.VERSION
        self.buffer += "Options:\n"

        for (name, description) in Command.get_commands_data():
            self.buffer += "\t%10s\t%s\n" % (name, description)
        self.buffer += "\n"

    def print_output(self):
        """ Prints the output of the command"""
        print self.buffer


class List(Command):
    """ Implements the .list command.

    Derives from :class:`shell.Command` class and implements the .list command
    """

    name = ".list"
    description = "lists all the available channels"

    def execute(self, *args):
        ''' Executes the command.

        Lists all the available channels.
        '''
        self.buffer = [(key, data["name"])
                       for key, data
                       in self.data["channels"].iteritems()]

    @less
    def print_output(self):
        """ Prints the output of the command

        Raises:
            ShellCommandOutputError: An error occured when the buffer is not a
            list.
        """
        try:
            output = ["%s| Name %s| Code" % (5 * " ", 15 * " "),
                      "%s+%s+%s" % (5 * "-", 21 * "-", 20 * "-")]
            output += ["%5s|%20s | %s" % (str(i + 1), name, short)
                       for i, (short, name)
                       in enumerate(self.buffer)]

            return "\n".join(output)
        except TypeError:
            # the buffer is not a list as expected
            raise ShellCommandOutputError


class Get(Command):
    """ Implements the .get command.

    Derives from :class:`shell.Command` class and implements the .get command
    """

    name = ".get"
    description = "retrieves the news of a given channel, e.g.: .get cnn"

    def execute(self, *args):
        """ Executes the command.

        Retrieves the events for the given channel.

        Raises:
            ShellCommandExecutionError: An error occured when the event
            retrieval fails.
        """
        if len(args) > 1:
            raise ShellCommandDoesNotExist

        channel_code = args[0]
        if channel_code not in self.data['channels'].keys():
            raise ShellCommandChannelNotFound

        name = self.data['channels'][channel_code]['name']
        url = self.data['channels'][channel_code]['url']

        channel = Channel(name, url)

        try:
            self.buffer = channel.get_events()
        except ChannelRetrieveEventsError:
            raise ShellCommandOutputError

    @less
    def print_output(self):
        """ Prints the output of the command

        Raises:
            ShellCommandOutputError: An error occured when the buffer is not a
            list.
        """
        try:
            output = ["%3s. %s, %s\n     %s\n     %s\n" % \
                      (Fore.WHITE + Style.BRIGHT + str(i + 1), event.title,
                       Fore.MAGENTA + event.date,
                       Fore.WHITE + Style.DIM + event.url,
                       Fore.YELLOW + Style.NORMAL + event.summary)
                      for i, event
                      in enumerate(self.buffer)
                     ]

            return "\n".join(output)

        except TypeError:
            # the buffer is not a list as expected
            raise ShellCommandOutputError


class Quit(Command):
    """ Implements the .get command.

    Derives from :class:`shell.Command` class and implements the .get command
    """

    name = ".quit"
    description = "exits the application."


def get_command_by_input(input):
    name = input[0]
    arguments = input[1:]
    for klass in Command.__subclasses__():
        if klass.__dict__['name'] == name:
            return klass(*arguments)

    return None
