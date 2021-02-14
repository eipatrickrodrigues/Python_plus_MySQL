import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QLabel, QLineEdit
from PyQt5 import QtGui

class Window (QMainWindow):
    def __init__(self):
        super().__init__()

        self.topo = 100
        self.esquerda = 100
        self.largura = 800
        self.altura = 600
        self.titulo = 'Janela'

        self.text_box = QLineEdit(self)
        self.text_box.move(25,20)
        self.text_box.resize(250,30)

        self.buttom_1 = QPushButton('Botão 1',self)
        self.buttom_1.move(100,250)
        self.buttom_1.resize(200,100)
        self.buttom_1.setStyleSheet('QPushButton{background-color:#0fB328}')
        self.buttom_1.clicked.connect(self.Clique)

        self.buttom_box = QPushButton('Text',self)
        self.buttom_box.move(350,250)
        self.buttom_box.resize(200,100)
        self.buttom_box.setStyleSheet('QPushButton{background-color:#ff0933}')
        self.buttom_box.clicked.connect(self.Show_Text)

        self.Label_box = QLabel(self)
        self.Label_box.move(100,400)
        self.Label_box.setStyleSheet('QLabel{font-size:20px}')
        self.Label_box.setText('Digitou: ')

        self.Label_1 = QLabel(self)
        self.Label_1.setText('Patrick Rodrigues')
        self.Label_1.move(100,20)
        self.Label_1.resize(300,300)
        self.Label_1.setStyleSheet('QLabel{font-size:30px;color:red}')

        self.car = QLabel(self)
        self.car.move(150,50)
        self.car.resize(500,200)
        self.car.setPixmap(QtGui.QPixmap('car.png'))

    def Clique(self):
        print('O Botão foi clicado')
        self.Label_1.setText('Clicou.')
        self.Label_1.setStyleSheet('QLabel{font-size:30px;color:pink}')

    def Show_Text(self):
        content = self.Label_box.text()
        self.Label_box.setText('Digitou: ' + content)

    def CarregarJanela(self):
        self.setGeometry(self.esquerda,self.topo,self.largura,self.altura)
        self.setWindowTitle(self.titulo)
        self.show()

        # Carregar a janela é o último passo.
        self.CarregarJanela()



application = QApplication(sys.argv)
w = Window()
sys.exit(application.exec_())