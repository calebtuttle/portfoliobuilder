import sys

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout, 
                            QVBoxLayout, QStackedLayout, QLabel, QLineEdit, 
                            QPushButton,  QRadioButton, QButtonGroup, QSpinBox, 
                            QMessageBox)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from portfoliobuilder.builder import Portfolio, Basket


# TODO: Bring portfoliobuilder.builder functionality into the GUI.
# TODO: Use a database to keep track of and access the different 
#       portfolios (completed ones, in progress ones)


def create_portfolio():
    basket = Basket(symbols=['GOOG', 'FB', 'AMZN'], weight=1)
    portfolio = Portfolio()
    portfolio.baskets.append(basket)
    portfolio.build_portfolio()






class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Builder")
        self.setFixedWidth(1000)

        self.portfolios = []

        self.initUI()
        
    def initUI(self):
        self.box_layout = QVBoxLayout()
        self.setLayout(self.box_layout)

        # Header layout
        self.header_layout = QVBoxLayout()
        self.init_portfolio_builder_header()
        self.header_layout.addWidget(self.portfolio_builder_header)
        self.init_frame_header()
        self.header_layout.addWidget(self.frame_header)

        self.stacked_layout = QStackedLayout()

        self.home_frame = HomeFrame()
        self.home_frame.new_portfolio_button.clicked.connect(self.switch_to_new_portfolio_frame)
        self.stacked_layout.addWidget(self.home_frame)

        self.new_portfolio_frame = NewPortfolioFrame()
        self.new_portfolio_frame.new_basket_button.clicked.connect(self.switch_to_new_basket_frame)
        self.stacked_layout.addWidget(self.new_portfolio_frame)

        self.new_basket_frame = NewBasketFrame()
        self.new_basket_frame.basket_created.connect(self.on_basket_created)
        self.stacked_layout.addWidget(self.new_basket_frame)

        # TODO: Put the below line in a method and change setCurrentIndex
        # to a variable 
        self.stacked_layout.setCurrentIndex(0)

        self.box_layout.addLayout(self.header_layout)
        self.box_layout.addLayout(self.stacked_layout)

    def init_portfolio_builder_header(self):
        self.portfolio_builder_header = QLabel('Portfolio Builder')
        self.portfolio_builder_header.setStyleSheet(
            """
            font-family: Arial;
            font-size: 40px;
            color: '#001040';
            """
        )

    def init_frame_header(self):
        self.frame_header = QLabel('Home')
        self.frame_header.setStyleSheet(
            """
            font-family: Arial;
            font-size: 30px;
            color: '#001040';
            """
        )

    def switch_to_new_portfolio_frame(self):
        from_home_frame = self.stacked_layout.currentIndex() == 0
        from_new_basket_frame = self.stacked_layout.currentIndex() == 2
        if from_home_frame:
            name = f'Portfolio{len(self.portfolios)}'
            new_portfolio = Portfolio(name=name)
            self.new_portfolio_frame.portfolio = new_portfolio
        elif from_new_basket_frame:
            pass
        self.frame_header.setText('Create New Portfolio')
        self.stacked_layout.setCurrentIndex(1)

    def switch_to_new_basket_frame(self):
        portfolio = self.new_portfolio_frame.portfolio
        self.new_basket_frame.portfolio = portfolio
        self.frame_header.setText('Create New Basket')
        self.stacked_layout.setCurrentIndex(2)

    @pyqtSlot(bool)
    def on_basket_created(self, value):
        if value:
            new_basket = self.new_basket_frame.basket
            self.new_portfolio_frame.portfolio.baskets.append(new_basket)
            # self.portfolios.append(self.new_portfolio_frame.portfolio)
            self.new_portfolio_frame.init_basket_labels()  # TODO: Find a better way to do this. Find a way to just update basket labels
            self.switch_to_new_portfolio_frame()



class HomeFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.portfolios = []

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.init_portfolio_list_header()
        self.init_portfolio_labels()
        self.init_new_portfolio_button()

        # Add widgets to grid
        self.grid.addWidget(self.portfolio_list_header, 0, 0)
        for i, p in enumerate(self.portfolio_labels):
            self.grid.addWidget(p, i+1, 0)
        self.grid.addWidget(self.new_portfolio_button, 0, 1)

    def init_portfolio_list_header(self):
        self.portfolio_list_header = QLabel('Portfolios')
        self.portfolio_list_header.setAlignment(Qt.AlignLeft)
        self.portfolio_list_header.setStyleSheet("""
                text-decoration: underline;
                font-size: 25px;
                font-family: Arial;
                color: '#001040';
                """)

    def init_portfolio_labels(self):
        self.portfolio_labels = []
        for p in self.portfolios:
            p_label = QLabel()
            p_label.setStyleSheet("""
                font-size: 15px;
                font-family: Arial;
                """)
            p_label.setText(p.name)
            self.portfolio_labels.append(p_label)

    def init_new_portfolio_button(self):
        self.new_portfolio_button = QPushButton()
        self.new_portfolio_button.setText('New Portfolio')
        self.new_portfolio_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_portfolio_button.setStyleSheet(
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


class NewPortfolioFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.portfolio = None

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.init_baskets_header()
        self.init_basket_labels()
        self.init_new_basket_button()

        # Add widgets to grid
        self.grid.addWidget(self.baskets_header, 0, 0)
        for i, p in enumerate(self.basket_labels):
            self.grid.addWidget(p, i+1, 0)
        self.grid.addWidget(self.new_basket_button, 0, 1)

    def init_baskets_header(self):
        self.baskets_header = QLabel('Baskets')
        self.baskets_header.setStyleSheet("""
                text-decoration: underline;
                font-size: 25px;
                font-family: Arial;
                color: '#001040';
                """)

    def init_basket_labels(self):
        self.basket_labels = []
        print(f'Printing new_portfolio_frame.portfolio.. {self.portfolio}') # TODO: Delete this line
        if self.portfolio:                                                  # TODO: Delete this line
            print(f'Printing portfolio.baskets... {self.portfolio.baskets}') # TODO: Delete this line
        if self.portfolio:
            for b in self.portfolio.baskets:
                b_label = QLabel()
                b_label.setText(b.name)
                self.basket_labels.append(b_label)

    def init_new_basket_button(self):
        self.new_basket_button = QPushButton('New Basket')
        self.new_basket_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_basket_button.setStyleSheet(
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


class NewBasketFrame(QWidget):

    basket_created = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

        self.portfolio = None
        self.basket = None

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.init_new_basket_header()

        # Collect stock symbols from user
        self.init_add_stock_label()
        self.init_new_stocks_label()
        self.symbol_input = QLineEdit()
        self.symbols = []
        self.symbol_input.returnPressed.connect(self.add_symbol_to_new_stocks_label)
        
        self.init_weighting_method_label()
        self.init_weighting_method_buttons()

        self.init_weight_label()
        self.init_weight()

        self.init_confirm_basket_message_box()
        self.init_create_basket_button()

        self.grid.addWidget(self.new_basket_header, 0, 0, 1, 4)
        self.grid.addWidget(self.add_stock_label, 1, 0)
        self.grid.addWidget(self.symbol_input, 1, 1)
        self.grid.addWidget(self.new_stocks_label, 1, 2)
        self.grid.addWidget(self.weighting_method_label, 2, 0)
        self.grid.addWidget(self.equal_wm_btn, 2, 1)
        self.grid.addWidget(self.market_cap_wm_btn, 2, 2)
        self.grid.addWidget(self.value_wm_btn, 2, 3)
        self.grid.addWidget(self.weight_label, 3, 0)
        self.grid.addWidget(self.weight, 3, 1)
        self.grid.addWidget(self.create_basket_button, 4, 0, 1, 4)

    def init_new_basket_header(self):
        self.new_basket_header = QLabel('Create New Basket')
        self.new_basket_header.setAlignment(Qt.AlignCenter) 
        self.new_basket_header.setStyleSheet(
            """
            text-decoration: underline;
            font-size: 30px;
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_add_stock_label(self):
        self.add_stock_label = QLabel('Add Stock: ')
        self.add_stock_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_new_stocks_label(self):
        self.new_stocks_label = QLabel('Stocks added:\n')
        self.new_stocks_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_weighting_method_label(self):
        self.weighting_method_label = QLabel('Weighting Method: ')
        self.weighting_method_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_weighting_method_buttons(self):
        self.weighting_method_btn_grp = QButtonGroup()
        self.equal_wm_btn = QRadioButton('Equal')
        self.equal_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        self.market_cap_wm_btn = QRadioButton('Market Cap')
        self.market_cap_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        self.value_wm_btn = QRadioButton('Value')
        self.value_wm_btn.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        self.weighting_method_btn_grp.addButton(self.equal_wm_btn)
        self.weighting_method_btn_grp.addButton(self.market_cap_wm_btn)
        self.weighting_method_btn_grp.addButton(self.value_wm_btn)

    def init_weight_label(self):
        self.weight_label = QLabel('Basket weight: ')
        self.weight_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_weight(self):
        self.weight = QSpinBox()
        self.weight.setMinimum(1)
        self.weight.setMaximum(100)

    def add_symbol_to_new_stocks_label(self):
        self.symbols.append(self.symbol_input.text())
        new_stocks_str = self.new_stocks_label.text() + f'{self.symbols[-1]}\n'
        self.new_stocks_label.setText(new_stocks_str)
        self.symbol_input.setText('')

    def init_confirm_basket_message_box(self):
        self.confirm_basket_message_box = QMessageBox()
        self.confirm_basket_message_box.setText('Are you finished creating this basket?')
        self.confirm_basket_message_box.setWindowTitle('Create Basket')
        self.confirm_basket_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def init_create_basket_button(self):
        def display_confirm_dialog():
            yes_or_no = self.confirm_basket_message_box.exec()
            if yes_or_no == QMessageBox.Yes:
                symbols = self.new_stocks_label.text().split('\n')[1:-1]
                weighting_method = self.get_weighting_method_str()
                if self.portfolio:
                    name = f'Basket{len(self.portfolio.baskets)}'
                    self.create_basket(symbols, weighting_method, self.weight.value(), name)
                self.basket_created.emit(True)
        self.create_basket_button = QPushButton('Create Basket')
        self.create_basket_button.setStyleSheet(
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
        self.create_basket_button.clicked.connect(display_confirm_dialog)

    def get_weighting_method_str(self):
        if self.equal_wm_btn.isChecked():
            weighting_method = 'equal'
        elif self.market_cap_wm_btn.isChecked():
            weighting_method = 'market_cap'
        elif self.value_wm_btn.isChecked():
            weighting_method = 'value'
        return weighting_method

    def create_basket(self, symbols, weighting_method, weight, name='Basket'):
        basket = Basket(symbols, weighting_method, weight, name)
        print(f'new basket: {basket}')
        self.basket = basket
        return basket
    



def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

run()


