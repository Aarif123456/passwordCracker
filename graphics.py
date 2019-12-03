# Abdullah Arif 
# COMP-4670 password cracking final project
# main menu for password cracker

from passwordCracker import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# app = QApplication(sys.argv)
# # window = QMainWindow()
# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.resize(500, 400)
# # window.setCentralWidget(button)
# window.show()
# sys.exit(app.exec_())
menuCSS = """"

"""


# # open up and 
class Menu(QWidget):
    BRUTE_FORCE = 0
    MASK    = 1
    USE_RULE = 0

    def __init__(self):
        super().__init__()
        # set up all the default variable to be used in password cracker
        self.inputFile = "" # input file holds path to file with password or ash to crack
        self.outputFile = "" # output file will be the file where the passwords are printed
        self.mode = Menu.BRUTE_FORCE # by default will use brute force method
        # file that contains the words for the dictionary attack to run or masks for the masks attack
        self.methodInput= "" 
        self.rules = "" #holds path to the file with rules
        self.appendMask = "" #hold the mask that will be applied to end of brute force
        self.prependMask = "" #hold the mask that will be applied to start of brute force
        # by default we assume we are dealing with plain passwords
        self.hashMode = passwordCracker.NO_HASH  
        self.onlineHashCheck = False
        # testing
        self.setUpShortcuts()
        self.openMenu()

    #probably remove **
    def setUpShortcuts(self):
        # opening file test
        openFile = QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
    
    def file_open(self, path = 'Input'):
        fileDialog = QFileDialog()
        filePath = QFileDialog.getOpenFileName(fileDialog, 'Open File', path, "Text files (*.txt)")
        print(filePath[0])
        try:
            with open(filePath[0],"r+", encoding="utf-8") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("ERROR: could not open file")
        return ""

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
        btn.clicked.connect(lambda:self.file_open("Input"))
        btn.resize(btn.sizeHint())
        layout.addWidget(btn, 0, 2)       

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

        self.hashBox = QCheckBox("Hash mode")
        self.hashBox.toggled.connect(self.toggleHashMode)
        layout.addWidget(self.hashBox , 2, 0)

        self.rainbowBox = QCheckBox("Rainbow check")
        self.rainbowBox.toggled.connect(self.toggleOnlineHash)
        layout.addWidget(self.rainbowBox , 2, 1)

        self.hashDropdown = QComboBox(self)
        self.hashDropdown.addItem("SHA1")
        self.hashDropdown.addItem("MD5")
        self.hashDropdown.addItem("bcrypt")
        self.hashDropdown.currentIndexChanged.connect(self.toggleHashMode)
        layout.addWidget(self.hashDropdown , 2, 2,1 , 2)
        
        # ** USE save file mode instead of open
        self.inputBtn = QPushButton('', self)
        self.inputBtn.setIcon(QIcon('Resources/Images/filepw.png'))
        self.inputBtn.setIconSize(QSize(240,35))
        self.inputBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.inputBtn.setToolTip('Select file with all the passwords or hashes that you want to crack ')
        self.inputBtn.toggled.connect(self.getInputFile)
        layout.addWidget(self.inputBtn , 3, 1)

        self.outputBtn = QPushButton('', self)
        self.outputBtn.setIcon(QIcon('Resources/Images/savepw.png'))
        self.outputBtn.setIconSize(QSize(240,35))
        self.outputBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.outputBtn.setToolTip('Select file that will store the cracked passwords ')
        self.outputBtn.toggled.connect(self.getOutputFile)
        layout.addWidget(self.outputBtn , 3, 2)

        self.startBtn = QPushButton('', self)
        self.startBtn.setIcon(QIcon('Resources/Images/crackpw.png'))
        self.startBtn.setIconSize(QSize(240,35))
        self.startBtn.setStyleSheet('QPushButton{border: 0px solid;}')
        self.startBtn.toggled.connect(self.startCrack)
        self.outputBtn.setToolTip('Select folder to save password to')
        layout.addWidget(self.startBtn , 4, 1, 1, 2)

        
    def selectAttackMode(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            if(radiobutton.methodNum == Menu.BRUTE_FORCE):
                self.ruleBox.setVisible(True)
                self.maskAppendBox.setVisible(True)
                self.maskPrependBox.setVisible(True)
            if(radiobutton.methodNum == Menu.MASK):
                self.ruleBox.setVisible(False)
                self.maskAppendBox.setVisible(False)
                self.maskPrependBox.setVisible(False)
    
    def toggleRules(self):
        pass
    def toggleAppendMask(self):
        pass
    def togglePrependMask(self):
        pass
    def toggleHashMode(self):
        pass
    def toggleOnlineHash(self):
        pass
    def getInputFile(self):
        pass
    def getOutputFile(self):
        pass
    def startCrack(self):
        pass
        # Look at different option like input file/output file, rules file and so on 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Menu()
    screen.show()
    sys.exit(app.exec_())


