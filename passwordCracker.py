# COMP-4670 password cracking final project
import itertools
from RuleApplyer import *
from urllib.request import urlopen, hashlib
import hashlib
import bcrypt

def getFileInfo(filePath : str):
    file = open(filePath,"r+", encoding="utf-8")
    return file.read().splitlines()


class passwordCracker:
    #static variable for the different types of hashes
    NO_HASH = 0
    SHA1 = 1
    MD5 = 2
    BCRYPT = 3

    def __init__(self, inputPasswordFile : str, oFile : str):
        # I would try and catch error here but I want the program to crash if the input, output file are not set incorrectly
        self.passwordList = getFileInfo(inputPasswordFile)
        self.outputFile = open(oFile,"w+", encoding="utf-8")
        self.hashNumber = passwordCracker.NO_HASH #default is to use plain-text
        self.verbose = False #default is singular attacks so we don't need to verbose the attempts
        self.appendMask = []
        self.prependMask = []
        self.ruleList = []
        self.numCracked = 0

    # set the program to check for the given hashes
    def setHashNum(self, num : int):
        self.hashNumber = num

    # verbose mode prints out every attempt the program makes
    def setVerboseMode(self, verboseMode: bool):
        self.verbose = verboseMode

    def getWord(self, word : str):
        if(self.verbose):
            print(word+"\n")
        if(self.hashNumber == passwordCracker.SHA1):
            return hashlib.sha1(bytes(word, 'utf-8')).hexdigest()
        if(self.hashNumber == passwordCracker.MD5):
            return hashlib.md5(bytes(word, 'utf-8')).hexdigest()
        return word
    
    def setAppendMask(self, am: str):
        self.appendMask = am

    def setPrependMask(self, pm: str):
        self.prependMask = pm

    def setRuleList(self,rl: list):
        self.ruleList = rl 

    def checkMask(self,plainTextPassword) -> bool:
        if(len(self.appendMask) == 0 and len(self.prependMask) == 0):
            return False
        if(len(self.appendMask) != 0): # apply mask to end
            self.maskAttack(self.appendMask, plainTextPassword)             
        if (len(self.prependMask) != 0 ):
            self.maskAttack(self.prependMask, "", plainTextPassword)
        return True

    def ruleAttack(self, keyspace,  min_length = 0, max_length = 1) -> bool:
        for i in range( min_length ,max_length ):
            for ruleString in self.ruleList:
                lengthAttempt = itertools.product(keyspace,repeat=i+1)
                self.ruleEnhancer(ruleString, lengthAttempt)
            if 0 == len(self.passwordList):
                return True
        return False
    def endingPrompt(self) -> str:
        if 0 == len(self.passwordList):
            return "All passwords cracked!"
        return "Finished cracker. Could not find all passwords:("
    def passwordCheck(self, plainTextPassword):   
        possiblePassword = self.getWord(plainTextPassword)     
        for password in self.passwordList:
            # add in check for bcrypt
            if self.comparePassword(possiblePassword, password):
                print("Cracked: " + plainTextPassword)
                self.numCracked += 1
                self.outputFile.write(plainTextPassword+"\n")
                self.passwordList.remove(password)
            if 0 == len(self.passwordList):
                return True
        return False
    # for some hashes we can't just straight compare passwords
    def comparePassword(self, possiblePassword, password) -> bool:
        if(self.hashNumber == passwordCracker.BCRYPT):
            try:
                return  bcrypt.checkpw(possiblePassword.encode('utf-8'), password.encode('utf-8'))
            except ValueError as e:
                print("Not in BCRYPT form")
                return False     
        return possiblePassword == password 
    
    # straight brute force with no rules
    def normalBruteForce(self, keyspace,  min_length = 0, max_length = 1) -> bool: #return if finished
        for i in range( min_length ,max_length ):
            lengthAttempt = itertools.product(keyspace,repeat=i+1)
            for attempt in lengthAttempt:
                plainTextPassword = ''.join(attempt)
                if not self.checkMask(plainTextPassword):
                    if(self.passwordCheck(plainTextPassword)):
                        return True
        return False
    
    def bruteForce(self, keyspace,  min_length = 0, max_length = 1 ):        
        min_length = min(0,min_length) #min_length can't be less than 0
        print("running brute Force")
        if(len(self.ruleList) != 0):
            self.ruleAttack(keyspace,min_length,max_length)
        else:
            self.normalBruteForce(keyspace,min_length,max_length)

    def createMaskList(self, mask: str, *customFileName) -> list:
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
        return maskList
    
    def createMaskScript(self, maskList:list, prefix = "", suffix = "") -> str:
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
        s += "if(self.passwordCheck(prefix + plainTextPassword + suffix)):\n\t"
        s += "\t"*len(maskList)
        s += "exit()\n\t"
        # print(s) # for testing print out python code to execute 
        return s
    def maskAttack(self, mask: str, prefix = "", suffix = "",*customFileName ):     
        # ?b = 0x00 - 0xff -> not implemented
        print("running mask attack")        
        maskList =  self.createMaskList(mask, customFileName) # turn mask into character     
        exec(self.createMaskScript(maskList,prefix, suffix)) # execute created python script 
    
    # function applies rules to list of word and test against password
    # Note: starting position is inclusive and ending position is exclusive for all ranges
    def ruleEnhancer(self, ruleString : str, wordList : list) -> list: 
        # set up variables
        ruleCounter = 0 #place in the hypothetical rule array represented by the ruleString       
        # start applying rules
        while ruleCounter < len(ruleString):
            rule = ruleString[ruleCounter] 
            ruleCounter += ruleCountList.get(rule, 1)
            nextWordList=[]
            for word in wordList:
                # what if someone's password is "invalid rule "and it gets cracked by an error O.O
                func = ruleList.get(rule, lambda: print('Invalid rule'))                
                s = "func(''.join(word)"
                for i in range (ruleCounter - ruleCountList.get(rule, 1) + 1, ruleCounter):
                    s += ",'" + str(ruleString[i]) + "'"
                s += ")"
                # print(s)
                plainTextPassword = eval(s)
                if not self.checkMask(plainTextPassword):
                    if(ruleCounter<len(ruleString)): # if we need to know password to chain 
                    # ** for large rules it might be better to write to file and read back from it  
                        nextWordList.append(plainTextPassword)
                    # Test all possible passwords against all passwords to crack
                    if(self.passwordCheck(plainTextPassword)):
                        return True
                        
                    wordList = nextWordList             