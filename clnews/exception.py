"""
.. module:: exception
   :platform: Unix
      :synopsis: This module contains the exceptions of the modules.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """
# Event Exceptions
class EventAttrError(Exception):
    """Is raised when a wrong attribute type is given in an Event
    initialization

    """


# Channel Exceptions
class ChannelDataNotFound(Exception):
    """ Is raised when no data is retrieved from feedparser."""

class ChannelServerError(Exception):
    """ Is raised when feedparser returns a server error."""

class ChannelRetrieveEventsError(Exception):
    """ Is raised when an uncaught exception occurs during events' retrieval."""


# Shell Exceptions
class ShellLoadDataIOError(Exception):
    """ Is raised when the data file is not found"""

class ShellLoadDataCorruptedFile(Exception):
    """ Is raised when the data file is corrupted"""

class CommandDoesNotExist(Exception):
    """ Is raised when an unknown command is given in input prompt."""

class CommandChannelNotFound(Exception):
    """ Is raised when events from an unknown channel are requested."""

class CommandExecutionError(Exception):
    """ IS raised when an error occurs while executing a command."""

class CommandOutputError(Exception):
    """ Is raised when output is not of the expected type."""


# Data structure exceptions
class StackEmptyError(Exception):
    """ Is raised when a stack is empty"""
