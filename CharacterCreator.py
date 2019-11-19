# Abdullah Arif
# Create a file with list of characters to use for the main password cracker program
import string

# class CharacterCreator:
# 	@staticmethod
def createFile(fileName : str, wordList: list):
	if(fileName.find(".txt")==-1):
		fileName+=".txt"
		print("appended .txt to make file a text file")
	with open("Resources/"+fileName, "w", encoding="utf-8") as file: 
		for word in wordList:
			file.write(word+"\n")

def createLower():
	createFile("lowerCaseLetter",string.ascii_lowercase)
def createUpper():
	createFile("upperCaseLetter",string.ascii_uppercase)
def createAllLetters():
	createFile("allLetter",string.ascii_letters)
def createDigits():
	createFile("digits",string.digits)
def createPunctuation():
	createFile("punctuation",string.punctuation)
def createSpaces():
	createFile("spaces",string.whitespace)
def createPrintableAscii():
	createFile("printable",string.printable)

# let users pick their own range
def createCustomRange(fileName: str,low: int, high: int):
	createFile(fileName, [chr(i) for i in range(low,high)])
#set up the basic classes for the program to use 
def createAllBasic():
	createLower()
	createUpper()
	createAllLetters()
	createDigits()
	createSpaces()
	createPunctuation()
	createPrintableAscii()
	createCustomRange("upperHex",65,71)
	createCustomRange("lowerHex",97,103)

createAllBasic()



    