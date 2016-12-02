import lstarModule
import testLstar
import sys
import re
import time

def main():

	lstarInstance = lstarModule.Lstar()
	_TEST_ = 0

	# Parse arguments
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-h':
			print "Parameters:"
			print "-d\t\tDebug Mode"
			print "-t\t\tTest Mode"
			sys.exit()
		if sys.argv[i] == '-d':
			lstarInstance._DEBUG_ = 1

		if sys.argv[i] == '-t':
			_TEST_ = 1

		if sys.argv[i] == '-r':
			regex = re.compile(sys.argv[i+1])
			lstarInstance.regex = regex

		if sys.argv[i] == '-A':
			lstarInstance.setAlphabet(list(sys.argv[i+1]))

		if sys.argv[i] == '-l':
			lstarInstance.maxWordLength = int(sys.argv[i+1])

	if _TEST_ == 1:
		testInstance = testLstar.TestLstar()
		testInstance.testFunction(lstarInstance)
	else:	
		# Start with timer
		start_time = time.time()
		lstarInstance.main()
		print("\nExecution time: %s seconds " % (time.time() - start_time))

main()
