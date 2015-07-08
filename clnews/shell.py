"""
.. module:: shell
   :platform: Unix
      :synopsis: This module contains the shell functionality of clnews.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """
import sys
import readline

from colorama import init as colorama_init

from clnews import config
from clnews.commands import Command
from clnews.exceptions import CommandExecutionError, CommandIOError

reload(sys)
sys.setdefaultencoding("utf-8")


class Shell(object):
    """ Implements the shell functionality."""

    def __init__(self):
        """ Initializes the class."""

        colorama_init()
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        self.history = []
        self.commands = dict({(klass.__dict__['name'], klass())
                              for klass in Command.__subclasses__()})


    def _prompt(self, text):
        sys.stdin.flush()
        inp = raw_input(text)
        self.history.append(inp)

        return inp

    def _analyse_input(self, user_input):
        if '.quit' == user_input:
            raise EOFError

        tokens = user_input.split()
        try:
            command = self.commands[tokens[0]]
        except KeyError:
            raise CommandExecutionError('Command not found.\n')

        return command, tokens[1:]

    def __call__(self):
        """ Runs infinitely executing the commands given in input."""

        print "CLNews %s \n" % config.VERSION
        while True:
            try:
                user_input = self._prompt("news> ")
                if user_input:
                    command, arguments = self._analyse_input(user_input)
            except (EOFError, KeyboardInterrupt):
                print
                break
            except CommandExecutionError, exc:
                print str(exc), 'Use .help to see the available options.'
                continue
            except CommandChannelNotFound, exc:
                print exc.message + 'Use .list to see the available ones.'
                continue

            try:
                command.execute(*arguments)
                command.print_output()
            except CommandExecutionError as error:
                print "An error occured while executing the command.\n" \
                      + error.message
                continue
            except CommandIOError as error:
                print "An error occured while printing output.\n" \
                      + error.message
                continue

def main():
    """ Entry point
    """
    Shell()()
