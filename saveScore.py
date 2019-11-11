import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt
from operator import itemgetter


class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        #self.showScoreDB()


    def initUI(self):
        self.setGeometry(300, 300, 600, 350)
        self.setWindowTitle('SaveScoreProgram')

        vbox = QVBoxLayout()

        #1st QHBoxLayout
        nameLabel = QLabel("Name: ")
        self.nameEdit = QLineEdit(self)
        ageLabel = QLabel("Age: ")
        self.ageEdit = QLineEdit(self)
        scoreLabel = QLabel("Score: ")
        self.scoreEdit = QLineEdit(self)
        firsthbox = QHBoxLayout()
        firsthbox.addStretch(1)
        firsthbox.addWidget(nameLabel)
        firsthbox.addWidget(self.nameEdit)
        firsthbox.addWidget(ageLabel)
        firsthbox.addWidget(self.ageEdit)
        firsthbox.addWidget(scoreLabel)
        firsthbox.addWidget(self.scoreEdit)
        vbox.addLayout(firsthbox)

        #2nd QHBoxLayout
        amountLabel = QLabel("Amount: ")
        self.amountEdit = QLineEdit(self)
        keyLabel = QLabel("key: ")
        self.keyCombo = QComboBox(self)
        self.keyCombo.addItem("Name")
        self.keyCombo.addItem("Age")
        self.keyCombo.addItem("Score")
        secondbox = QHBoxLayout()
        secondbox.addStretch(1)
        secondbox.addWidget(amountLabel)
        secondbox.addWidget(self.amountEdit)
        secondbox.addWidget(keyLabel)
        secondbox.addWidget(self.keyCombo)
        vbox.addLayout(secondbox)

        #3th QHBoxLayout
        addButton = QPushButton("Add")
        delButton = QPushButton("Del")
        findButton = QPushButton("Find")
        incButton = QPushButton("Inc")
        showButton = QPushButton("show")
        thirdBox = QHBoxLayout()
        thirdBox.addStretch(1)
        thirdBox.addWidget(addButton)
        thirdBox.addWidget(delButton)
        thirdBox.addWidget(findButton)
        thirdBox.addWidget(incButton)
        thirdBox.addWidget(showButton)
        vbox.addLayout(thirdBox)

        #4th QHBoxLayout
        resultLabel = QLabel("Result:")
        fourthbox = QHBoxLayout()
        fourthbox.addWidget(resultLabel)
        vbox.addLayout(fourthbox)

        #5th QHBoxLayout
        self.resultTextEdit = QTextEdit(self)
        fifthbox = QHBoxLayout()
        fifthbox.addWidget(self.resultTextEdit)
        vbox.addLayout(fifthbox)

        #수평정렬
        self.setLayout(vbox)

        #각 버튼이벤트 연결
        addButton.clicked.connect(self.addButtonClicked)
        delButton.clicked.connect(self.delButtonClicked)
        findButton.clicked.connect(self.findButtonClicked)
        incButton.clicked.connect(self.incButtonClicked)
        showButton.clicked.connect(self.showButtonClicked)

        self.show()

    def addButtonClicked(self): #add버튼 코딩
        if self.nameEdit.text() and self.ageEdit.text() and self.scoreEdit:
            self.scoredb.append({'Name': self.nameEdit.text(), 'Age': int(self.ageEdit.text()),'Score': int(self.scoreEdit.text())})

        self.showScoreDB(self.scoredb)

    def delButtonClicked(self): #del버튼 코딩
        # Scoredb에 요소제거
        new_scoredb = []
        for i in self.scoredb:
            if i['Name'] != self.nameEdit.text():
                new_scoredb.append(i)
        self.scoredb = new_scoredb

        self.showScoreDB(self.scoredb)

    def findButtonClicked(self): #find버튼 코딩
        find_scoredb = []
        for i in self.scoredb :
            if i['Name'] == self.nameEdit.text():
                find_scoredb.append(i)
        self.showScoreDB(find_scoredb)

    def incButtonClicked(self): #inc버튼 코딩
        for i in self.scoredb :
            if i['Name'] == self.nameEdit.text():
                if i['Score'] and self.amountEdit.text() :
                    a = i['Score'] + int(self.amountEdit.text())
                    i['Score'] = a

        self.showScoreDB(self.scoredb)

    def showButtonClicked(self): #show버튼 코딩
        if self.keyCombo.currentText() :
            sort_scoredb = sorted(self.scoredb, key=itemgetter(self.keyCombo.currentText()))
        print(sort_scoredb)
        self.showScoreDB(sort_scoredb)

    def closeEvent(self, event): #창을 닫았을 때 저장
        self.writeScoreDB()

    def readScoreDB(self): #데이터 파일 읽음
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)
        except:
            pass
        else:
            pass

        fH.close()

    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def showScoreDB(self, scoredb): #QTextEdit에 결과 화면 나오게하는 코드
        self.resultTextEdit.clear()
        for i in scoredb :
            a = i['Name']
            b = str(i['Age'])
            c = str(i['Score'])
            self.resultTextEdit.append('Age=' + b + '    Name=' + a +'    Score=' + c)


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())
