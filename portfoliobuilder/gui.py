import sys

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QWidget, QFileDialog, QGridLayout, QStackedLayout,
                            QRadioButton, QButtonGroup, QSpinBox, QLineEdit,
                            QMessageBox, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore

from portfoliobuilder.builder import Portfolio, Basket


# TODO: Clean up code. Organize into classes and functions.
# TODO: Implement navigation between frames.
# TODO: Bring portfoliobuilder.builder functionality into the GUI.




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




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Builder")
        self.setFixedWidth(1000)

        self.initUI()
        
    def initUI(self):
        self.box_layout = QVBoxLayout()
        self.setLayout(self.box_layout)

        # Header layout
        self.header_layout = QVBoxLayout()
        portfolio_builder_header = self.portfolio_builder_header() # TODO: Turn portfolio_builder_header into a property
        self.header_layout.addWidget(portfolio_builder_header)
        self.frame_header = self.frame_header_func()
        self.header_layout.addWidget(self.frame_header)

        self.stacked_layout = QStackedLayout()
        # self.setLayout(self.stacked_layout)

        self.home_frame = HomeFrame()
        self.home_frame.new_portfolio_button.clicked.connect(self.switch_to_new_portfolio_frame)
        self.stacked_layout.addWidget(self.home_frame)

        self.new_portfolio_frame = NewPortfolioFrame()
        self.new_portfolio_frame.new_basket_button.clicked.connect(self.switch_to_new_basket_frame)
        self.stacked_layout.addWidget(self.new_portfolio_frame)

        self.new_basket_frame = NewBasketFrame()
        self.stacked_layout.addWidget(self.new_basket_frame)

        # TODO: Put the below line in a method and change setCurrentIndex
        # to a variable 
        self.stacked_layout.setCurrentIndex(0)

        self.box_layout.addLayout(self.header_layout)
        self.box_layout.addLayout(self.stacked_layout)

    def portfolio_builder_header(self):
        header = QLabel('Portfolio Builder')
        header.setStyleSheet(
            """
            font-family: Arial;
            font-size: 40px;
            color: '#001040';
            """
        )
        return header

    def frame_header_func(self):
        header = QLabel('Home')
        header.setStyleSheet(
            """
            font-family: Arial;
            font-size: 30px;
            color: '#001040';
            """
        )
        return header

    def switch_to_new_portfolio_frame(self):
        self.frame_header.setText('Create New Portfolio')
        self.stacked_layout.setCurrentIndex(1)

    def switch_to_new_basket_frame(self):
        self.frame_header.setText('Create New Basket')
        self.stacked_layout.setCurrentIndex(2)



class HomeFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.portfolios = []

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.portfolio_list_header = self.portfolio_list_header_func()
        self.portfolio_labels = self.portfolio_labels_func()
        self.new_portfolio_button = self.new_portfolio_button_func()

        # Add widgets to grid
        self.grid.addWidget(self.portfolio_list_header, 0, 0)
        for i, p in enumerate(self.portfolio_labels):
            self.grid.addWidget(p, i+1, 0)
        self.grid.addWidget(self.new_portfolio_button, 0, 1)

    def portfolio_list_header_func(self):
        ''' Return a QLabel '''
        portfolio_list_label = QLabel('Portfolios')
        portfolio_list_label.setAlignment(Qt.AlignLeft)
        portfolio_list_label.setStyleSheet("""
                text-decoration: underline;
                font-size: 25px;
                font-family: Arial;
                color: '#001040';
                """)
        return portfolio_list_label

    def portfolio_labels_func(self):
        ''' Return a list of QLabels '''
        portfolio_labels = []
        for p in self.portfolios:
            p_label = QLabel()
            p_label.setStyleSheet("""
                font-size: 15px;
                font-family: Arial;
                """)
            p_label.setText(p.name)
            portfolio_labels.append(p_label)
        return portfolio_labels

    def new_portfolio_button_func(self):
        ''' Return a QPushButton '''
        new_portfolio_btn = QPushButton()
        new_portfolio_btn.setText('New Portfolio')
        new_portfolio_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        new_portfolio_btn.setStyleSheet(
            """
            *{
                border: 4px solid '#001040';
                border-radius: 15px;
                font-family: Arial;
                font-size: 25px;
                font-family: Arial;
                color: '#001040';
            }
            *:hover{
                background: '#00107f';
                color: '#ffffff';
            }
            """
        )
        return new_portfolio_btn


class NewPortfolioFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.baskets = []

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.basket_list_header = self.baskets_list_header_func()
        self.basket_labels = self.basket_labels_func()
        self.new_basket_button = self.new_basket_button_func()

        # Add widgets to grid
        self.grid.addWidget(self.basket_list_header, 0, 0)
        for i, p in enumerate(self.basket_labels):
            self.grid.addWidget(p, i+1, 0)
        self.grid.addWidget(self.new_basket_button, 0, 1)

    def baskets_list_header_func(self):
        basket_list_label = QLabel('Baskets')
        basket_list_label.setStyleSheet("""
                text-decoration: underline;
                font-size: 25px;
                font-family: Arial;
                color: '#001040';
                """)
        return basket_list_label

    def basket_labels_func(self):
        basket_labels = []
        for b in self.baskets:
            b_label = QLabel()
            b_label.setText(b.name)
            basket_labels.append(b_label)
        return basket_labels

    def new_basket_button_func(self):
        new_basket_button = QPushButton('New Basket')
        new_basket_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        new_basket_button.setStyleSheet(
            """
            *{
                border: 4px solid '#00107f';
                border-radius: 15px;
                font-family: Arial;
                font-size: 25px;
                color: '#001040';
                padding: 15px 0px;
            }
            *:hover{
                background: '#00107f';
                color: '#ffffff';
            }
            """
        )
        return new_basket_button


class NewBasketFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.new_basket_header = self.new_basket_header_func()

        # Collect stock symbols from user
        self.add_stock_label = self.add_stock_label_func()
        self.new_stocks_label = self.new_stocks_label_func()
        self.symbol_input = QLineEdit()
        self.symbols = []
        self.symbol_input.returnPressed.connect(self.add_symbol_to_new_stocks_label)
        
        weighting_method_label = QLabel('Weighting Method: ')
        weighting_method_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        weighting_method_btn_grp = QButtonGroup()
        equal_wm_btn = QRadioButton('Equal')
        equal_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        market_cap_wm_btn = QRadioButton('Market Cap')
        market_cap_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        value_wm_btn = QRadioButton('Value')
        value_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        weighting_method_btn_grp.addButton(equal_wm_btn)
        weighting_method_btn_grp.addButton(market_cap_wm_btn)
        weighting_method_btn_grp.addButton(value_wm_btn)

        weight_label = QLabel('Basket weight: ')
        weight_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        weight = QSpinBox()
        weight.setMinimum(1)
        weight.setMaximum(100)

        self.confirm_basket_message_box = self.confirm_basket_message_box_func()
        self.create_basket_button = self.create_basket_button()

        self.grid.addWidget(self.new_basket_header, 0, 0, 1, 4)
        self.grid.addWidget(self.add_stock_label, 1, 0)
        self.grid.addWidget(self.symbol_input, 1, 1)
        self.grid.addWidget(self.new_stocks_label, 1, 2)
        self.grid.addWidget(weighting_method_label, 2, 0)
        self.grid.addWidget(equal_wm_btn, 2, 1)
        self.grid.addWidget(market_cap_wm_btn, 2, 2)
        self.grid.addWidget(value_wm_btn, 2, 3)
        self.grid.addWidget(weight_label, 3, 0)
        self.grid.addWidget(weight, 3, 1)
        self.grid.addWidget(self.create_basket_button, 4, 0, 1, 4)

    def new_basket_header_func(self):
        new_basket_label = QLabel('Create New Basket')
        new_basket_label.setAlignment(QtCore.Qt.AlignCenter) 
        new_basket_label.setStyleSheet(
            """
            text-decoration: underline;
            font-size: 30px;
            font-family: Arial;
            color: '#001040';
            """
        )
        return new_basket_label

    def add_stock_label_func(self):
        add_stock = QLabel('Add Stock: ')
        add_stock.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        return add_stock

    def new_stocks_label_func(self):
        new_stocks = QLabel('Stocks added:\n')
        new_stocks.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        return new_stocks

    def add_symbol_to_new_stocks_label(self):
        self.symbols.append(self.symbol_input.text())
        new_stocks_str = self.new_stocks_label.text() + f'{self.symbols[-1]}\n'
        self.new_stocks_label.setText(new_stocks_str)
        self.symbol_input.setText('')

    def confirm_basket_message_box_func(self):
        baskets_message_box = QMessageBox()
        baskets_message_box.setText('Are you finished creating this basket?')
        baskets_message_box.setWindowTitle('Create Basket')
        baskets_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # baskets_message_box.buttonClicked.connect(some_function)
        return baskets_message_box

    def create_basket_button(self):
        def display_confirm_dialog():
            yes_or_no = self.confirm_basket_message_box.exec()
            if yes_or_no == QMessageBox.Yes:
                print('OK clicked')
        create_basket_btn = QPushButton('Create Basket')
        create_basket_btn.setStyleSheet(
            """
            *{
                border: 4px solid '#00107f';
                border-radius: 15px; 
                font-family: Arial;
                font-size: 25px;
                color: '#001040';
                padding: 15px 0px;
            }
            *:hover{
                background: '#00107f';
                color: '#ffffff';
            }
            """
        )
        create_basket_btn.clicked.connect(display_confirm_dialog)
        return create_basket_btn

    



def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

run()








# app = QApplication(sys.argv)

# window = QWidget()
# window.setWindowTitle('Portfolio Builder')
# window.setFixedWidth(1000)
# # window.setFixedHeight(400)
# window.setStyleSheet("background: #ffffff;")

# grid = QGridLayout(window)

# # Add logo
# image = QPixmap("/home/caleb/Desktop/myprograms/portfoliobuilder/Portfolio_Builder.png")
# logo = QLabel()
# logo.setPixmap(image)
# # logo.setAlignment(QtCore.Qt.AlignCenter) # Center logo
# logo.setStyleSheet("margin: 10px;")


# def home_frame():
#     # Add portfolios list header
#     portfolio_list_label = QLabel()
#     portfolio_list_label.setText('Portfolios')
#     portfolio_list_label.setStyleSheet("text-decoration: underline;")

#     # Add list of portfolios
#     portfolios = ['Portfolio1', 'Portfolio2']
#     portfolio_labels = []
#     for p in portfolios:
#         p_label = QLabel()
#         p_label.setText(p)
#         portfolio_labels.append(p_label)

#     # Add New Portfolio button
#     new_portfolio_btn = QPushButton()
#     new_portfolio_btn.setText('New Portfolio')
#     new_portfolio_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
#     new_portfolio_btn.setStyleSheet(
#         """
#         *{
#             border: 4px solid '#00107f';
#             border-radius: 15px; 
#             font-size: 25px;
#             color: '#0010ff;
#             padding: 15px 0px;
#         }
#         *:hover{
#             background: '#00107f';
#             color: '#ffffff';
#         }

#         """
#     )
#     new_portfolio_btn.clicked.connect(create_portfolio)

#     # Add widgets to grid
#     grid.addWidget(logo, 0, 0) # widget, row, col
#     grid.addWidget(portfolio_list_label, 1, 0)
#     for i, p in enumerate(portfolio_labels):
#         grid.addWidget(p, i+2, 0)
#     grid.addWidget(new_portfolio_btn, 0, 1)


# def new_portfolio_frame():
#     # Add frame header
#     new_portfolio_label = QLabel()
#     new_portfolio_label.setText('Create New Portfolio')
#     new_portfolio_label.setAlignment(QtCore.Qt.AlignCenter) 
#     new_portfolio_label.setStyleSheet(
#         """
#         text-decoration: underline;
#         font-size: 30px;
#         """
#     )

#     # Add baskets list header
#     basket_list_label = QLabel()
#     basket_list_label.setText('Baskets')
#     basket_list_label.setStyleSheet("text-decoration: underline;")

#     # Add list of baskets
#     baskets = []
#     basket_labels = []
#     for b in baskets:
#         b_label = QLabel()
#         b_label.setText(b)
#         basket_labels.append(b_label)

#     # Add New Basket button
#     new_basket_btn = QPushButton()
#     new_basket_btn.setText('New Basket')
#     new_basket_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
#     new_basket_btn.setStyleSheet(
#         """
#         *{
#             border: 4px solid '#00107f';
#             border-radius: 15px; 
#             font-size: 25px;
#             color: '#0010ff;
#             padding: 15px 0px;
#         }
#         *:hover{
#             background: '#00107f';
#             color: '#ffffff';
#         }

#         """
#     )
#     new_basket_btn.clicked.connect(create_basket)

#     # Add widgets to grid
#     grid.addWidget(new_portfolio_label, 0, 0, 1, 2) # widget, row, col
#     grid.addWidget(basket_list_label, 1, 0)
#     for i, p in enumerate(basket_labels):
#         grid.addWidget(p, i+2, 0)
#     grid.addWidget(new_basket_btn, 1, 1)


# def new_basket_frame():
#     '''
#     Frame in which a user creates a new Basket.
#     '''
#     # Add frame header
#     new_basket_label = QLabel()
#     new_basket_label.setText('Create New Basket')
#     new_basket_label.setAlignment(QtCore.Qt.AlignCenter) 
#     new_basket_label.setStyleSheet(
#         """
#         text-decoration: underline;
#         font-size: 30px;
#         """
#     )

#     # Take stocks input
    # stock_label = QLabel()
    # stock_label.setText('Add Stock: ')
    # new_stocks_label = QLabel('Stocks added:\n')
    # symbol_input = QLineEdit()
    # symbols = []
    # def add_symbol():
    #     symbols.append(symbol_input.text())
    #     print(f'symbols: {symbols}')
    #     new_stocks_str = new_stocks_label.text() + f'{symbols[-1]}\n'
    #     new_stocks_label.setText(new_stocks_str)
    #     symbol_input.setText('')
    # symbol_input.returnPressed.connect(add_symbol)

#     # Weighting method
    # weighting_method_label = QLabel('Weighting Method: ')
    # weighting_method_btn_grp = QButtonGroup()
    # equal_wm_btn = QRadioButton('Equal')
    # weighting_method_btn_grp.addButton(equal_wm_btn)
    # market_cap_wm_btn = QRadioButton('Market Cap')
    # weighting_method_btn_grp.addButton(market_cap_wm_btn)
    # value_wm_btn = QRadioButton('Value')
    # weighting_method_btn_grp.addButton(value_wm_btn)

#     # Basket weight
    # weight_label = QLabel('Basket weight: ')
    # weight = QSpinBox()
    # weight.setMinimum(1)
    # weight.setMaximum(100)

    # Confirm button
    # def display_confirm_dialog():
    #     yes_or_no = baskets_message_box.exec()
    #     if yes_or_no == QMessageBox.Yes:
    #         print('OK clicked')
    # create_basket_btn = QPushButton('Create Basket')
    # create_basket_btn.setStyleSheet(
    #     """
    #     margin: 10px;
    #     height: 35px;
    #     width: 50px;
    #     """
    # )
    # create_basket_btn.clicked.connect(display_confirm_dialog)

#     # Confirm pop-up
    # baskets_message_box = QMessageBox()
    # baskets_message_box.setText('Are you finished creating this basket?')
    # baskets_message_box.setWindowTitle('Create Basket')
    # baskets_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    # # baskets_message_box.buttonClicked.connect(some_function)

    # # Add widgets to grid
    # grid.addWidget(new_basket_label, 0, 0, 1, 4) # widget, row, col, occupy_num_rows, occupy_num_cols
    # grid.addWidget(stock_label, 1, 0)
    # grid.addWidget(symbol_input, 1, 1)
    # grid.addWidget(new_stocks_label, 1, 2)
    # grid.addWidget(weighting_method_label, 2, 0)
    # grid.addWidget(equal_wm_btn, 2, 1)
    # grid.addWidget(market_cap_wm_btn, 2, 2)
    # grid.addWidget(value_wm_btn, 2, 3)
    # grid.addWidget(weight_label, 3, 0)
    # grid.addWidget(weight, 3, 1)
    # grid.addWidget(create_basket_btn, 4, 0, 1, 4)



# home_frame()
# # new_portfolio_frame()
# # new_basket_frame()


# window.setLayout(grid)

# window.show()
# sys.exit(app.exec_())

