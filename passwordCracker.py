# COMP-4670 password cracking final project
import itertools
from RuleApplyer import *
from urllib.request import urlopen, hashlib
import hashlib
#   import bcrypt

def getFileInfo(filePath : str):
    file = open(filePath,"r+", encoding="utf-8")
    return file.read().splitlines()

def makeOutputFile(filePath : str):
    file = open(filePath,"w+", encoding="utf-8")
    return file

class passwordCracker:
    #static variable for the different types of hashes
    NOHASH = 0
    SHA1 = 1
    MD5 = 2
    def __init__(self, inputPasswordFile : str, oFile : str):
        # I would try and catch error here but I want the program to crash if the input, output file are not set incorrectly
        self.passwordList = getFileInfo(inputPasswordFile)
        self.outputFile = makeOutputFile(oFile)
        self.hashNumber = 0 #default is to use plain-text
        self.verbose = False #default is singular attacks so we don't need to verbose the attempts

    # set the program to check for the given hashes
    def setHashNum(self, num : int):
        self.hashNumber = num

    def setVerboseMode(self, verboseMode: bool):
        self.verbose = verboseMode

    def getWord(self, word : str):
        if(self.verbose):
            print(word+"\n")
        if(self.hashNumber == passwordCracker.NOHASH):
            return word
        if(self.hashNumber == passwordCracker.SHA1):
            return hashlib.sha1(bytes(guess, 'utf-8')).hexdigest()
        if(self.hashNumber == passwordCracker.MD5):
            return hashlib.md5(bytes(guess, 'utf-8')).hexdigest()

    def bruteForce(self, keyspace,  min_length = 0, max_length = 1 , rule = False, ruleList = None, appendMask = False, prependMask = False):
        numCracked = 0
        min_length = min(0,min_length) #min_length can't be less than 0
        print("running brute Force")
        for i in range( max_length ):
            # attempt for a given length
            lengthAttempt = itertools.product(keyspace,repeat=i+1)
            # apply rules
            if(rule):
                if(ruleList == None):
                    print("No rule file is set")
                else:
                    for ruleString in ruleList:
                        self.ruleEnhancer(ruleString, lengthAttempt)
                        lengthAttempt = itertools.product(keyspace,repeat=i+1)
            else:
                for attempt in lengthAttempt:
                    plainTextPassword = ''.join(attempt)
                    possiblePassword = self.getWord(plainTextPassword)
                    for password in self.passwordList:
                        if possiblePassword == password:
                            print("Cracked: " + plainTextPassword)
                            numCracked += 1
                            self.outputFile.write(plainTextPassword+"\n")
                            self.passwordList.remove(possiblePassword)
                        if 0 == len(self.passwordList):
                            print("All passwords cracked!")
                            return
    def maskAttack(self, mask: str, prefix = "", suffix = "",*customFileName ):     
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
        s += "plainTextPassword = "
        for i in range(len(maskList)):
            s += variableList[i%len(variableList)]*((i//len(variableList)+1))
            if(i != len(maskList)-1):
                s += " + "
        s += "\n"
        s += "\t"*(len(maskList))  
        s += "possiblePassword = prefix + self.getWord(plainTextPassword) + suffix\n"
        s += "\t"*(len(maskList))  
        s += "for password in self.passwordList:\n\t"
        s += "\t"*len(maskList)
        s += "if possiblePassword == password:\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "numCracked += 1\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "self.outputFile.write(plainTextPassword+'\\n')\n\t"
        s += "\t"*(len(maskList)+1)
        s +=  "self.passwordList.remove(possiblePassword)\n\t"
        s += "\t"*len(maskList)
        s += "if 0 == len(self.passwordList):\n\t"
        s += "\t"*(len(maskList)+1)
        s += 'print("All passwords cracked!")\n\t'
        s += "\t"*(len(maskList)+1)
        s += "exit()\n\t"
        # print(s) # for testing print out python code to execute 
        exec(s)
    
    # function applies rules to list of word and test against password
    # Note: starting position is inclusive and ending position is exclusive for all ranges
    def ruleEnhancer(self, ruleString : str, wordList : list) -> list: 
        ruleCounter = 0 #place in the hypothetical rule array represented by the ruleString
        ruleList = {
            ":": nothingString, # do nothing
            "l": lowerString, # lowercase   
            "u": upperString, # upper case
            "c": capitalizeString,
            "C": invertCapitalize,
            "t": toggleString,
            "T": toggleStringAtPos,
            "r": reverseString,
            "d": duplicateString,
            "p": duplicateStringNtimes,
            "f": reflectString,
            "{": rotateLeftString,
            "}": rotateRightString,
            "$": appendCharacter,
            "^": prependCharacter,
            "[": truncateLeft,
            "]": truncateRight,
            "D": deleteAtPos, 
            "x": extractSubstring, #extract substring from main string
            "O": omitSubstring,
            "i": insertCharacterAtPos, 
            "o": overwriteCharacterAtPos, 
            "'": truncateFromPos,  
            "s": replaceCharacter, 
            "@": purgeString,
            "z": duplicateFirst,
            "Z": duplicateLast,
            "q": duplicateAll,
            "M": MemoryRules.setMemory,
            "X": MemoryRules.extractMemory,
            "4": MemoryRules.appendMemory,
            "6": MemoryRules.prependMemory
        }
        # handle rules that have arguments
        ruleCountList = {
            "T": 2, # toggle at given position
            "p": 2, # duplicate n number of time
            "$": 2, # append the given character
            "^": 2, # prepend the given character
            "D": 2, # Delete at given position
            "x": 3, # get character in the given range if out of range get whole word
            "O": 3, # get rid of character is given range
            "i": 3, # iNX insert char X at position n
            "o": 3, # oNX overwrite character at position i with char X
            "'": 2, # truncate word after given index 
            "s": 3, # sXY - replace all instances of X with Y
            "@": 2, # second argument is character to purge
            "z": 2, # second argument is how many times first character will be duplicated
            "Z": 2, # second argument is how many times last character will be duplicated
            "X": 4,  # Insert substring of length M starting from position N of word saved to memory at position I
        }
        numCracked = 0 
        while ruleCounter < len(ruleString):
            rule = ruleString[ruleCounter] 
            ruleCounter += ruleCountList.get(rule, 1)
            nextWordList=[]
            for word in wordList:
                # what if someone's password is "invalid rule "and it gets cracked by an error O.O
                func = ruleList.get(rule, lambda: print('Invalid'))                
                s = "func(''.join(word)"
                for i in range (ruleCounter - ruleCountList.get(rule, 1) + 1, ruleCounter):
                    s += ",'" + str(ruleString[i]) + "'"
                s += ")"
                # print(s)
                plainTextPassword = eval(s)
                possiblePassword = self.getWord(plainTextPassword)
                if(ruleCounter<len(ruleString)): # if we need to know password to chain 
                    # ** for large rules it might be better to write to file and read back from it  
                    nextWordList.append(plainTextPassword)
                # Test all possible passwords against all passwords to crack
                for password in self.passwordList:
                    if possiblePassword == password:
                        print("Cracked: " + plainTextPassword)
                        numCracked += 1
                        self.outputFile.write(plainTextPassword+"\n")
                        self.passwordList.remove(possiblePassword)
                    if 0 == len(self.passwordList):
                        print("All passwords cracked!")
                        return
                wordList = nextWordList 

    def combinationAttack(self):
        pass

            