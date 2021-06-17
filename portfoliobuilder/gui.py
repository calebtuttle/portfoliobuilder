import sys

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QWidget, QFileDialog, QGridLayout)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore

from portfoliobuilder.builder import Portfolio, Basket



class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle('Portfolio Builder')
        self.initUI()

        self.portfolios = []

    def initUI(self):
        self.label = QLabel(self)
        self.label.setText('Portfolios')
        self.label.move(10,10)

        self.btn1 = QPushButton(self)
        self.btn1.setGeometry(10, 10, 150, 35)
        self.btn1.setText('This is a button')
        self.btn1.clicked.connect(self.event_func)

    def display_portfolio_list(self):
        for portfolio in self.portfolios:
            pass

    def event_func(self):
        self.label.setText('Button clicked. Event executed.')


def window_func():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

# window_func()


def create_portfolio():
    basket = Basket(symbols=['GOOG', 'FB', 'AMZN'], weight=1)
    portfolio = Portfolio()
    portfolio.baskets.append(basket)
    portfolio.build_portfolio()



app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Portfolio Builder')
window.setFixedWidth(1000)
# window.setFixedHeight(400)
window.setStyleSheet("background: #ffffff;")

grid = QGridLayout(window)

# Add logo
image = QPixmap("/home/caleb/Desktop/myprograms/portfoliobuilder/Portfolio_Builder.png")
logo = QLabel()
logo.setPixmap(image)

# Add list header
portfolio_list_label = QLabel()
portfolio_list_label.setText('Portfolios')
portfolio_list_label.setStyleSheet("text-decoration: underline;")

# Add list of portfolios
portfolios = ['Portfolio1', 'Portfolio2']
portfolio_labels = []
for p in portfolios:
    p_label = QLabel()
    p_label.setText(p)
    portfolio_labels.append(p_label)

# Add New Portfolio button
new_portfolio_btn = QPushButton()
new_portfolio_btn.setText('New Portfolio')
new_portfolio_btn.clicked.connect(create_portfolio)

# Add widgets to grid
grid.addWidget(logo, 0, 0) # widget, row, col
grid.addWidget(portfolio_list_label, 1, 0)
for i, p in enumerate(portfolio_labels):
    grid.addWidget(p, i+2, 0)
grid.addWidget(new_portfolio_btn, 0, 1)


window.setLayout(grid)

window.show()
sys.exit(app.exec_())

