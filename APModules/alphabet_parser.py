from IBBFObjects import basicObject

class AlphabetParser:

    def __init__(self, location):
        self.location = location

    def getAlphabet(self):

        alphabet_file = open(self.location, 'r')
        A = []

        while 42 == 42:

            line = alphabet_file.readline()

            if line.endswith('\n'):
                line = line[:-1]

            if line != "":
                A.append(basicObject.IBBFObj(line))
            else:
                break

        return A