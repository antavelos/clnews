
# Event Exceptions 
class EventAttrError(Exception):
	pass


# Channel Exceptions
class ChannelDataNotFound(Exception):
	pass

class ChannelServerError(Exception):
	pass

class ChannelRetrieveEventsError(Exception):
	pass


# Console
class ConsoleCommandDoesNotExist(Exception):
	pass
	
class ConsoleCommandChannelNotFound(Exception):
	pass
