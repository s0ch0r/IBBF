import random
import time
from IBBFObjects import simple_object
from collections import defaultdict

class CQModule:

	"""
	Init lstar instance
	"""
	def __init__(self, MQModule, parser, debugFlag, params):
		
		self._DEBUG_ = debugFlag
		self._TIME_ = 0

		self.MQModule = MQModule
		self.Parser = parser

		parameter = params.split(",")

		self.tries = int(parameter[0])
		self.length = int(parameter[1])

	def getTime(self):
		return self._TIME_
	"""
	Prints a visual representation of a given DFSM
	"""
	def printDFSM(self, DFSM, description):

		print "\n\n################################################\n" + description + "\n" \
			  "################################################ "

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]
		A = DFSM[3]

		# parse headline
		headline = "\ntransition table"
		for i in range(0, len(A)):
			headline += "| " + ''.join(A[i].identifier) + "\t"

		# parse line
		line = ""
		for i in range(0, len(A) + 2):
			line += "--------"

		# parse content
		body = ""
		for key in ttable:
			body += " " + key + "\t-->\t"
			for i in range(0, len(A)):
				body += "| " + ttable[key][i] + "\t"
			body += "\n"

		print headline
		print line
		print body
		print "\nInitial state: " + str(initState)
		print "Final states: " + str(finiteStates)

		return 1




	"""
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""
	def membershipQuery(self, teststring):

		return self.MQModule.isMember(teststring)


	"""
	Generates x examples, if no counterexample was found the given DFSM, by chance, is correct
	"""
	def isCorrect(self, DFSM):

		start_time = time.time()

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]
		A = DFSM[3]

		# Generate table for mapping state transitions
		stateTransTable = {'': ''}
		stateTransTable.clear()

		for key in ttable:
			for i in range(0, len(A)):
				stateTransTable[(key, A[i].identifier[0])] = ttable[key][i]

		# Generate examples and query them
		for i in range(0, self.tries):

			# Generate random example
			example = []
			for j in range(0, random.randint(0, self.length-1)):
				example.append(A[random.randint(0, len(A)-1)].identifier[0])

			# Calculate membership according to own DFSM
			answer = initState
			for a in example:
				answer = stateTransTable[(answer, a)]
			if answer in finiteStates:
				answer = '1'
			else:
				answer = '0'

			# Generate Query object
			query = simple_object.IBBFObj('')
			for a in example:
				query += simple_object.IBBFObj(a)


			# Compare
			if answer != self.membershipQuery(query):
				if self._DEBUG_:
					self.printDFSM(DFSM, "Following is not the correct DFSM")
				self._TIME_ += time.time()-start_time
				return query

		self._TIME_ += time.time()-start_time
		self.printDFSM(DFSM, "Following is the correct DFSM")
		return ''