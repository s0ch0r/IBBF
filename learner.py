import time
import socket
import struct
import select
import random
import asyncore
import sys
import getopt
import time
import itertools
from itertools import product
from string import ascii_lowercase
from threading import Thread
from collections import defaultdict


_DEBUG_ = 0

A = ['0','1']
E = ['', ]
S = {'':''}
SA = {'0': '', '1': ''}


"""
Tests if the Table is consistent, returns 0 if yes and the value of s_1 and s_2 if not
"""
def testTableConsistent():

	keys = S.keys()
	
	# Search for identical rows
	for i in range(0, len(keys)):
		for j in range(i+1, len(keys)):
			if S[keys[i]] == S[keys[j]]:
				
				# if found, test if row(s_1 + a) == row(s_2 + a) 
				for a in A:
					if (keys[i]+a) in S:
						s_1 = S[keys[i]+a]
					else:
						s_1 = SA[keys[i]+a]
					if (keys[j]+a) in S:
						s_2 = S[keys[j]+a]
					else:
						s_2 = SA[keys[j]+a]

					# if not the same return the inconsistent values
					if s_1 != s_2:
						return keys[i],keys[j]
	return ""



"""
Fixes a table which is not consistent, returns 1 on success and 0 on failure
"""
def fixTableInconsistent(s):

	# Search for suitable canditates of a and e to fix the inconsistency of the given values s_1, s_2
	for a in A:
		for e in E:
			if membershipQuery(s[0]+a+e) is not membershipQuery(s[1]+a+e):
				
				# add suitable value (ae) to E
				E.append(a+e)

				# Fill new collumn with membership queries
				for key in S:
					S[key] += membershipQuery(key+a+e)
				for key in SA:
					SA[key] += membershipQuery(key+a+e)
				return 1
	return 0

"""
Test if the table is closed, returns 0 if yes and the value if not
"""
def testTableClosed():
	
	found = 0	
	
	# Validate if all rows in SA are also rows in S
	for key_SA in SA:
		found = 0
		for key_S in S:
			if SA[key_SA] == S[key_S]:
				found = 1
				break

		# if a row in SA was not found in S, return it's corresponding key
		if found == 0:
			return key_SA
	return ""

"""
Fixes a table which is not closed by adding the missing value and returns 1 on success and 0 on failure
"""
def fixTableNotClosed(key):
	
	# Add key to S
	S[key] = queryRow(key)

	# remove key from SA
	del SA[key]

	# Add missing keys to SA
	for a in A:
		SA[key+a] = queryRow(key+a)

	return 1

"""
Returns a whole row to a given value from S or SA
"""
def queryRow(value):

	string = ''

	for i in range(0, len(E)):
		string += membershipQuery(value+E[i])

	return string

"""
Makes a membership query to a teacher and returns 1 if string was a member and 0 if not
"""
def membershipQuery(teststring):

	
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
def printDFSM(DFSM):

	initState = DFSM[0]
	finiteStates = DFSM[1]
	ttable = DFSM[2]

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

	if _DEBUG_:
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
def askTeacher(DFSM):

	initState = DFSM[0]
	finiteStates = DFSM[1]
	ttable = DFSM[2]

	# Generate table for mapping state transitions
	stateTransTable = {'':''}
	stateTransTable.clear()

	for key in ttable:
		for i in range(0, len(A)):
			stateTransTable[key+":"+A[i]] = ttable[key][i]

	# Generate examples and query them
	for i in range(1,5):
		examples = itertools.product(A, repeat = i)
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
			if answer != membershipQuery(''.join(example)):
				return ''.join(example)
	
	return ''


"""
Constructs a DFSM candidate and does a conjecture query
"""
def conjectureQuery():

	states = []
	ttable = defaultdict(list)
	ttable_new = defaultdict(list)
	finiteStates = []
	mapping = {'':'q0'}

	# parse different states
	for key in S:
		states.append([key,S[key]])
		for i in range(0, len(states)-1):
			if states[i][1] == states[len(states)-1][1]:
				states.remove([key,S[key]])
				break

	# make state transition table
	for i in range(0, len(states)):

		if states[i][0] == '':
			initState = states[i][0]

		for a in A:
			if (states[i][0] + a) in SA:
				row = SA[states[i][0] + a]
			elif (states[i][0] + a) in S:
				row = S[states[i][0] + a]
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
		for i in range(0, len(A)):
			ttable[key][i] = mapping[ttable[key][i]]
	
	for key in ttable:
		ttable_new[mapping[key]] = ttable[key]

	# make DFSM
	DFSM = [initState, finiteStates, ttable_new]

	# ask for counterexample
	if _DEBUG_:
		printDFSM(DFSM)
	counterexample = askTeacher(DFSM)

	return counterexample, DFSM

"""
Adds a given counterexample to the Table
"""
def addCounterexample(counterexample):
	
	strings = []
	
	# Generate all values (prefixes) which should be added 
	for i in range(0,len(counterexample)+1):
		strings.append(counterexample)
		counterexample = counterexample[:-1]

	# Add values to S (and their corresponding ones to SA) if they are not already there
	for i in range(0, len(strings)):
		if strings[i] not in S:
			S[strings[i]] = queryRow(strings[i])
			for a in A:
				SA[strings[i]+a] = queryRow(strings[i]+a)
	
	# Remove duplicate values
	for key in S:
		if key in SA:
			del SA[key]

	return 1

"""
Prints a visual representation of the Table (S,E,T)
"""
def printTable(description):
	
	if _DEBUG_:

		print "\n\n################################################\n" + description + "\n################################################"

		# Construct Headline with set E
		headline = "\n T\t|  \t"
		for i in range(1, len(E)):
			headline += "| " + E[i] + "\t"
		print headline

		# Construct line
		line = ""
		for i in range(0, len(headline)):
			line += "--"
		print line

		# Construct S
		keys = S.keys()
		Alines = ""
		for i in range(0, len(keys)):
			Alines += keys[i] + "\t"
			row = list(S[keys[i]])
			for j in range(0, len(row)):
				Alines += "| " + row[j] + "\t"
			if i+1 < len(keys):
				Alines += "\n"
		print Alines
		print line

		# Construct SA
		keys = SA.keys()
		Blines = ""
		for i in range(0, len(keys)):
			Blines += keys[i] + "\t"
			row = list(SA[keys[i]])
			for j in range(0, len(row)):
				Blines += "| " + row[j] + "\t"
			Blines += "\n"
		print Blines

		return 1

"""
Implements the l* algorithm, returns a DFSM
"""
def main():

	# Make initial table with S, E and lambda
	for key in S:
		S[key] = queryRow(key)
	for key in SA:
		SA[key] = queryRow(key)
	
	printTable("Initial table:")

	while(42==42):
		while(42==42):
			
			tmp = testTableClosed()
			if tmp is not "":
				fixTableNotClosed(tmp)
				printTable("Table after making it closed:")
				continue
			
			tmp = testTableConsistent()
			if tmp is not "":
				fixTableInconsistent(tmp)
				printTable("Table after making it consistent:")
				continue
			break
	
		counterexample, DFSM = conjectureQuery()
		if counterexample is not "":
			addCounterexample(counterexample)
			printTable(("Table after a counterexample \"" + counterexample + "\" was added:"))
			continue
		break
	
	print "\n\n##################################\n# L* terminated succesfully!! :) #\n##################################"
	printDFSM(DFSM)
	return 1 

"""
Tests the implemented functions
"""
def testFunctions():

	# Test function testTableClosed()
	# Test function fixTableNotClosed()
	# Test function testTableConsistent()
	# Test function fixTableInconsistent()
	# Test function conjectureQuery()
	# Test function askTeacher()
	# Test function addCounterexample()
	return 1

# Parse arguments
for arg in sys.argv:
	if arg == '-h':
		print "Parameters:"
		print "-d\t\tDebug Mode"
		sys.exit()
	elif arg == '-d':
		_DEBUG_ = 1
	elif arg == '-t':
		testFunctions()
		sys.exit()		
main()
