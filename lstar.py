import lstarModule
import testLstar
import sys

def main():

	lstarInstance = lstarModule.Lstar()
	
	# Parse arguments
	for arg in sys.argv:
		if arg == '-h':
			print "Parameters:"
			print "-d\t\tDebug Mode"
			print "-t\t\tTest Mode"
			sys.exit()
		if arg == '-d':
			lstarInstance._DEBUG_ = 1

		if arg == '-t':
			testInstance = testLstar.TestLstar()
			testInstance.testFunction()
			sys.exit()

	lstarInstance.main()

main()
