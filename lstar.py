import sys
import importlib
import time

"""
Implements the l* algorithm, returns a DFSM
"""
def main(CQModule, MQModule, TModule, A, regex, debugFlag, length, timerFlag):

	# Init Modules
	sys.path.append('MQModules')
	MQModule = (importlib.import_module(MQModule)).MQModule(regex, debugFlag)
	sys.path.append('TableModules')
	tableModule = (importlib.import_module(TModule)).TableModule(MQModule, A, debugFlag)
	sys.path.append('CQModules')
	CQModule = (importlib.import_module(CQModule)).CQModule(MQModule, tableModule, debugFlag, length)

	# Algorithm
	while 42 == 42:

		tableModule.fixTable()
		DFSM = tableModule.getDFSM()
		counterexample = CQModule.isCorrect(DFSM)
		
		if counterexample is not "":
			tableModule.addCounterexample(counterexample)
			continue
		break
		
	print "\n\n##################################\n# L* terminated succesfully!! :) #\n##################################"

	if timerFlag:
		print "Execution time of modules:"
		print "Conjecture-Query-Module: " + str(CQModule.getTime())
		print "Table-Module:            " + str(tableModule.getTime())

	return 1


def printHelp():
	print "Parameters:"
	print "-d\t\tDebug Mode"
	print "-t\t\tTest Mode"
	print "-r\t\tRegex"
	print "-A\t\tAlphabet (eg \"abcdef\")"
	print "-l\t\tMaxLength of Strings (only for basicCQ-Module)"
	print "-CQ\t\tConjecture Query - Module to be used"
	print "-MQ\t\tMembership Query - Module to be used"
	print "-TM\t\tTable - Module to be used"
	sys.exit()

def parseParameters():

	_TEST_ = 0
	_DEBUG_ = 0
	_extendedTimer_ = 0
	length = 5  	# Only for basicCQ module
	A = ""
	regex = ""
	CQModuleName = "basicCQ"
	MQModuleName = "regexMQ"
	TModuleName = "basicTable"

	# Parse arguments
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-h':
			printHelp()

		if sys.argv[i] == '-d':
			_DEBUG_ = 1

		if sys.argv[i] == '-t':
			_TEST_ = 1

		if sys.argv[i] == '-r':
			regex = sys.argv[i+1]
			
		if sys.argv[i] == '-A':
			A = list(sys.argv[i+1])

		if sys.argv[i] == '-l':
			length = int(sys.argv[i+1])
		
		if sys.argv[i] == '-CQ':
			CQModuleName = sys.argv[i+1]
		
		if sys.argv[i] == '-MQ':
			MQModuleName = sys.argv[i+1]

		if sys.argv[i] == '-TM':
			TModuleName = sys.argv[i+1]
		if sys.argv[i] == '-eT':
			_extendedTimer_ = 1

	# Test parameter
	if A == "" or regex == "":
		printHelp()
	
	if _TEST_ == 1:
		print "Test Mode currently not available"
	else:	
		# Start with timer
		start_time = time.time()
		main(CQModuleName, MQModuleName, TModuleName, A, regex, _DEBUG_, length, _extendedTimer_)
		print("\nExecution time: %s seconds " % (time.time() - start_time))


parseParameters()
