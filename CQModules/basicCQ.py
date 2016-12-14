import itertools

class CQModule:

	"""
	Init lstar instance
	"""
	def __init__(self, MQModule, debugFlag, length):
		
		self._DEBUG_ = debugFlag

		self.MQModule = MQModule

		self.maxWordLength = length


	"""
	Prints a visual representation of a given DFSM
	"""
	@staticmethod
	def printDFSM(DFSM, description):
		
		print "\n\n################################################\n" + description + "\n" \
			  "################################################ "

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]
		A = DFSM[3]

		# parse headline
		headline = "\ntransition table"
		for i in range(0, len(A)):
			headline += "| " + A[i] + "\t"

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

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]
		A = DFSM[3]

		# Generate table for mapping state transitions
		stateTransTable = {'': ''}
		stateTransTable.clear()

		for key in ttable:
			for i in range(0, len(A)):
				stateTransTable[key+":"+A[i]] = ttable[key][i]

		# Generate examples and query them
		for i in range(1, self.maxWordLength+1):
			examples = itertools.product(A, repeat=i)
			for example in examples:
				
				# Calculate membership according to own DFSM
				
				answer = initState
				for a in example:
					answer = stateTransTable[answer+":"+a]
				if answer in finiteStates:
					answer = '1'
				else:
					answer = '0'
				
				# Compare
				if answer != self.membershipQuery(''.join(example)):
					if self._DEBUG_:
						self.printDFSM(DFSM, "Following is not the correct DFSM")
					return ''.join(example)
		
		self.printDFSM(DFSM, "Following is the correct DFSM")
		return ''