
# Event Exceptions 
class EventAttrError(Exception):
	pass

# Channel Exceptions
class ChannelDataNotFound(Exception):
	pass

class ChannelServerError(Exception):
	pass


# Console
class ConsoleConfigFileDoesNotExist(Exception):
	pass

class ConsoleConfigFileFormatError(Exception):
	pass

class ConsoleCommandDoesNotExist(Exception):
	pass
	
class ConsoleCommandChannelNotFound(Exception):
	pass

