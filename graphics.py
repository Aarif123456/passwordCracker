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
menuCSS = '''
QPushButton#StyledButton[Test=true] {...}
'''
# # open up and 
class Menu(QWidget):
    BRUTE_FORCE = 0
    MASK    = 1
    USE_RULE = 0

    def __init__(self):
        super().__init__()
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

    def openMenu(self):
        # set up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Password Cracker')    

        # set up the main window in grid form
        layout = QGridLayout()
        self.setLayout(layout)

        #Make the main menu radio buttons
        # set one group for all password methods
        methodGroup = QButtonGroup()
        #brute force option
        radiobutton = QRadioButton("Brute-force or dictionary attack")
        radiobutton.setChecked(True)
        radiobutton.methodNum = Menu.BRUTE_FORCE
        methodGroup.addButton(radiobutton, 0)
        radiobutton.toggled.connect(self.selectAttackMode)
        layout.addWidget(radiobutton, 0, 0)

        # Check-box to add option to add to dictionary attack
        self.optionBox = QCheckBox("Customize Attack attack")
        self.optionBox.toggled.connect(self.toggleMenu)
        layout.addWidget(self.optionBox , 1, 0)

        #mask option
        radiobutton = QRadioButton("Mask attack")
        radiobutton.methodNum = Menu.MASK
        methodGroup.addButton(radiobutton, 1)
        radiobutton.toggled.connect(self.selectAttackMode)
        layout.addWidget(radiobutton, 0, 1)
        
        # button to open input file
        btn = QPushButton('', self)
        btn.setIcon(QIcon('Resources/Images/open.png'))
        btn.setIconSize(QSize(24,24))
        btn.setToolTip('Open up the input file that the program will use to crack the passwords')
        btn.clicked.connect(lambda:self.file_open("Input"))
        btn.resize(btn.sizeHint())
        btn.move(50, 50)               

        # Create togglable menu -> Nest layout in frame because you can control when to show and when to hide
        # frame = QFrame()
        # bruteForceMenu = QGridLayout()

        bruteForceGroup = QButtonGroup()
        # Option to apply rules
        self.ruleMenu = QRadioButton("Rules")
        self.ruleMenu.setProperty('Hide', True)
        btn.setObjectName('BruteforceOption')
        self.ruleMenu.optionNum = Menu.USE_RULE
        bruteForceGroup.addButton(self.ruleMenu, 1)
        self.ruleMenu.toggled.connect(self.selectAttackMode)
        bruteForceMenu.addWidget(self.ruleMenu, 0, 0)

        #store hidden layout in frame
        # frame.setLayout(bruteForceMenu)
        

        # self.addWidget(frame) # add to bruteForce menu to main window
        # frame.hide()
        # frame.show()

    #testing **
    def selectAttackMode(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            print("Method is %d" % (radiobutton.methodNum ))
    
    def toggleMenu(self):
        if(self.optionBox.isChecked()):
            print("Show Menu")
        else:
            print("Hide Menu")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Menu()
    screen->setStyleSheet(menuCSS)
    screen.show()
    sys.exit(app.exec_())


