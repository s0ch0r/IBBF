import re

class MQModule:

	"""
	Init instance
	"""
	def __init__(self, debugFlag, regex):

		self._DEBUG_ = debugFlag
		self.regex = re.compile(regex)


	"""
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""
	def isMember(self, teststring):

		if self.regex.match(teststring):
			return '1'
		else:
			return '0'
