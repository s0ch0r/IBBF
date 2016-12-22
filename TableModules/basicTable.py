from collections import defaultdict
import time
from IBBFObjects import simple_object
import sys

class TableModule:

	"""
	Init lstar instance
	"""
	def __init__(self, MQModule, A, debugFlag, params):
		
		self._DEBUG_ = debugFlag
		self.MQModule = MQModule
		self._TIME_ = 0

		self.A = ['', ]
		self.SA = {simple_object.IBBFObj(''): ''}
		self.S = {simple_object.IBBFObj(''): self.membershipQuery(simple_object.IBBFObj(''))}
		self.E = [simple_object.IBBFObj(''), ]
		
		self.setAlphabet(A)

		self.printTable("Initial Table")


	def getTime(self):
		return self._TIME_

	
	""" 
	Sets a new alphabet and initialises S and SA
	"""
	def setAlphabet(self, newA):
	
		self.SA.clear()
		self.A = newA
		for a in self.A:
			self.SA[simple_object.IBBFObj('') + a] = self.membershipQuery(simple_object.IBBFObj('') + a)

		return 1


	"""
	Fixes Table so it is closed and consistent
	"""
	def fixTable(self):

		start_time = time.time()

		while 42 == 42:
			answer = self.testTableClosed()
			if answer != "":
				self.fixTableNotClosed(answer)
				self.printTable("Table after closing it")
				continue
			answer = self.testTableConsistent()
			if answer != "":
				self.fixTableInconsistent(answer)
				self.printTable("Table after fixing inconsistency")
				continue
			self._TIME_ += time.time()-start_time
			return 1
		self._TIME_ += time.time()-start_time
		return 0

	"""
	Tests if the Table is consistent, returns '' if yes and the value of s_1 and s_2 if not
	"""
	def testTableConsistent(self):

		keys = self.S.keys()
		
		# Search for identical rows
		for i in range(0, len(keys)):
			for j in range(i+1, len(keys)):
				if self.S[keys[i]] == self.S[keys[j]]:
					
					# if found, test if row(s_1 + a) == row(s_2 + a) 
					for a in self.A:
						if (keys[i]+a) in self.S:
							s_1 = self.S[keys[i]+a]
						else:
							s_1 = self.SA[keys[i]+a]
						if (keys[j]+a) in self.S:
							s_2 = self.S[keys[j]+a]
						else:
							s_2 = self.SA[keys[j]+a]

						# if not the same return the inconsistent values
						if s_1 != s_2:
							return keys[i], keys[j]
		return ""



	"""
	Fixes a table which is not consistent, returns 1 on success and 0 on failure
	"""
	def fixTableInconsistent(self, s):

		# Search for suitable canditates of a and e to fix the inconsistency of the given values s_1, s_2
		for a in self.A:
			for e in self.E:
				if self.membershipQuery(s[0]+a+e) is not self.membershipQuery(s[1]+a+e):
					
					# add suitable value (ae) to E
					self.E.append(a+e)

					# Fill new collumn with membership queries
					for key in self.S:
						self.S[key] += self.membershipQuery(key+a+e)
					for key in self.SA:
						self.SA[key] += self.membershipQuery(key+a+e)
					return 1
		return 0

	"""
	Test if the table is closed, returns '' if yes and the value if not
	"""
	def testTableClosed(self):
		
		# Validate if all rows in SA are also rows in S
		for key_SA in self.SA:
			found = 0
			for key_S in self.S:
				if self.SA[key_SA] == self.S[key_S]:
					found = 1
					break

			# if a row in SA was not found in S, return it's corresponding key
			if found == 0:
				return key_SA
		return ""

	"""
	Fixes a table which is not closed by adding the missing value and returns 1 on success and 0 on failure
	"""
	def fixTableNotClosed(self, key):
		
		# Add key to S
		self.S[key] = self.queryRow(key)

		# remove key from SA
		del self.SA[key]

		# Add missing keys to SA
		for a in self.A:
			self.SA[key+a] = self.queryRow(key+a)

		return 1

	"""
	Returns a whole row to a given value from S or SA
	"""
	def queryRow(self, value):

		string = ''

		for i in range(0, len(self.E)):
			string += self.membershipQuery(value+self.E[i])

		return string

	"""
	Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
	"""
	def membershipQuery(self, teststring):

		return self.MQModule.isMember(teststring)

	"""
	Constructs a DFSM candidate and does a conjecture query
	"""
	def getDFSM(self):

		start_time = time.time()

		row = 0
		initState = 0
		states = []
		ttable = defaultdict(list)
		ttable_new = defaultdict(list)
		finiteStates = []

		# parse different states
		for key in self.S:
			states.append([key, self.S[key]])
			for i in range(0, len(states)-1):
				if states[i][1] == states[len(states)-1][1]:
					states.remove([key, self.S[key]])
					break

		# make state transition table
		for i in range(0, len(states)):

			if states[i][0] == '':
				initState = states[i][0]

			for a in self.A:
				if (states[i][0] + a) in self.SA:
					row = self.SA[states[i][0] + a]
				elif (states[i][0] + a) in self.S:
					row = self.S[states[i][0] + a]
				for j in range(0, len(states)):
					if row == states[j][1]:
						ttable[states[i][0]].append(states[j][0])
						break

		# parse finite and initial state(s)
		for i in range(0, len(states)):

			if states[i][1][0] == '1':
				finiteStates.append(states[i][0])
			if states[i][0] == '':
				initState = states[i][0]

		# parse to readable form by exchanging state names with values of the form q_i:
		i = 0
		mapping = {simple_object.IBBFObj(''): 'q0'}

		for key in ttable:
			mapping[key] = 'q' + str(i)
			i += 1

		initState = mapping[initState]
		for i in range(0, len(finiteStates)):
			finiteStates[i] = mapping[finiteStates[i]]

		for key in ttable:
			for i in range(0, len(self.A)):
				ttable[key][i] = mapping[ttable[key][i]]

		for key in ttable:
			ttable_new[mapping[key]] = ttable[key]

		# make DFSM
		DFSM = [initState, finiteStates, ttable_new, self.A]

		self._TIME_ += time.time()-start_time
		return DFSM

	"""
	Adds a given counterexample to the Table
	"""
	def addCounterexample(self, counterexample):

		start_time = time.time()

		objects = []

		for i in range(len(counterexample.identifier)-1, 0, -1):
			self.S[counterexample] = self.queryRow(counterexample)
			for a in self.A:
				self.SA[counterexample + a] = self.queryRow(counterexample + a)
			counterexample = counterexample.removeElement()
		
		# Remove duplicate values
		for key in self.S:
			if key in self.SA:
				del self.SA[key]

		self.printTable("Table after adding counterexample \"" + str(counterexample.identifier) + "\"")

		self._TIME_ += time.time()-start_time
		return 1

	"""
	Prints a visual representation of the Table (S,E,T)
	"""
	def printTable(self, description):
		
		if self._DEBUG_:

			print "\n\n################################################\n" + description + "\n" \
			      "################################################ "

			# Construct Headline with set E
			headline = "\n T\t|  \t"
			for i in range(1, len(self.E)):
				headline += "| " + str(self.E[i].identifier) + "\t"
			print headline

			# Construct line
			line = ""
			for i in range(0, len(headline)):
				line += "--"
			print line

			# Construct S
			keys = self.S.keys()
			Alines = ""
			for i in range(0, len(keys)):
				Alines += str(keys[i].identifier) + "\t"
				row = list(self.S[keys[i]])
				for j in range(0, len(row)):
					Alines += "| " + row[j] + "\t"
				if i+1 < len(keys):
					Alines += "\n"
			print Alines
			print line

			# Construct SA
			keys = self.SA.keys()
			Blines = ""
			for i in range(0, len(keys)):
				Blines += str(keys[i].identifier) + "\t"
				row = list(self.SA[keys[i]])
				for j in range(0, len(row)):
					Blines += "| " + row[j] + "\t"
				Blines += "\n"
			print Blines

			return 1
