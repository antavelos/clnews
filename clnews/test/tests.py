#!/usr/bin/env python

import unittest
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))

from clnews.exceptions import *
from clnews.news import Event, Channel
from clnews.shell import Shell
from clnews.utils import remove_html, validate_url
from clnews.commands import Command, Get, Add, Help, List, Remove

Command()
Command.data['channels'] = {}

class TestUtils(unittest.TestCase):

    def test_remove_html(self):
        html = '<div class"class">test test test<img src="src"/></div>'
        output = remove_html(html)
        self.assertEqual(output, 'test test test')

class TestNews(unittest.TestCase):

    def setUp(self):
        self.url = 'http://rss.cnn.com/rss/edition_world.rss'
        self.channel = Channel('cnn', self.url)
        self.event = Event('title', 'url', datetime.datetime.now())

    # test Event
    def test_event_object(self):
        # invalid date
        # event = Event('title', 'url', 'string date')

        self.assertEqual(str(self.event), "%s, %s" % (self.event.title,
                                                      self.event.url))

    # test Channel
    def test__get_data(self):
        data = self.channel._get_data()
        self.assertTrue(isinstance(data, list))

        # corrupted url
        self.channel.url = self.url[:-15]
        with self.assertRaises(ChannelDataNotFound):
            self.channel._get_data()

    def test_get_events(self):
        events = self.channel.get_events()
        self.assertTrue(isinstance(events, list))
        self.assertTrue(isinstance(events[0], Event))
        self.assertEqual(str(events[0]), "%s, %s" % (events[0].title,
                                                     events[0].url))


class TestListCommand(unittest.TestCase):
    def setUp(self):
        name = 'cnn'
        url = 'http://rss.cnn.com/rss/edition_world.rss'
        Command.data['channels'].update({'cnn': {'name': name, 'url': url}})

    def test_command_list(self):
        command = List()
        command.execute()
        self.assertTrue(isinstance(command.buffer, list))
        self.assertTrue(isinstance(command.buffer[0], tuple))

        channels = Command.data['channels']
        keys = channels.keys()
        self.assertEqual(command.buffer,
                         [(ch, channels[ch]["name"]) for ch in keys])


class TestGetCommand(unittest.TestCase):

    def setUp(self):
        self.name = 'cnn'
        self.url = 'http://rss.cnn.com/rss/edition_world.rss'
        Command.data['channels'].update({'cnn': {'name': self.name,
                                                 'url': self.url}})
    def test_command_get(self):

        ch = Channel(self.name, self.url)
        command = Get()

        # happy case
        events = ch.get_events()
        command.execute(self.name)
        self.assertEqual(len(events), len(command.buffer))

        # no channel given
        with self.assertRaises(CommandExecutionError):
            command.execute()

        # too many arguments
        with self.assertRaises(CommandExecutionError):
            command.execute()

        # channel does not exist
        with self.assertRaises(CommandExecutionError):
            command.execute('bbc')

        # empty list
        with self.assertRaises(CommandExecutionError):
            Command.data['channels'] = {}
            command.execute(self.name)

class TestAddCommand(unittest.TestCase):

    def setUp(self):
        self.code = 'cnn'
        self.name = 'CNN'
        self.url = 'http://rss.cnn.com/rss/edition_world.rss'
        Command.data['channels'].update({self.code: {'name': self.name,
                                                     'url': self.url}})

    def test_command_get(self):
        command = Add()

        # too few arguments
        with self.assertRaises(CommandExecutionError):
            command.execute(self.code, self.name)

        # too many arguments
        with self.assertRaises(CommandExecutionError):
            command.execute(self.code, self.name, self.url, self.url)

        # same code exists
        with self.assertRaises(CommandExecutionError):
            command.execute(self.code, self.name, self.url)

        # same url exists
        with self.assertRaises(CommandExecutionError):
            command.execute('bbc', self.name, self.url)

        # invalid URL
        with self.assertRaises(CommandExecutionError):
            url = 'rss.cnn.com/rss/edition_world.rss'
            command.execute('bbc', self.name, url)

        # broken URL
        with self.assertRaises(CommandExecutionError):
            url = 'http://rss.cnn.com/rss/edition_worl'
            command.execute('bbc', self.name, url)

        code = 'asia'
        name = 'Asia'
        url = 'http://rss.cnn.com/rss/edition_asia.rss'
        command.execute(code, name, url)
        self.assertTrue(code in Command.data['channels'].keys())


class TestRemoveCommand(unittest.TestCase):

    def setUp(self):
        self.code = 'cnn'
        self.name = 'CNN'
        self.url = 'http://rss.cnn.com/rss/edition_world.rss'
        Command.data['channels'].update({self.code: {'name': self.name,
                                                     'url': self.url}})
        self.code1 = 'asia'
        self.name1 = 'Asia'
        self.url1 = 'http://rss.cnn.com/rss/edition_asia.rss'
        Command.data['channels'].update({self.code1: {'name': self.name1,
                                                      'url': self.url1}})
        self.code2 = 'africa'
        self.name2 = 'Africa'
        self.url2 = 'http://rss.cnn.com/rss/edition_africa.rss'
        Command.data['channels'].update({self.code2: {'name': self.name2,
                                                      'url': self.url2}})
        command = Remove()

        # 0 arguments
        with self.assertRaises(CommandExecutionError):
            command.execute()

        # wrong channel code in the list
        with self.assertRaises(CommandExecutionError):
            command.execute(self.code, 'false_code')

        command.execute(self.code)
        self.assertEqual(Command.data['channels'].keys(), [self.code1,
                                                           self.code2])

        command.execute('*')
        self.assertEqual(Command.data['channels'].keys(), [])

# class TestShell(unittest.TestCase):

#     def setUp(self):
#         self.shell = Shell()

#     def test_analyse_input(self):
#         # command does not exist

#         self.assertRaises(CommandIOError,
#                           self.shell._analyse_input, 'false command')

#         # test .help command
#         output = self.shell._analyse_input('.help')
#         self.assertTrue(isinstance(output, Help))

#         # test .list command
#         output = self.shell._analyse_input('.list')
#         self.assertTrue(isinstance(output, List))

#         # test .get with not available channel
#         self.assertRaises(CommandChannelNotFound,
#                           self.shell._analyse_input, '.get false_channel')


if __name__ == '__main__':
    unittest.main()
