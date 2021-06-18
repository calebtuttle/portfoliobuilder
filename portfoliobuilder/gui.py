import sys

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QWidget, QFileDialog, QGridLayout,
                            QRadioButton, QButtonGroup, QSpinBox, QLineEdit,
                            QDialogButtonBox)
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

def create_basket(portfolio, symbols):
    if not portfolio:
        return None
    if not symbols:
        symbols = ['GOOG', 'FB', 'AMZN']
    basket = Basket(symbols, weight=1)
    portfolio.baskets.append(basket)
    return basket



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
# logo.setAlignment(QtCore.Qt.AlignCenter) # Center logo
logo.setStyleSheet("margin: 10px;")


def home_frame():
    # Add portfolios list header
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
    new_portfolio_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    new_portfolio_btn.setStyleSheet(
        """
        *{
            border: 4px solid '#00107f';
            border-radius: 15px; 
            font-size: 25px;
            color: '#0010ff;
            padding: 15px 0px;
        }
        *:hover{
            background: '#00107f';
            color: '#ffffff';
        }

        """
    )
    new_portfolio_btn.clicked.connect(create_portfolio)

    # Add widgets to grid
    grid.addWidget(logo, 0, 0) # widget, row, col
    grid.addWidget(portfolio_list_label, 1, 0)
    for i, p in enumerate(portfolio_labels):
        grid.addWidget(p, i+2, 0)
    grid.addWidget(new_portfolio_btn, 0, 1)


def new_portfolio_frame():
    # Add frame header
    new_portfolio_label = QLabel()
    new_portfolio_label.setText('Create New Portfolio')
    new_portfolio_label.setAlignment(QtCore.Qt.AlignCenter) 
    new_portfolio_label.setStyleSheet(
        """
        text-decoration: underline;
        font-size: 30px;
        """
    )

    # Add baskets list header
    basket_list_label = QLabel()
    basket_list_label.setText('Baskets')
    basket_list_label.setStyleSheet("text-decoration: underline;")

    # Add list of baskets
    baskets = []
    basket_labels = []
    for b in baskets:
        b_label = QLabel()
        b_label.setText(b)
        basket_labels.append(b_label)

    # Add New Basket button
    new_basket_btn = QPushButton()
    new_basket_btn.setText('New Basket')
    new_basket_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    new_basket_btn.setStyleSheet(
        """
        *{
            border: 4px solid '#00107f';
            border-radius: 15px; 
            font-size: 25px;
            color: '#0010ff;
            padding: 15px 0px;
        }
        *:hover{
            background: '#00107f';
            color: '#ffffff';
        }

        """
    )
    new_basket_btn.clicked.connect(create_basket)

    # Add widgets to grid
    grid.addWidget(new_portfolio_label, 0, 0, 1, 2) # widget, row, col
    grid.addWidget(basket_list_label, 1, 0)
    for i, p in enumerate(basket_labels):
        grid.addWidget(p, i+2, 0)
    grid.addWidget(new_basket_btn, 1, 1)


def new_basket_frame():
    '''
    Frame in which a user creates a new Basket.
    '''
    # Add frame header
    new_basket_label = QLabel()
    new_basket_label.setText('Create New Basket')
    new_basket_label.setAlignment(QtCore.Qt.AlignCenter) 
    new_basket_label.setStyleSheet(
        """
        text-decoration: underline;
        font-size: 30px;
        """
    )

    # Take stocks input
    stock_label = QLabel()
    stock_label.setText('Add Stock: ')
    new_stocks_label = QLabel('Stocks added:\n')
    symbol_input = QLineEdit()
    symbols = []
    def add_symbol():
        symbols.append(symbol_input.text())
        print(f'symbols: {symbols}')
        new_stocks_str = new_stocks_label.text() + f'{symbols[-1]}\n'
        new_stocks_label.setText(new_stocks_str)
        symbol_input.setText('')
    symbol_input.returnPressed.connect(add_symbol)

    # Weighting method
    weighting_method_label = QLabel('Weighting Method: ')
    weighting_method_btn_grp = QButtonGroup()
    equal_wm_btn = QRadioButton('Equal')
    weighting_method_btn_grp.addButton(equal_wm_btn)
    market_cap_wm_btn = QRadioButton('Market Cap')
    weighting_method_btn_grp.addButton(market_cap_wm_btn)
    value_wm_btn = QRadioButton('Value')
    weighting_method_btn_grp.addButton(value_wm_btn)

    # Basket weight
    weight_label = QLabel('Basket weight: ')
    weight = QSpinBox()
    weight.setMinimum(1)
    weight.setMaximum(100)

    # Confirm button
    def display_confirm_dialog():
        confirm_new_basket_dlg.exec()
    create_basket_btn = QPushButton('Create Basket')
    create_basket_btn.setStyleSheet(
        """
        margin: 10px;
        height: 35px;
        width: 50px;
        """
    )
    create_basket_btn.clicked.connect(display_confirm_dialog)

    # Confirm pop-up
    def print_yes_message():
        print('Yes')
    def print_no_message():
        print('No')
    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    confirm_new_basket_dlg = QDialogButtonBox(QBtn)
    confirm_new_basket_dlg.accepted.connect(print_yes_message)
    confirm_new_basket_dlg.rejected.connect(print_no_message)

    # Add widgets to grid
    grid.addWidget(new_basket_label, 0, 0, 1, 4) # widget, row, col, occupy_num_rows, occupy_num_cols
    grid.addWidget(stock_label, 1, 0)
    grid.addWidget(symbol_input, 1, 1)
    grid.addWidget(new_stocks_label, 1, 2)
    grid.addWidget(weighting_method_label, 2, 0)
    grid.addWidget(equal_wm_btn, 2, 1)
    grid.addWidget(market_cap_wm_btn, 2, 2)
    grid.addWidget(value_wm_btn, 2, 3)
    grid.addWidget(weight_label, 3, 0)
    grid.addWidget(weight, 3, 1)
    grid.addWidget(create_basket_btn, 4, 0, 1, 4)
    grid.addWidget(confirm_new_basket_dlg)



# home_frame()
# new_portfolio_frame()
new_basket_frame()

window.setLayout(grid)

window.show()
sys.exit(app.exec_())

