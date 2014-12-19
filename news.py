import re
import datetime
import feedparser

from exception import *

class Event(object):

	def __init__(self, title, url, date, summary=''):
		self.title = title
		self.url = url
		self.date = date
		self.summary = self._remove_html(summary)

	def _remove_html(self, str):
		p = re.compile(r'<.*?>')
		str = p.sub('', str)
		
		return str

	def __repr__(self):
		return "%s, %s" % (self.title, self.url)

class Channel(object):

	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.events = []

	def _get_data(self):
		response = feedparser.parse(self.url)

		if response.status == 200:
			pass
		elif response.status == 404:
			raise ChannelDataNotFound
		else:
			raise ChannelServerError

		return response.entries

	def get_events(self):
		event_entries = self._get_data()
		
		try:
			self.events = [Event(e.title, e.link, e.published, e.summary) 
						   for e 
						   in event_entries]
		except TypeError:
			raise ChannelRetrieveEventsError

		return self.events

