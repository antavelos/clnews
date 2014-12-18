#!/usr/bin/env python

import unittest
import datetime
import os

from news import * 
from console import *
from exception import *


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
        self.assertRaises(ChannelDataNotFound, self.channel._get_data)

    def test_get_events(self):
        events = self.channel.get_events()
        self.assertTrue(isinstance(events, list))
        self.assertTrue(isinstance(events[0], Event))
        self.assertEqual(str(events[0]), "%s, %s" % (events[0].title, 
                         events[0].url))


class TestConsole(unittest.TestCase):

    def setUp(self):
        self.console = Console()

    def test_config_file(self):
        # file does not exist
        self.assertRaises(ConsoleConfigFileDoesNotExist, 
                          self.console._load_config, 'not_existent')
        
        # bad json format
        with open('temp.json', 'w') as f:
            f.write('{"name":"value"')
            f.close()

        self.assertRaises(ConsoleConfigFileFormatError, 
                          self.console._load_config, 'temp.json')
        os.remove('temp.json')
        
        data = self.console._load_config('config.json')
        self.assertTrue(isinstance(data, dict))

    def test_list_channels(self):
        data = self.console._list()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(isinstance(data[0], tuple))

        channels = self.console.config["channels"]
        keys = channels.keys()
        self.assertEqual(data, [(ch, channels[ch]["name"]) for ch in keys])

    def test_get_channel_events(self):
        channel_name = 'cnn'
        channel_url = 'http://rss.cnn.com/rss/edition_world.rss'
        ch = Channel(channel_name, channel_url)

        events = ch.get_events()
        get_events = self.console._get(channel_name, channel_url)
        self.assertEqual(len(events), len(get_events))

    def test_analyse_input(self):
        # command does not exist
        
        self.assertRaises(ConsoleCommandDoesNotExist, 
                          self.console._analyse_input, 'false_command')

        # test .help command
        self.assertEqual(self.console._analyse_input('.help'), 
                         self.console._help())

        # test .list command
        self.assertEqual(self.console._analyse_input('.list'), 
                         self.console._list())

        # test .get with few options
        self.assertRaises(ConsoleCommandChannelNotFound, 
                          self.console._analyse_input, '.get')

        # test .get with not available channel
        self.assertRaises(ConsoleCommandChannelNotFound, 
                          self.console._analyse_input, '.get false_channel')

        channel_name = 'cnn'
        channel_url = 'http://rss.cnn.com/rss/edition_world.rss'
        events = self.console._get(channel_name, channel_url)
        get_events = self.console._analyse_input('.get cnn')
        self.assertEqual(len(events), len(get_events))


if __name__ == '__main__':
    unittest.main()
