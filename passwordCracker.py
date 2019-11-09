# Abdullah Arif 
# COMP-4670 password cracking final project
import itertools
import string

def getFileInfo(filePath : str):
    file = open(filePath,"r")
    return file.read().splitlines()

def bruteForce(keyspace, passwordList, max_length):
    recoveredList =[]
    for i in range( max_length ):
        # attempt for a given length
        lengthAttempt = itertools.product(keyspace,repeat=i+1)
        for attempt in lengthAttempt:
            possiblePassword = ''.join(attempt)
            # print("Trying "+ possiblePassword)
            for password in passwordList:
                if possiblePassword == password:
                    print('Password: '+ possiblePassword)
                    recoveredList.append(possiblePassword)
                if len(recoveredList) == len(passwordList):
                    return recoveredList
    return recoveredList








 # string.printable[:-5]
# bruteForce("abcdefghijklmnopqrstuvwxyz", ['a','ab','lily', 'jsfx', 'alpham'], 5)
bruteForce(['alpha','meg', 'a','b'], ['a','ab','lily', 'jsfx', 'alphameg','alphamega'], 5)
# opening file with th graphical version of the program will be done in 
# def openFile():
#     Tk().withdraw()
#     fileFormats = [('All Files','*'),
#                ('Text File','*.txt')    ]
#     filename = filedialog.askopenfile(mode="r",title="Load",filetypes = fileFormats)