
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


# Shell
class ShellCommandDoesNotExist(Exception):
	pass
	
class ShellCommandChannelNotFound(Exception):
	pass
