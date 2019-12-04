# Abdullah Arif
# Hold all the function used for rule attacks 

# invert capitalizer makes the first character in a string  a lower case and makes the rest of the string upper-case

def invertCapitalize( curString :str) -> str:
	if len(curString) <2:
		return curString.lower()
	c = curString[0]
	curString = curString[1:]
	c = str(c).lower()
	curString = curString.upper()
	return c+ curString

def nothingString(curString :str) -> str:
	return curString

def lowerString(curString :str) -> str:
	return curString.lower()

def upperString(curString :str) -> str:
	return curString.upper()

def capitalizeString(curString :str) -> str:
	return curString.capitalize()

# switch cases for every letter in a string
def toggleString(curString :str) -> str:
	c = list(curString)
	for i in range(len(curString)):
		if(c[i]>='a' and c[i]<='z'):
			c[i] = c[i].upper()
		elif(c[i]>='A' and c[i]<='Z'):
			c[i] = c[i].lower()
	return "".join(c)

def charToInt( char : chr) -> int:
	n = 0 
	if(char>='0' and char<='9'):
		n = ord(char)-ord('0')
	elif((char>='A' and char<='Z')):
		n = ord(char)-ord('A')+10 
	elif((char>='a' and char<='z')):
		n = ord(char)-ord('a')+36
	return n
# swap cases at position i, negative position would wrap around if user somehow broke program and inputed a negative value... A-Z represent number 10-35, a-z is 36 and beyond
def toggleStringAtPos(curString :str, p : chr) -> str:
	pos = charToInt(p)
	c = list(curString)
	if(pos < len(curString)):
		if(c[pos]>='a' and c[pos]<='z'):
			c[pos] = c[pos].upper()
		elif(c[pos]>='A' and c[pos]<='Z'):
			c[pos] = c[pos].lower()
	return "".join(c) # if position is located out of string then don't change string

#reverse the string
def reverseString(curString : str)  -> str:
	c = list(curString)
	for i in range(0, len(curString)//2):
		temp = c[i]
		c[i] = c[-1-i]
		c[-1-i] = temp
	return "".join(c)

# duplicate string
def duplicateStringNtimes(curString : str, n: chr) -> str:
	num = charToInt(n)
	return curString *num

# make the string appear twice
def duplicateString(curString : str,) -> str:
	return curString *2

#reflect string so something like password will become passworddrowssap
def reflectString(curString : str,) -> str:
	return curString  + reverseString(curString)

# rotate string to the left e.g string -> trings
def rotateLeftString(curString : str,) -> str:
	if(len(curString)>2):
		c = curString[0] # get first character
		curString = curString[1:] #delete first character
		curString += c # append first character to end of string
	return curString

# rotate string to the right e.g string -> gstrin
def rotateRightString(curString : str,) -> str:
	c = curString
	if(len(curString)>2):
		c = curString[-1] # get last character
		curString = curString[:-1] #delete last character
		c += curString # append string to last character
	return c

# append character - add to end of string
def appendCharacter(curString : str, char: chr) -> str:
	curString += str(char)
	return curString

# prepend Character -add to start of string
def prependCharacter(curString : str, char: chr) -> str:
	curString = str(char) + curString
	return curString

# delete first character
def truncateLeft(curString : str,) -> str:
	if(len(curString)<2):
		return ""
	return curString[1:]

#delete last character
def truncateRight(curString : str) -> str:
	if(len(curString)<2):
		return ""
	return curString[:-1]

def deleteAtPos(curString : str, p : chr) -> str:
	pos = charToInt(p)
	if(pos < len(curString)):
		leftString = curString[:pos]
		if(pos != len(curString)-1):
			rightString = curString[pos+1:]
		else:
			rightString = ""
		curString =  leftString + rightString
	return curString
#for ranges cap at length of string
def extractSubstring(curString : str, startPos : chr, endPos : chr) -> str:
	sPos = max(0,charToInt(startPos))
	ePos = min(charToInt(endPos), len(curString))
	if(sPos>ePos):
		raise Exception("Error starting position cannot come after ending position")
	return curString[sPos:ePos]

def omitSubstring(curString : str, startPos : chr, endPos : chr) -> str:
	sPos = charToInt(startPos)
	ePos = charToInt(endPos)+1
	if(sPos>len(curString)): 
		return curString
	if(sPos>ePos):
		raise Exception("Error starting position cannot come after ending position")
	leftString = ""
	rightString = ""
	if(sPos > 0):
		leftString = curString[:sPos]
	if(ePos < len(curString)):
		rightString = curString[ePos:]
	return leftString + rightString

#in-case it is out of range it doesn't add in character -> could make it so if out range it can add to end
def insertCharacterAtPos(curString : str, p : chr, char : chr) -> str:
	pos = charToInt(p)
	if(pos < len(curString)):
		leftString = curString[:pos]
		rightString = curString[pos:]
		curString = leftString + str(char) + rightString
	if(pos == len(curString)):
		curString += str(char)
	return curString

def overwriteCharacterAtPos(curString : str, p : chr, char : chr) -> str:
	pos = charToInt(p)
	if(pos < len(curString)):
		leftString = curString[:pos]
		if(pos != len(curString)-1):
			rightString = curString[pos+1:]
		else:
			rightString = ""
		curString =  leftString + str(char) + rightString
	return curString

# delete anything that comes after the given index
def truncateFromPos(curString : str, p : chr) -> str:
	pos = charToInt(p)
	if(pos < len(curString)):
		curString = curString[:pos]
	return curString

# could  have used string.replace(x,y)
def replaceCharacter (curString : str, target : chr, replacement: chr) -> str:
	c = list(curString)
	for i in range(len(curString)):
		if(c[i] == target):
			c[i] = replacement
	return "".join(c)

def purgeString(curString : str, target : chr) -> str:
	return replaceCharacter(curString, target, '')

def duplicateFirst(curString : str, n : chr) -> str:
	if(len(curString)>1): #handle empty string
		first = curString[0]
		num = charToInt(n)
		first *= num
		curString = first + curString
	return curString
def duplicateLast(curString : str, n : chr) -> str:
	if(len(curString)>1): #handle empty string
		last = curString[-1]
		num = charToInt(n)
		last *= num
		curString += last 
	return curString

# The reason I used array instead of strings because string concatenation takes big O(K+L) time where k is the length of the first string and l is the length of the second string
def duplicateAll(curString : str) -> str:
	s = []
	for c in curString:
		s.append(c)
		s.append(c)
	return "".join(s)

# class to deal with for rules with memory
class MemoryRules:
	memoryList = []
	@staticmethod
	def setMemory(curString : str):
		MemoryRules.memoryList.append(curString)
		return curString
	
	# Take the word in memory from position N till N+M and insert that position i in current word
	@staticmethod
	def extractMemory(curString : str, sPos : chr, lenOfMem : chr, insertP: chr) -> str:
		if(len(MemoryRules.memoryList)==0):
			print("Nothing in memory. Something went wrong :(")
		else:
			memory = MemoryRules.memoryList.pop(0)
			startPos = charToInt(sPos)
			lengthOfMemory = min(charToInt(lenOfMem), len(memory) -startPos)
			if(lengthOfMemory > 0 ): # handles if startPos is less than 0 or if length of memory is 0
				insertPosition = charToInt(insertP)
				insertWord = memory[startPos: startPos+lengthOfMemory]
				leftString = curString[:insertPosition]
				rightString = curString[insertPosition:]
				curString = leftString + insertWord + rightString
		return curString
	
	@staticmethod
	def appendMemory(curString : str) -> str:
		if(len(MemoryRules.memoryList)==0):
			print("Nothing in memory. Something went wrong :(")
		else:
			curString += MemoryRules.memoryList.pop(0)
		return curString
	
	@staticmethod
	def prependMemory(curString : str) -> str:
		if(len(MemoryRules.memoryList)==0):
			print("Nothing in memory. Something went wrong :(")
		else:
			curString = MemoryRules.memoryList.pop(0) +curString
		return curString

# rule list kind of work like a quick filter
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

