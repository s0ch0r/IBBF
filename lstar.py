import importlib
import sys
import time
from APModules import alphabet_parser

"""
Implements the l* algorithm, returns a DFSM
"""
def main(CQModule, MQModule, TModule, alphabet_location, debugFlag, timerFlag, cqpara, mqpara, tpara):

	# parse Alphabet
	parser = alphabet_parser.AlphabetParser(alphabet_location)
	A = parser.getAlphabet()

	# Init Modules
	sys.path.append('MQModules')
	MQModule = (importlib.import_module(MQModule)).MQModule(debugFlag, mqpara)
	sys.path.append('TableModules')
	tableModule = (importlib.import_module(TModule)).TableModule(MQModule, A, debugFlag, tpara)
	sys.path.append('CQModules')
	CQModule = (importlib.import_module(CQModule)).CQModule(MQModule, parser, debugFlag, cqpara)

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
	print "-A\t\tAlphabet (eg \"abcdef\")"
	print "-CQ\t\tConjecture Query - Module to be used"
	print "-MQ\t\tMembership Query - Module to be used"
	print "-TM\t\tTable - Module to be used"
	print "-cqp\t\tParameters for CQModule"
	print "-mqp\t\tParameters for MQModule"
	print "-tmp\t\tParameters for Table Module"
	print "-eT\t\tExtended Timer for Modules"
	sys.exit()

def parseParameters():

	_TEST_ = 0
	_DEBUG_ = 0
	_extendedTimer_ = 0
	alphabet_location = ""
	CQModuleName = "basicCQ"
	MQModuleName = "regexMQ"
	TModuleName = "basicTable"
	cqpara = 0
	mqpara = 0
	tpara = 0

	# Parse arguments
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-h':
			printHelp()

		if sys.argv[i] == '-d':
			_DEBUG_ = 1

		if sys.argv[i] == '-t':
			_TEST_ = 1
			
		if sys.argv[i] == '-A':
			alphabet_location = sys.argv[i+1]
		
		if sys.argv[i] == '-CQ':
			CQModuleName = sys.argv[i+1]
		
		if sys.argv[i] == '-MQ':
			MQModuleName = sys.argv[i+1]

		if sys.argv[i] == '-TM':
			TModuleName = sys.argv[i+1]

		if sys.argv[i] == '-eT':
			_extendedTimer_ = 1

		if sys.argv[i] == '-cqp':
			cqpara = sys.argv[i+1]

		if sys.argv[i] == '-mqp':
			mqpara = sys.argv[i+1]

		if sys.argv[i] == '-tp':
			tpara = sys.argv[i+1]

	# Test parameter
	if alphabet_location == "":
		printHelp()
	
	if _TEST_ == 1:
		print "Test Mode currently not available"
	else:	
		# Start with timer
		start_time = time.time()
		main(CQModuleName, MQModuleName, TModuleName, alphabet_location, _DEBUG_, _extendedTimer_, cqpara, mqpara, tpara)
		print("\nExecution time: %s seconds " % (time.time() - start_time))


parseParameters()