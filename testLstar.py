import lstarModule

def testFunction():
	print "Start Testing ... \n"
	errors = "\n"
	lstarTest = lstarModule.Lstar()

	#########################################
	# Test function testTableClosed()	#
	#########################################
	function = "testTableClosed()"

	# Testcase 1
	testcase = '1.1'

	lstarTest.A = ['0','1']
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

	
	#########################################
	# Test function fixTableNotClosed()	#
	#########################################
	function = "fixTableNotClosed()"

	#Testcase 1
	testcase = '2.1'

	lstarTest.A = ['0','1']
	lstarTest.E = ['',]
	lstarTest.S = {'':'1'}
	lstarTest.SA = {'0':'0', '1':'0'}	

	answer = lstarTest.fixTableNotClosed('1')
	expected_S = {'':'1', '1':'0'}
	expected_SA = {'0':'0','10':'0','11':'0'}
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

testFunction()
