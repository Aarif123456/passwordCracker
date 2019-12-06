# Abdullah Arif 
# COMP-4670 password cracking final project
# main menu for password cracker

from passwordCracker import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

menuCSS = """"

"""

# Open Menu window
class Menu(QWidget):
    BRUTE_FORCE = 0
    MASK    = 1
    USE_RULE = 0

    def __init__(self):
        super().__init__()
        # set up all the default variable to be used in password cracker
        self.inputFile = "" # input file holds path to file with password or hash to crack
        self.outputFile = "" # output file will be the file where the passwords are printed
        self.mode = Menu.BRUTE_FORCE # by default will use brute force method
        # file that contains the words for the dictionary attack to run or masks for the masks attack
        self.methodInput = "" 
        self.rules = "" #holds path to the file with rules
        self.appendMask = "" #hold the mask that will be applied to end of brute force
        self.prependMask = "" #hold the mask that will be applied to start of brute force
        self.openMenu()

    
    def fileOpen(self, path = 'Input'):
        fileDialog = QFileDialog()
        filePath = QFileDialog.getOpenFileName(fileDialog, 'Open File', path, "Text files (*.txt)")
        try:
            with open(filePath[0],"r+", encoding="utf-8") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("ERROR: could not open file")
            return ""

    def fileSelectInput(self, path = 'Input'):
        if(self.methodInput == ""):
            self.methodInput = self.fileOpen("Input/Recommended")
            if(self.methodInput != ""):
                  pass # change to X icon ** 
        else:
            self.methodInput = ""
            # change box to back to open icon **

    def openMenu(self):
        # self.setStyleSheet(menuCSS)
        # set up window
        self.setGeometry(200, 20, 200, 500)
        self.setWindowTitle('Password Cracker')    

        # set up the main window in grid form
        layout = QGridLayout()
        self.setLayout(layout)

        #Make the main menu radio buttons
        # set one group for all password methods
        methodGroup = QButtonGroup()
        #brute force option
        radiobutton = QRadioButton("Brute-force attack")
        radiobutton.setToolTip('Select to do either brute-force or dictionary attack!')
        radiobutton.setChecked(True)
        radiobutton.methodNum = Menu.BRUTE_FORCE
        methodGroup.addButton(radiobutton, 0)
        radiobutton.toggled.connect(self.selectAttackMode)
        layout.addWidget(radiobutton, 0, 0)

        #mask option
        radiobutton = QRadioButton("Mask attack")
        radiobutton.methodNum = Menu.MASK
        methodGroup.addButton(radiobutton, 1)
        radiobutton.toggled.connect(self.selectAttackMode)
        layout.addWidget(radiobutton, 0, 1)
        
        # button to open input file
        btn = QPushButton('', self)
        btn.setIcon(QIcon('Resources/Images/fileuse.png'))
        btn.setIconSize(QSize(240,35))
        btn.setStyleSheet('QPushButton{border: 0px solid;}')
        btn.setToolTip('Open up the input file that the program will use to crack the passwords')
        btn.clicked.connect(lambda: self.fileSelectInput("Input"))
        btn.resize(btn.sizeHint())
        layout.addWidget(btn, 0, 2,1,2)       

        # Togglable options for dictionary attack
        # Check-box to add rules to add to dictionary attack
        self.ruleBox = QCheckBox("Add Rules")
        self.ruleBox.toggled.connect(self.toggleRules)
        layout.addWidget(self.ruleBox , 1, 0)

        # Check-box to append a mask to add to dictionary attack
        self.maskAppendBox = QCheckBox("Append Mask")
        self.maskAppendBox.toggled.connect(self.toggleAppendMask)
        layout.addWidget(self.maskAppendBox , 1, 1)

        # Check-box to append a mask to add to dictionary attack
        self.maskPrependBox = QCheckBox("Prepend Mask")
        self.maskPrependBox.toggled.connect(self.togglePrependMask)
        layout.addWidget(self.maskPrependBox , 1, 2)

        # validate input for text box
        # self.onlyInt = QIntValidator()
        self.minBoxLabel = QLabel(self)
        self.minBoxLabel.setText("Min")
        self.minBoxLabel.setAlignment(Qt.AlignRight)
        layout.addWidget(self.minBoxLabel, 2, 0)

        self.minBox = QSpinBox(self)
        self.minBox.setRange(0,10)
        # self.minBox.setValidator(self.onlyInt)
        layout.addWidget(self.minBox , 2, 1)

        self.maxBoxLabel = QLabel(self)
        self.maxBoxLabel.setText("Max")
        self.maxBoxLabel.setAlignment(Qt.AlignRight)
        layout.addWidget(self.maxBoxLabel, 2, 2)

        self.maxBox = QSpinBox(self)
        self.maxBox.setValue(1)
        self.maxBox.setRange(0,10)
        
        layout.addWidget(self.maxBox , 2, 3)        

        self.hashBox = QCheckBox("Hash mode")
        layout.addWidget(self.hashBox , 3, 0)

        self.rainbowBox = QCheckBox("Verbose mode")
        layout.addWidget(self.rainbowBox , 3, 1)

        self.hashDropdown = QComboBox(self)
        self.hashDropdown.addItem("SHA1", QVariant(passwordCracker.SHA1))
        self.hashDropdown.addItem("MD5", QVariant(passwordCracker.MD5))
        self.hashDropdown.addItem("bcrypt", QVariant(passwordCracker.BCRYPT))
        layout.addWidget(self.hashDropdown , 3, 2, 1, 2)
        
        # ** USE save file mode instead of open
        self.inputBtn = QPushButton('', self)
        self.inputBtn.setIcon(QIcon('Resources/Images/filepw.png'))
        self.inputBtn.setIconSize(QSize(240,35))
        self.inputBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.inputBtn.setToolTip('Select file with all the passwords or hashes that you want to crack ')
        self.inputBtn.clicked.connect(self.getInputFile)
        layout.addWidget(self.inputBtn, 4, 0, 1, 2)

        self.outputBtn = QPushButton('', self)
        self.outputBtn.setIcon(QIcon('Resources/Images/savepw.png'))
        self.outputBtn.setIconSize(QSize(240,35))
        self.outputBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.outputBtn.setToolTip('Select file that will store the cracked passwords ')
        self.outputBtn.clicked.connect(self.getOutputFile)
        layout.addWidget(self.outputBtn, 4, 2, 1, 2)

        self.startBtn = QPushButton('', self)
        self.startBtn.setIcon(QIcon('Resources/Images/crackpw.png'))
        self.startBtn.setIconSize(QSize(260,45))
        self.startBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.startBtn.clicked.connect(self.startCrack)
        self.outputBtn.setToolTip('Select folder to save password to')
        layout.addWidget(self.startBtn , 5, 0, 1, 4)
        
    def selectAttackMode(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            if(radiobutton.methodNum == Menu.BRUTE_FORCE):
                self.ruleBox.setVisible(True)
                self.maskAppendBox.setVisible(True)
                self.maskPrependBox.setVisible(True)
                self.minBoxLabel.setVisible(True)
                self.minBox.setVisible(True)
                self.maxBoxLabel.setVisible(True)
                self.maxBox.setVisible(True)

            if(radiobutton.methodNum == Menu.MASK):
                self.ruleBox.setVisible(False)
                self.maskAppendBox.setVisible(False)
                self.maskPrependBox.setVisible(False)
                self.minBoxLabel.setVisible(False)
                self.minBox.setVisible(False)
                self.maxBoxLabel.setVisible(False)
                self.maxBox.setVisible(False)
    
    def toggleRules(self):
        if(self.ruleBox.isChecked()):
            self.rules = self.fileOpen("Input/Recommended/Rules")
            if(self.rules == ""):
                self.ruleBox.setChecked(False) 
        else:
            self.rules = ""

    def toggleAppendMask(self):
        if(self.maskAppendBox.isChecked()):
            self.appendMask = self.fileOpen("Input/Recommended/Mask")
            if(self.appendMask == ""):
                self.maskAppendBox.setChecked(False) 
        else:
            self.appendMask = ""
    def togglePrependMask(self):
        if(self.maskPrependBox.isChecked()):
            self.prependMask = self.fileOpen("Input/Recommended/Mask")
            if(self.prependMask == ""):
                self.maskPrependBox.setChecked(False) 
        else:
            self.prependMask = ""

    def getHashMode(self):
        hashMode = 0
        if(self.hashBox.isChecked()):
            hashMode = self.hashDropdown.currentData()
        return hashMode
    
    def getInputFile(self):
        fileDialog = QFileDialog()
        filePath = QFileDialog.getOpenFileName(fileDialog, 'Open File', 'Input/TargetFile', "Text files (*.txt)")
        self.inputFile = filePath[0]

    def getOutputFile(self):
        fileDialog = QFileDialog()
        filePath= QFileDialog.getSaveFileName(fileDialog, 'Open File', 'Output', "Text files (*.txt)")
        self.outputFile = filePath[0]

    def startCrack(self):      
        if(self.inputFile == ""):
            print("You need to select input file that contains the files to crack")
            return
        if(self.outputFile == ""):
            print("You must select an output file where the cracked passwords will be saved")
            return
        if(self.methodInput == "" ):
            print("You must have an input file for the method")
            return
        cracker = passwordCracker(self.inputFile, self.outputFile)
        cracker.setVerboseMode(self.rainbowBox.isChecked())
        if(self.mode == Menu.BRUTE_FORCE):
            cracker.setRuleList(self.rules)
            cracker.setPrependMask(self.prependMask)
            cracker.setAppendMask(self.appendMask)
            cracker.setHashNum(self.getHashMode())
            # if(self.hashBox.isChecked()  and self.rainbowBox.isChecked()):
            #     pass # use this to run on-line hash check ***
            # Brute force stuff
            cracker.bruteForce(self.methodInput , int(self.minBox.value()), int(self.maxBox.value()))
        else:
            cracker.maskAttack(self.methodInput)
            # mask stuff
        print(cracker.endingPrompt())

        # Look at different option like input file/output file, rules file and so on 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Menu()
    screen.show()
    sys.exit(app.exec_())
