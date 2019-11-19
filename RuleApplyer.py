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

def toggleString(curString :str) -> str:
	s = ""
	for c in curString:
		if(c>='a' and c<='z'):
			s += c.upper()
		elif(c>='A' and c<='Z'):
			s += c.lower()
		else:
			s += c
	return s

def toggleStringAtPos(curString :str, pos : int) -> str:
	if(pos < len(curString)):
		c = list(curString)
		s = c[pos]
		if(s>='a' and s<='z'):
			s = s.upper()
		elif(s>='A' and s<='Z'):
			s = s.lower()
		c[pos] = s
		curString = "".join(c)
	return curString # if position is located out of string then don't change string

