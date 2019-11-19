# Abdullah Arif 
# COMP-4670 password cracking final project
import itertools
from RuleApplyer import *

def getFileInfo(filePath : str):
    file = open(filePath,"r+", encoding="utf-8")
    return file.read().splitlines()

def makeOutputFile(filePath : str):
    file = open(filePath,"w+", encoding="utf-8")
    return file

class passwordCracker:
    def __init__(self, inputPasswordFile : str, oFile : str):
        # I would try and catch error here but I want the program to crash if the input, output file are not set incorrectly
        self.passwordList = getFileInfo(inputPasswordFile)
        self.outputFile = makeOutputFile(oFile)

    def bruteForce(self, keyspace, max_length = 1 , rule = False, ruleList = None):
        # ** change keySpace to point to file which program will get
        numCracked = 0
        print("running brute Force")
        for i in range( max_length ):
            # attempt for a given length
            lengthAttempt = itertools.product(keyspace,repeat=i+1)
            if(rule):
                if(ruleList == None):
                    print("No rule file is set")
                else:
                    for ruleString in ruleList:
                        self.ruleEnhancer(ruleString, lengthAttempt)
                        lengthAttempt = itertools.product(keyspace,repeat=i+1)
                
                # do rule stuff
            else:
                for attempt in lengthAttempt:
                    possiblePassword = ''.join(attempt)
                    # print("Trying "+ possiblePassword)
                    for password in self.passwordList:
                        if possiblePassword == password:
                            print("Cracked: " + password)
                            numCracked += 1
                            self.outputFile.write(possiblePassword+"\n")
                            self.passwordList.remove(possiblePassword)
                        if 0 == len(self.passwordList):
                            print("All passwords cracked!")
                            return
    def maskAttack(self, mask: str,*customFileName ):     
        # ?b = 0x00 - 0xff -> not implemented
        print("running mask attack")
        numCracked = 0
        maskList =[]
        for i in range(0,len(mask),2):
            # print(mask[i:i+2])
            if(mask[i:i+2] == "?l"):  # lowercase= abcdefghijklmnopqrstuvwxyz
                maskList.append(getFileInfo("Resources/lowerCaseLetter.txt"))
            elif(mask[i:i+2] == "?u"): # uppercase = ABCDEFGHIJKLMNOPQRSTUVWXYZ
                maskList.append(getFileInfo("Resources/upperCaseLetter.txt"))
            elif(mask[i:i+2] == "?d"): # digits = 0123456789
                maskList.append(getFileInfo("Resources/digits.txt"))
            elif(mask[i:i+2] == "?h"):  # lower hex= 0123456789abcdef
                digitList =getFileInfo("Resources/digits.txt") 
                maskList.append(digitList.extend(getFileInfo("Resources/lowerHex.txt")))
            elif(mask[i:i+2] == "?H"):# upper hex= 0123456789ABCDEF
                digitList =getFileInfo("Resources/digits.txt") 
                maskList.append(digitList.extend(getFileInfo("Resources/upperHex.txt")))
            elif(mask[i:i+2] == "?s"): # space+punctuation = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                spaceList = getFileInfo("Resources/spaces.txt") 
                maskList.append(spaceList.extend(getFileInfo("Resources/punctuation.txt")))
            elif(mask[i:i+2] == "?a"): # all ascii printable =all printable
                maskList.append(getFileInfo("Resources/printable.txt"))
            else:
                for i in range(10):
                    try:
                        if(mask[i:i+2] == ("?"+i)):
                            maskList.append(getFileInfo("Resources/"+customFileName[i]+".txt"))
                    except:
                        print("File could not be retrieved for custom set " + str(i) +"please enter valid custom file name\n")
        s = ""
        variableList = getFileInfo("Resources/allLetter.txt")
        for i in range(len(maskList)):
            s += "for " + variableList[i%len(variableList)]*((i//len(variableList)+1)) + " in maskList["+str(i)+"]:\n\t"
            s += "\t"*i
        s += "possiblePassword = "
        for i in range(len(maskList)):
            s += variableList[i%len(variableList)]*((i//len(variableList)+1))
            if(i != len(maskList)-1):
                s += " + "
        s += "\n"
        s += "\t"*(len(maskList))  
        s += "for password in self.passwordList:\n\t"
        s += "\t"*len(maskList)
        # s += "print(password)\n\t"
        # s += "\t"*len(maskList)
        s += "if possiblePassword == password:\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "numCracked += 1\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "self.outputFile.write(possiblePassword+'\\n')\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "self.passwordList.remove(possiblePassword)\n\t"
        s += "\t"*len(maskList)
        s += "if 0 == len(self.passwordList):\n\t"
        s += "\t"*(len(maskList)+1)
        s += 'print("All passwords cracked!")\n\t'
        s += "\t"*(len(maskList)+1)
        s += "exit()\n\t"
        # print(s)
        exec(s)
    # function applies rules to list of word and test against password
    def ruleEnhancer(self, ruleString : str, wordList : list) -> list: 
        # consume string depending on input 
        curString = ""
        ruleCounter = 0 #place in the char array
        ruleList = {
            ":": nothingString, # do nothing
            "l": lowerString, # lowercase   #
            "u": upperString, # upper case
            "c": capitalizeString,
            "C": invertCapitalize,
            "t": toggleString,
            "T": toggleStringAtPos
        }
        # handle rules that "eat more of the string"
        ruleCountList = {
            "T": 2
        }
        numCracked = 0 
        while ruleCounter < len(ruleString):
            rule = ruleString[ruleCounter] 
            ruleCounter += ruleCountList.get(rule, 1)
            for word in wordList:
                # what if someone's password is "invalid rule "and it gets cracked by an error O.O
                # func = ruleList.get(rule, lambda: print('Invalid'))
                # possiblePassword = func(''.join(word))

                func = ruleList.get(rule, lambda: print('Invalid'))                
                s = "func(''.join(word)"
                for i in range (ruleCounter - ruleCountList.get(rule, 1) + 1, ruleCounter):
                    s += ", " + str(ruleString[i])
                s += ")"
                # print(s)
                possiblePassword = eval(s)

                # print(possiblePassword)
                # Test all possible passwords
                for password in self.passwordList:
                    if possiblePassword == password:
                        print("Cracked: " + password)
                        numCracked += 1
                        self.outputFile.write(possiblePassword+"\n")
                        self.passwordList.remove(possiblePassword)
                    if 0 == len(self.passwordList):
                        print("All passwords cracked!")
                        return
            
                

# 
#
