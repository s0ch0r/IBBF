import importlib
import sys
import time
import os
from APModules import alphabet_parser

"""
Implements the l* algorithm, returns a DFSM
"""
def main(object_classname, CQModule, MQModule, TModule, alphabet_location, debugFlag, timerFlag, testFlag, cqpara, mqpara, tpara):
	# Init ObjectClass
	sys.path.append('IBBFObjects')
	ObjectClass = (importlib.import_module(object_classname))

	# parse Alphabet
	parser = alphabet_parser.AlphabetParser(alphabet_location, ObjectClass)
	A = parser.getAlphabet()

	# Init Modules
	sys.path.append('MQModules')
	MQModule = (importlib.import_module(MQModule)).MQModule(debugFlag, mqpara)
	sys.path.append('TableModules')
	tableModule = (importlib.import_module(TModule)).TableModule(ObjectClass, MQModule, A, debugFlag, tpara, testFlag)
	sys.path.append('CQModules')
	CQModule = (importlib.import_module(CQModule)).CQModule(ObjectClass, MQModule, parser, debugFlag, cqpara, testFlag)

	DFSM = 0

	# Algorithm
	while 42 == 42:

		tableModule.fixTable()
		DFSM = tableModule.getDFSM()
		counterexample = CQModule.isCorrect(DFSM)

		if counterexample is not "":
			tableModule.addCounterexample(counterexample)
			continue
		break

	if not testFlag:
		print "\n\n##################################\n# L* terminated succesfully!! :) #\n##################################"

	if timerFlag and not testFlag:
		print "Execution time of modules:"
		print "Conjecture-Query-Module: " + str(CQModule.getTime())
		print "Table-Module:            " + str(tableModule.getTime())

	return DFSM


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
	CQModuleName = "randomCQ"
	MQModuleName = "regexMQ"
	TModuleName = "basicTable"
	object_classname = "basicObject"
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
			alphabet_location = sys.argv[i + 1]

		if sys.argv[i] == '-CQ':
			CQModuleName = sys.argv[i + 1]

		if sys.argv[i] == '-MQ':
			MQModuleName = sys.argv[i + 1]

		if sys.argv[i] == '-TM':
			TModuleName = sys.argv[i + 1]

		if sys.argv[i] == '-eT':
			_extendedTimer_ = 1

		if sys.argv[i] == '-cqp':
			cqpara = sys.argv[i + 1]

		if sys.argv[i] == '-mqp':
			mqpara = sys.argv[i + 1]

		if sys.argv[i] == '-tp':
			tpara = sys.argv[i + 1]

		if sys.argv[i] == '-O':
			object_classname = sys.argv[i + 1]

	# Test parameter
	if alphabet_location == "":
		printHelp()

	if _TEST_ == 1:
		startTesting()
		sys.exit()
	else:
		# Start with timer
		start_time = time.time()
		main(object_classname, CQModuleName, MQModuleName, TModuleName, alphabet_location, _DEBUG_, _extendedTimer_, _TEST_, cqpara, mqpara, tpara)
		print("\nExecution time: %s seconds " % (time.time() - start_time))


def startTesting():

	# Get CQModules:
	CQModule_list = []
	for filename in os.listdir("C:\_Daten\Daten\IBBF\CQModules"):
		if filename.endswith(".py") and filename != "__init__.py":
			CQModule_list.append(filename.split('.')[0])

	# Get MQModules:
	MQModule_list = []
	for filename in os.listdir("C:\_Daten\Daten\IBBF\MQModules"):
		if filename.endswith(".py") and filename != "__init__.py":
			MQModule_list.append(filename.split('.')[0])

	# Get TableModules:
	TableModule_list = []
	for filename in os.listdir("C:\_Daten\Daten\IBBF\TableModules"):
		if filename.endswith(".py") and filename != "__init__.py":
			TableModule_list.append(filename.split('.')[0])

	errors = 0
	warnings = 0

	# Try combinations
	for CQModule in CQModule_list:
		for MQModule in MQModule_list:
			for TableModule in TableModule_list:

				# Test combination
				print "Testing " + str(CQModule) + "-" + str(MQModule) + "-" + str(TableModule) + " ..."
				result = "Passed"
				try:
					# Get modules for test-parameters
					parameter = {}
					sys.path.append('CQModules')
					parameter['CQ'] = (importlib.import_module(CQModule).CQModule.getTestParameter())
					sys.path.append('MQModules')
					parameter['MQ'] = (importlib.import_module(MQModule).MQModule.getTestParameter())
					sys.path.append('TableModules')
					parameter['T'] = (importlib.import_module(TableModule).TableModule.getTestParameter())

					# Test-Run
					DFSM = main("basicObject", CQModule, MQModule, TableModule, "IBBFTestFiles/alphabet.txt", 0, 0, 1, parameter['CQ'], parameter['MQ'], parameter['T'])

					# See if result seems to be correct
					if len(DFSM[1]) != 2 or len(DFSM[2]) != 9 or len(DFSM[3]) != 77:
						warnings += 1
						result = "WARNING :: No errors occurred, but it seems that the resulting DFSM is incorrect"
				except Exception as e:
					errors += 1
					result = "ERROR :: " + str(e)
				print result

	print "\nFinished, " + str(warnings) + " warnings and " + str(errors) + " errors."


parseParameters()
