from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout
from keypad import *
import calcFunctions

class Button(QToolButton):
    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Calculator(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        #Display Window
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        # Button Creation and Placement
        numLayout = QGridLayout()
        opLayout = QGridLayout()
        constLayout = QGridLayout()
        funcLayout = QGridLayout()

        buttonGroups = {
            'num': {'buttons': numPadList, 'layout': numLayout, 'columns': 3},
            'op': {'buttons': operatorList, 'layout': opLayout, 'columns': 2},
            'constants': {'buttons': constantList, 'layout': constLayout, 'columns': 1},
            'functions': {'buttons': functionList, 'layout': funcLayout, 'columns': 1},
        }

        for label in buttonGroups.keys():
            r = 0;
            c = 0
            buttonPad = buttonGroups[label]
            for btnText in buttonPad['buttons']:
                button = Button(btnText, self.buttonClicked)
                buttonPad['layout'].addWidget(button, r, c)
                c += 1
                if c >= buttonPad['columns']:
                    c = 0;
                    r += 1

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 2)
        mainLayout.addLayout(numLayout, 1, 0)
        mainLayout.addLayout(opLayout, 1, 1)
        mainLayout.addLayout(constLayout, 2, 0)
        mainLayout.addLayout(funcLayout, 2, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("My Calculator")

        self.setLayout(mainLayout)
        self.setWindowTitle("My Calculator")

        self.number = ["0","1","2","3","4","5","6","7","8","9","(",")"]
        self.operator = ["+","-","*","/"]
        self.errorMessage = ["0으로 나눌 수 없습니다.", "0으로 시작하지 마십시오.", "괄호를 다시 확인해주세요."]

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if self.display.text() in self.errorMessage :
            self.display.setText('0')

        #숫자 넣어주기
        if key in self.number :
            if self.display.text() == "0" or not self.display.text() in self.number:
                self.display.setText('') #오류처리1 - 처음에 0이 온다면 오류 -> 빈 문자열로 만듦
                self.display.setText(self.display.text()+key)
            else:
                self.display.setText(self.display.text()+key)

        #연산자 넣어주기
        elif key in self.operator:
            if not self.display.text() == '0' : #오류처리2 - 처음에 연산자 오지 못함
                if self.display.text()[-1] in self.operator : #오류처리3 - 연산자는 2개가 올 수 없음. 마지막이 연산자면 입력한 것으로 변환
                    self.display.setText(self.display.text()[:-1]+key)

                else:
                    self.display.setText(self.display.text() + key)

        #소수점 넣어주기
        elif key == '.':
            if self.display.text()[-1] == '.': #오류처리4 - 소수점이 2개면 오류
                pass
            else:
                self.display.setText(self.display.text() + key)

        #결과조회하기
        elif key == '=':
            try :
                if self.display.text()[-1] in self.operator : #오류처리5 - 연산자로 끝났을 경우 오류. >아무것도 실행하지 않게 함
                    pass

                else :
                    self.display.setText(self.checkZeroNumber(self.display.text())) #오류처리6, 오류처리8

            except ZeroDivisionError as e : #오류처리7 - ZeroDivisonError가 났을 경우 에러메시지를 text로 set함
                self.display.setText(self.errorMessage[0])

        elif key in constantList:
            self.display.setText(self.display.text() + constantList[key])

        elif key in functionList:
            num = self.display.text()
            value = calcFunctions.operator(num, functionList[key])
            self.display.setText(str(value))

        #초기화
        else :
            self.display.setText('0')

    #오류처리6, 오류처리8
    def checkZeroNumber(self, text):
        #오류처리8 - 괄호의 갯수 확인 및 괄호 정확한 순서 확인 > 아닐경우 에러메시지 남김
        left = []
        check = True

        for i in self.display.text():
            if i == "(":
                left.append(1)
            elif i == ")":
                if len(left) == 0:
                    check = False
                    break
                else:
                    left.pop()

        if len(left) != 0 :
            check = False

        if check:
            for i in range(len(text)): #오류처리6 - 연산자 뒤에 0으로 시작하는 숫자 있으면 에러메시지 남김
                if text[i] in self.operator and text[i+1] == "0" and (i+1) != len(text)-1:
                    if text[i+1] == "." :
                        pass
                        if text[i+2] != 0 :
                            return self.errorMessage[1]
            return str(eval(text))

        else:
            return self.errorMessage[2]


if __name__  == '__main__':

    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())