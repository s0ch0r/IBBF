import sys
import getopt
import itertools
import importlib
from itertools import product
from collections import defaultdict

class Lstar:

	"""
	Init lstar instance
	"""
	def __init__(self):
		
		self._DEBUG_ = 0

		self.A = ['0','1']
		self.SA = {'0': '', '1': ''}
		self.S = {'':''}
		self.E = ['', ]


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
							return keys[i],keys[j]
		return ""



	"""
	Fixes a table which is not consistent, returns 1 on success and 0 on failure
	"""
	def fixTableInconsistent(self,s):

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

		found = 0	
		
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

		
		"""		
		# Returns 1 if the number of 1 and 0 both are even
		if (teststring == ''):
			return '1'

		testbinary = int('0b'+teststring, 2)

		x = 0
		y = 0

		for i in range(0, len(teststring)):
			if (testbinary & 1):
				x += 1
			else:
				y += 1
			testbinary >>= 1
		if (x % 2 == 0) and (y % 2 == 0):
			return '1'
		else:
			return '0'


		"""
		# Returns 1 if the number of 1 is 3 (modulo 4)
		if (teststring == ''):
			return '0'
		testbinary = int('0b'+teststring, 2)
		x = 0
		for i in range(0,len(teststring)):
			x += (testbinary & 1)
			testbinary >>= 1
		if (x % 4 == 3):
			return '1'
		else:
			return '0'
		
		
	"""
	Prints a visual representation of a given DFSM
	"""
	def printDFSM(self,DFSM):

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]

		# parse headline
		headline = "\ntransition table"
		for i in range(0, len(self.A)):
			headline += "| " + self.A[i] + "\t"

		# parse line
		line = ""
		for i in range(0, len(self.A) + 2):
			line += "--------"

		# parse content
		body = ""
		for key in ttable:
			body += " " + key + "\t-->\t"
			for i in range(0, len(self.A)):
				body += "| " + ttable[key][i] + "\t"
			body += "\n"

		if self._DEBUG_:
			print "\n\n################################################\nTable is closed and consistent - construct DFSM:\n################################################"
		
		print headline
		print line
		print body
		print "\nInitial state: " + str(initState)
		print "Final states: " + str(finiteStates)

		return 1 


	"""
	Generates x examples, if no counterexample was found the given DFSM, by chance, is correct
	"""
	def askTeacher(self,DFSM):

		initState = DFSM[0]
		finiteStates = DFSM[1]
		ttable = DFSM[2]

		# Generate table for mapping state transitions
		stateTransTable = {'':''}
		stateTransTable.clear()

		for key in ttable:
			for i in range(0, len(self.A)):
				stateTransTable[key+":"+self.A[i]] = ttable[key][i]

		# Generate examples and query them
		for i in range(1,5):
			examples = itertools.product(self.A, repeat = i)
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
					return ''.join(example)
		
		return ''


	"""
	Constructs a DFSM candidate and does a conjecture query
	"""
	def conjectureQuery(self):

		states = []
		ttable = defaultdict(list)
		ttable_new = defaultdict(list)
		finiteStates = []
		mapping = {'':'q0'}

		# parse different states
		for key in self.S:
			states.append([key,self.S[key]])
			for i in range(0, len(states)-1):
				if states[i][1] == states[len(states)-1][1]:
					states.remove([key,self.S[key]])
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

		for key in ttable:
			mapping[key] = 'q'+str(i)
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
		DFSM = [initState, finiteStates, ttable_new]

		# ask for counterexample
		if self._DEBUG_:
			self.printDFSM(DFSM)
		counterexample = self.askTeacher(DFSM)

		return counterexample, DFSM

	"""
	Adds a given counterexample to the Table
	"""
	def addCounterexample(self,counterexample):
		
		strings = []
		
		# Generate all values (prefixes) which should be added 
		for i in range(0,len(counterexample)+1):
			strings.append(counterexample)
			counterexample = counterexample[:-1]

		# Add values to S (and their corresponding ones to SA) if they are not already there
		for i in range(0, len(strings)):
			if strings[i] not in self.S:
				self.S[strings[i]] = self.queryRow(strings[i])
				for a in self.A:
					self.SA[strings[i]+a] = self.queryRow(strings[i]+a)
		
		# Remove duplicate values
		for key in self.S:
			if key in self.SA:
				del self.SA[key]

		return 1

	"""
	Prints a visual representation of the Table (S,E,T)
	"""
	def printTable(self,description):
		
		if self._DEBUG_:

			print "\n\n################################################\n" + description + "\n################################################"

			# Construct Headline with set E
			headline = "\n T\t|  \t"
			for i in range(1, len(self.E)):
				headline += "| " + self.E[i] + "\t"
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
				Alines += keys[i] + "\t"
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
				Blines += keys[i] + "\t"
				row = list(self.SA[keys[i]])
				for j in range(0, len(row)):
					Blines += "| " + row[j] + "\t"
				Blines += "\n"
			print Blines

			return 1

	"""
	Implements the l* algorithm, returns a DFSM
	"""
	def main(self):

		# Make initial table with S, E and lambda
		for key in self.S:
			self.S[key] = self.queryRow(key)
		for key in self.SA:
			self.SA[key] = self.queryRow(key)
		
		self.printTable("Initial table:")

		while(42==42):
			while(42==42):
				
				tmp = self.testTableClosed()
				if tmp is not "":
					self.fixTableNotClosed(tmp)
					self.printTable("Table after making it closed:")
					continue
				
				tmp = self.testTableConsistent()
				if tmp is not "":
					self.fixTableInconsistent(tmp)
					self.printTable("Table after making it consistent:")
					continue
				break
		
			counterexample, DFSM = self.conjectureQuery()
			if counterexample is not "":
				self.addCounterexample(counterexample)
				self.printTable(("Table after a counterexample \"" + counterexample + "\" was added:"))
				continue
			break
		
		print "\n\n##################################\n# L* terminated succesfully!! :) #\n##################################"
		self.printDFSM(DFSM)
		return 1 

