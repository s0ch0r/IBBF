import lstarModule
import re

class TestLstar:

	#def __init__(self):
		# Nothing to do here

	def testFunction(self,testInstance):
		
		print "Start Testing ... \n"
		errors = "\n"
		lstarTest = testInstance

		#########################################
		# Test function testTableClosed()	#
		#########################################
		function = "testTableClosed()"

		# Testcase 1
		testcase = '1.1'

		lstarTest.A = ['0','1']
		lstarTest.regex = re.compile('1[0]*1')
		lstarTest.E = ['',]
		lstarTest.S = {'':'1'}
		lstarTest.SA = {'0':'0', '1':'0'}

		answer = lstarTest.testTableClosed()
		expected = ['0','1']

		if answer not in expected:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected) + "\" but was \"" + answer + "\" \t(" + testcase + ")\n"
		else:
			print "Success"


		# Testcase 2
		testcase = '1.2'

		lstarTest.A = ['0','1']
		lstarTest.regex = re.compile('1[0]*1')
		lstarTest.E = ['',]
		lstarTest.S = {'':'0'}
		lstarTest.SA = {'0':'0', '1':'0'}	

		answer = lstarTest.testTableClosed()
		expected = ''
		if answer not in expected:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected) + "\" but was \"" + answer + "\" \t(" + testcase + ")\n"
		else:
			print "Success"

		
		# Testcase 3
		testcase = '1.3'

		lstarTest.A = ['0','1']
		lstarTest.regex = re.compile('1[0]*1')
		lstarTest.E = ['','1']
		lstarTest.S = {'':'00','1':'00','11':'01','111':'10'}
		lstarTest.SA = {'0':'00','10':'00','110':'01','1110':'10','1111':'00'}

		lstarTest.testTableClosed()
		expected = ''

		if answer != expected:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected) + "\" but was \"" + str(answer) + "\" \t(" + testcase + ")\n"
		else:
			print "Success"

		# Testcase 4
		testcase = '1.4'

		lstarTest.A = ['a','@','c']
		lstarTest.regex = re.compile('[a,c]*@[a,c]')
		lstarTest.E = ['']
		lstarTest.S = {'':'0'}
		lstarTest.SA = {'a':'0','@':'1','c':'0'}
		
		lstarTest.printTable("Test")

		lstarTest.testTableClosed()
		expected = '@'

		if answer != expected:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected) + "\" but was \"" + str(answer) + "\" \t(" + testcase + ")\n"
		else:
			print "Success"




		#########################################
		# Test function fixTableNotClosed()	#
		#########################################
		function = "fixTableNotClosed()"

		#Testcase 1
		testcase = '2.1'

		lstarTest.A = ['0','1']
		lstarTest.regex = re.compile('1[0]*1')
		lstarTest.E = ['',]
		lstarTest.S = {'':'1'}
		lstarTest.SA = {'0':'0', '1':'0'}	

		answer = lstarTest.fixTableNotClosed('1')
		expected_S = {'':'1', '1':'0'}
		expected_SA = {'0':'0','10':'0','11':'1'}
		if lstarTest.S != expected_S:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected_S) + "\" but was \"" + str(lstarTest.S) + "\" \t(" + testcase + ")\n"
		elif lstarTest.SA != expected_SA:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected_SA) + "\" but was \"" + str(lstarTest.SA) + "\" \t(" + testcase + ")\n"
		else:
			print "Success"


		#Testcase 2
		testcase = '2.2'

		lstarTest.A = ['0','1']
		lstarTest.regex = re.compile('1[0]*1')
		lstarTest.E = ['','1']
		lstarTest.S = {'':'00','1':'00','11':'00','111':'10'}
		lstarTest.SA = {'0':'00','10':'00','110':'01','1110':'10','1111':'00'}

		answer = lstarTest.fixTableNotClosed('110')
		expected_S = {'':'00','1':'00','11':'00','111':'10','110':'11'}
		expected_SA = {'0':'00','10':'00','1110':'10','1111':'00','1100':'11','1101':'11'}

		if lstarTest.S != expected_S:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected_S) + "\" but was \"" + str(lstarTest.S) + "\" \t(" + testcase + ")\n"
		elif lstarTest.SA != expected_SA:
			print "Fail"
			errors += "Failure in function \"" + function + "\": Expected \"" + str(expected_SA) + "\" but was \"" + str(lstarTest.SA) + "\" \t(" + testcase + ")\n"
		else:
			print "Success"




		#########################################
		# Test function testTableConsistent()	#
		#########################################
		function = "testTableConsistent()"

		#Testcase 1


		#########################################
		# Test function fixTableInconsistent()	#
		#########################################
		function = "fixTableConsistent()"

		#Testcase 1


		#########################################
		# Test function conjectureQuery()	#
		#########################################
		function = "conjectureQuery()"

		#Testcase 1


		#########################################
		# Test function askTeacher()		#
		#########################################
		function = "askTeacher()"

		#Testcase 1


		#########################################
		# Test function addCounterexample()	#
		#########################################
		function = "addCounterexample()"

		#Testcase 1



		# print out details about failed tests
		if errors != '\n':
			print errors
		else:
			print "\nPassed all tests succesfully!!"
		return 1
