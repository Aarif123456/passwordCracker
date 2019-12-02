# Abdullah Arif 
# COMP-4670 password cracking final project
# main menu for password cracker

from passwordCracker import *
# Full program will implement basic GUI
# class passwordCrackingMenu:
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

def menu():
	# mode = int(input(''' 
	# 	choose your attack mode
	# 	1. password cracking -If you list passwords you want to check against attack
	# 	2. Hash cracking - If you have hashes for the password you wish to crack
	# 	3.On-line attack - If you have a website or server you would like to test
	# 	'''))
	# testing set mode ** currently password crack
	mode =1
	if(mode == 1):
		passwordCrackingMenu()
	if(mode == 2):
		hashCrackingMenu()
		# can have hash identifier too figure out what kind hash it is if you have time
	if(mode == 3):
		onlineAttackMenu()

def passwordCrackingMenu():
	print("Please choose your input file")
	# ** will make this activated by a button
	inputFileName = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
	#outputFile = input("Please type in the name of the file that will store your cracked password")
	# testing set file **
	outputFile = "o1"
	cracker = passwordCracker(inputFileName, "Output/"+ outputFile +".txt")

# 	mode = int(input(''' 
# choose your cracking method
# 1. Raw brute-force attack
# 2. Dictionary attack
# 3. Mask attack
# 4. Rule-based with dictionary
# 5. Combination'''))
	mode = 1
	if(mode == 1):
		#  get key space from file or one of the pre selected
		cracker.bruteForce("456789", 0,12)
	if(mode == 2):
		cracker.maskAttack("?l?l?u?a","","cat")
	if(mode == 3):
		# get rule File using Tkinter
		with open("Input/rule.txt","r+", encoding="utf-8") as ruleFile:
			cracker.bruteForce(['p','prat', 'p@ssW0rd'], 0,3, True,ruleFile.read().splitlines())
	if(mode == 4 ):
		# hybrid attack
		pass

	print("check output file for list of cracked password")
	# filename = filedialog.askopenfile(mode="r",title="Load",filetypes = fileFormats)

def hashCrackingMenu():
	pass
menu()