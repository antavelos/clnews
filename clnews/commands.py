"""
.. module:: commands
   :platform: Unix
      :synopsis: This module contains the commands being used in shell.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """

from colorama import Fore, Style

from clnews import config
from clnews.news import Channel
from clnews.decorators import less
from clnews.utils import DataFile, validate_url
from clnews.exceptions import  CommandIOError, ChannelRetrieveEventsError, \
CommandExecutionError


class Command(object):
    """ Abstract class implementing the shell commands.

    It implements the basic functionality of the shell commands and serves as a
    parent class.
    """
    name = None
    description = None
    options = ''
    data = {'channels': {}}

    def __init__(self):
        """Initializes of the command."""

        # saves the output of the command
        self.buffer = None
        self.data_file = DataFile(config.CHANNELS_PATH)
        if not Command.data:
            Command.data = self.data_file.load()


    def execute(self, *args):
        """ Parent function
        """
        raise NotImplementedError

    def print_output(self):
        """ Prints the output of the command"""
        print self.buffer

    @classmethod
    def code_exists(cls, code):
        return code in cls.data['channels']

    @classmethod
    def url_exists(cls, url):
        return url in [val['url'] for val in cls.data['channels'].values()]

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
        command_classes = Command.__subclasses__()
        self.buffer = "CLNews %s \n\n" % config.VERSION
        self.buffer += "Options:\n"

        for klass in command_classes:
            name = klass.__dict__.get('name')
            description = klass.__dict__.get('description')
            options = klass.__dict__.get('options')
            self.buffer += "\t%10s\t%s\n" % (name, description)
            if options:
                self.buffer += "\t%s\toptions: %s\n\n" % (' '*10, options)
            else:
                self.buffer += '\n'
        self.buffer += "\n"


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
        self.buffer = ''
        if Command.data:
            self.buffer = [(key, data["name"])
                           for key, data
                           in Command.data["channels"].iteritems()]

    @less
    def print_output(self):
        """ Prints the output of the command

        Raises:
            CommandIOError: An error occured when the buffer is not a
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
            raise CommandIOError


class Get(Command):
    """ Implements the .get command.

    Derives from :class:`shell.Command` class and implements the .get command
    """

    name = ".get"
    description = "retrieves the news of a given channel"
    options = '[channel_code]'

    def execute(self, *args):
        """ Executes the command.

        Retrieves the events for the given channel.

        Raises:
            CommandExecutionError
        """
        if not Command.data:
            raise CommandExecutionError("You channels' list is empty.")

        if len(args) != 1:
            raise CommandExecutionError('Check the provided arguments.')

        channel_code = args[0]
        if channel_code not in Command.data['channels'].keys():
            raise CommandExecutionError("Channel not found.")

        name = Command.data['channels'][channel_code]['name']
        url = Command.data['channels'][channel_code]['url']

        channel = Channel(name, url)

        try:
            self.buffer = channel.get_events()
        except ChannelRetrieveEventsError:
            raise CommandExecutionError("Error while retrieving data.")

    @less
    def print_output(self):
        """ Prints the output of the command

        Raises:
            CommandIOError: An error occured when the buffer is not a
            list.
        """
        try:
            output = ["%3s. %s, %s\n     %s\n     %s\n" %
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
            raise CommandIOError


class Quit(Command):
    """ Implements the .get command.

    Derives from :class:`shell.Command` class and implements the .quit command
    """

    name = ".quit"
    description = "exits the application."


class Add(Command):
    """ Implements the .add command.

    Derives from :class:`shell.Command` class and implements the .add command
    """

    name = ".add"
    description = "adds a new channel."
    options = '[channel_code] [channel_name] [url]'

    def execute(self, *args):
        try:
            code, name, url = args
        except ValueError:
            msg = 'Commmand .add requires exactly 3 arguments: ' \
                  '[channel_code], [channel_name], [url]'
            raise CommandExecutionError(msg)

        if Command.code_exists(code):
            msg = 'This code already exists in your list.'
            raise CommandExecutionError(msg)

        if Command.url_exists(url):
            msg = 'This URL already exists in your list.'
            raise CommandExecutionError(msg)

        if not validate_url(url):
            raise CommandExecutionError('URL is either not valid or broken')

        channel = {code: {'name': name, 'url': url}}
        if 'channels' in Command.data:
            Command.data['channels'].update(channel)
        else:
            Command.data['channels'] = channel
        self.data_file.save(Command.data)
        self.buffer = 'The RSS URL was added in your list.'


class Remove(Command):
    """ Implements the .remove command.

    Derives from :class:`shell.Command` class and implements the .remove command
    """

    name = ".remove"
    description = "adds one or more channels from the list."
    options = '[channel_code]...'

    def execute(self, *args):

        if not args:
            raise CommandExecutionError('No channel code was provided.')

        # remove all
        if len(args) == 1 and args[0] == '*':
            Command.data = {}
            self.data_file.save(Command.data)
            self.buffer = 'All the channels were removed from your list.'
            return

        data_copy = dict(Command.data)
        channel_codes = data_copy['channels'].keys()
        for arg in args:
            if arg in channel_codes:
                del data_copy['channels'][arg]
            else:
                msg = 'Channel %s was not found in your list' % arg
                raise CommandExecutionError(msg)
        self.data_file.save(data_copy)
        self.buffer = 'The channel(s) were removed from your list.'
