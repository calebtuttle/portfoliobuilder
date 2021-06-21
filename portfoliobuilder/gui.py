import sys

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout, 
                            QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, 
                            QLineEdit, QPushButton,  QRadioButton, QButtonGroup, 
                            QSpinBox, QScrollArea, QMessageBox, QInputDialog)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from portfoliobuilder.builder import Portfolio, Basket
from portfoliobuilder.utils import copy_portfolio


# TODO: Bring portfoliobuilder.builder functionality into the GUI.
# TODO: Use a database to keep track of and access the different 
#       portfolios (completed ones, in progress ones)
# TODO: In NewPortfolioFrame, display the weight
#       of each basket, add the ability to edit a basket.
# TODO: In HomeFrame, add the ability to edit a portfolio, the
#       ability to build (execute) a portfolio.


_LIST_ELEMENT_STYLE_SHEET = """font-size: 20px;
                            font-family: Arial;
                            color: '#001040';
                            """
_BLUE_BUTTON_STYLE_SHEET = """*{
                    border: 4px solid '#001040';
                    border-radius: 15px;
                    font-family: Arial;
                    font-size: 22px;
                    color: '#001040';
                    padding: 5px;
                    }
                    *:hover{
                        background: '#001040';
                        color: '#ffffff';
                    }
                    """
_RED_BUTTON_STYLE_SHEET = """*{
                    border: 4px solid '#500007';
                    border-radius: 15px;
                    font-family: Arial;
                    font-size: 22px;
                    color: '#500007';
                    padding: 5px;
                    }
                    *:hover{
                        background: '#500007';
                        color: '#ffffff';
                    }
                    """



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Builder")
        self.setFixedWidth(700)

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
        self.new_portfolio_frame.portfolio_created.connect(self.on_portfolio_created)
        self.new_portfolio_frame.portfolio_canceled.connect(self.on_portfolio_canceled)
        self.stacked_layout.addWidget(self.new_portfolio_frame)

        self.new_basket_frame = NewBasketFrame()
        self.new_basket_frame.basket_created.connect(self.on_basket_created)
        self.new_basket_frame.basket_canceled.connect(self.on_basket_canceled)
        self.stacked_layout.addWidget(self.new_basket_frame)

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
            border-bottom: 4px solid '#001040';
            border-radius: 0px;
            font-family: Arial;
            font-size: 30px;
            color: '#001040';
            """
        )

    def switch_to_home_frame(self):
        self.frame_header.setText('Home')
        self.stacked_layout.setCurrentIndex(0)

    def switch_to_new_portfolio_frame(self):
        from_home_frame = self.stacked_layout.currentIndex() == 0
        from_new_basket_frame = self.stacked_layout.currentIndex() == 2
        if from_home_frame:
            new_portfolio = Portfolio(name='Portfolio Name')
            self.new_portfolio_frame.portfolio = new_portfolio
        elif from_new_basket_frame:
            # TODO
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
            self.new_portfolio_frame.update_basket_labels()
            self.new_portfolio_frame.update_unallocated_label()
            self.switch_to_new_portfolio_frame()

    @pyqtSlot(bool)
    def on_basket_canceled(self, value):
        if value:
            self.new_basket_frame.basket = None
            self.switch_to_new_portfolio_frame()

    @pyqtSlot(bool)
    def on_portfolio_created(self, value):
        if value:
            new_portfolio = copy_portfolio(self.new_portfolio_frame.portfolio)
            self.home_frame.portfolios.append(new_portfolio)
            print(f'New portfolio: {new_portfolio.name}')
            # self.portfolios.append(self.new_portfolio_frame.portfolio)
            self.home_frame.update_portfolio_labels()
            self.new_portfolio_frame.portfolio = None
            self.new_portfolio_frame.update_basket_labels()
            self.switch_to_home_frame()

    @pyqtSlot(bool)
    def on_portfolio_canceled(self, value):
        if value:
            self.new_portfolio_frame.portfolio = None
            self.home_frame.update_portfolio_labels()
            self.new_portfolio_frame.update_basket_labels()
            self.switch_to_home_frame()


class HomeFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.portfolios = []

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.portfolio_box_layout = QVBoxLayout()

        self.init_portfolio_list_header()
        self.init_portfolio_labels()
        self.init_new_portfolio_button()

        # Add widgets to grid
        self.grid.addWidget(self.portfolio_list_header, 0, 0)
        for p in self.portfolio_labels:
            self.portfolio_box_layout.addWidget(p)
        self.grid.addLayout(self.portfolio_box_layout, 1, 0)
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
        if self.portfolios:
            for p in self.portfolios:
                p_label = QLabel()
                p_label.setStyleSheet(_LIST_ELEMENT_STYLE_SHEET)
                p_label.setText(p.name)
                self.portfolio_labels.append(p_label)
        else:
            no_portfolios_label = QLabel('No portfolios to show...')
            style = _LIST_ELEMENT_STYLE_SHEET + '\nfont-size: 17px;'
            no_portfolios_label.setStyleSheet(style)
            self.portfolio_labels.append(no_portfolios_label)

    def update_portfolio_labels(self):
        if self.portfolio_labels:
            # Remove portfolio labels
            for p_label in self.portfolio_labels:
                self.portfolio_box_layout.removeWidget(p_label)

        # Add portfolio labels
        self.portfolio_labels = []
        for i, p in enumerate(self.portfolios):
            p_label = QLabel(p.name)
            p_label.setStyleSheet(_LIST_ELEMENT_STYLE_SHEET)
            self.portfolio_labels.append(p_label)
            self.portfolio_box_layout.insertWidget(i, p_label)

    def init_new_portfolio_button(self):
        self.new_portfolio_button = QPushButton('New Portfolio')
        self.new_portfolio_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_portfolio_button.setStyleSheet(_BLUE_BUTTON_STYLE_SHEET)


class NewPortfolioFrame(QWidget):

    portfolio_created = pyqtSignal(bool)
    portfolio_canceled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.portfolio = None

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.basket_box_layout = QVBoxLayout()

        self.init_name_label()
        self.init_edit_name_button()

        self.init_unallocated_label()

        self.init_baskets_header()
        self.init_basket_labels()

        self.init_new_basket_button()

        self.init_cancel_portfolio_message_box()
        self.init_cancel_portfolio_button()

        self.init_confirm_portfolio_message_box()
        self.init_create_portfolio_button()

        # Add widgets to grid
        self.grid.addWidget(self.name_label, 0, 0)
        self.grid.addWidget(self.edit_name_button, 0, 1, 1, 1)
        self.grid.addWidget(self.unallocated_label, 1, 1)
        self.grid.addWidget(self.baskets_header, 1, 0)
        for basket_label in enumerate(self.basket_labels):
            self.basket_box_layout.addWidget(basket_label)
        self.grid.addLayout(self.basket_box_layout, 2, 0, 1, 2)
        self.grid.addWidget(self.new_basket_button, 3, 0)
        self.grid.addWidget(self.cancel_portfolio_button, 4, 0, 1, 1)
        self.grid.addWidget(self.create_portfolio_button, 4, 1, 1, 3)

    def init_name_label(self):
        self.name_label = QLabel('"Portfolio Name"')
        self.name_label.setStyleSheet("""
                font-size: 22px;
                font-family: Arial;
                color: '#001040';
                """
        )
        if self.portfolio:
            self.portfolio.name = self.name_label.text()

    def init_edit_name_button(self):
        def get_name():
            name, ok, = QInputDialog.getText(self, 'Edit Portfolio Name', 'New portfolio name: ')
            if ok and name:
                self.name_label.setText(f'"{name}"')
                self.portfolio.name = name
        self.edit_name_button = QPushButton('Edit Portfolio Name')
        self.edit_name_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_name_button.setStyleSheet(_BLUE_BUTTON_STYLE_SHEET)
        self.edit_name_button.clicked.connect(get_name)

    def init_unallocated_label(self):
        self.unallocated_label = QLabel('100% of this portfolio is unallocated')
        style = _LIST_ELEMENT_STYLE_SHEET + '\nfont-size: 17px;'
        self.unallocated_label.setStyleSheet(style)
        if self.portfolio:
            unallocated = 100 - sum([b.weight for b in self.portfolio.baskets])
            unallocated_str = f'{unallocated}% of this portfolio is unallocated'
            self.unallocated_label.setText(unallocated_str)

    def update_unallocated_label(self):
        unallocated = 100 - sum([b.weight for b in self.portfolio.baskets])
        unallocated_str = f'{unallocated}% of this portfolio is unallocated'
        self.unallocated_label.setText(unallocated_str)

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
        if self.portfolio:
            for b in self.portfolio.baskets:
                b_label = QLabel(b.name)
                b_label.setStyleSheet(_LIST_ELEMENT_STYLE_SHEET)
                self.basket_labels.append(b_label)

    def update_basket_labels(self):
        # Remove basket labels
        for b_label in self.basket_labels:
            self.basket_box_layout.removeWidget(b_label)

        self.basket_labels = []
        
        if self.portfolio:
            # Add labels for current baskets
            for i, b in enumerate(self.portfolio.baskets):
                b_label = QLabel(f'{b.name}  |  {b.weight}%')
                b_label.setStyleSheet(_LIST_ELEMENT_STYLE_SHEET)
                self.basket_labels.append(b_label)
                self.basket_box_layout.insertWidget(i, b_label)

    def init_new_basket_button(self):
        self.new_basket_button = QPushButton('New Basket')
        self.new_basket_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_basket_button.setStyleSheet(_BLUE_BUTTON_STYLE_SHEET)

    def init_cancel_portfolio_message_box(self):
        self.cancel_portfolio_message_box = QMessageBox()
        self.cancel_portfolio_message_box.setText('Are you sure you want to cancel this portfolio?')
        self.cancel_portfolio_message_box.setWindowTitle('Cancel Portfolio')
        self.cancel_portfolio_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def init_cancel_portfolio_button(self):
        def display_confirm_dialog():
            yes_or_no = self.cancel_portfolio_message_box.exec()
            if yes_or_no == QMessageBox.Yes:
                self.portfolio_canceled.emit(True)
        self.cancel_portfolio_button = QPushButton('Cancel Portfolio')
        self.cancel_portfolio_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel_portfolio_button.setStyleSheet(_RED_BUTTON_STYLE_SHEET)
        self.cancel_portfolio_button.clicked.connect(display_confirm_dialog)

    def init_confirm_portfolio_message_box(self):
        self.confirm_portfolio_message_box = QMessageBox()
        self.confirm_portfolio_message_box.setText('Are you finished creating this portfolio?')
        self.confirm_portfolio_message_box.setWindowTitle('Create Portfolio')
        self.confirm_portfolio_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def init_create_portfolio_button(self):
        def display_confirm_dialog():
            yes_or_no = self.confirm_portfolio_message_box.exec()
            if yes_or_no == QMessageBox.Yes:
                self.portfolio_created.emit(True)
        self.create_portfolio_button = QPushButton('Create Portfolio')
        self.create_portfolio_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.create_portfolio_button.setStyleSheet(_BLUE_BUTTON_STYLE_SHEET)
        self.create_portfolio_button.clicked.connect(display_confirm_dialog)


class NewBasketFrame(QWidget):

    basket_created = pyqtSignal(bool)
    basket_canceled = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

        self.portfolio = None
        self.basket = None

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.init_new_basket_header()

        self.init_add_stock_label()
        self.init_new_stocks_label()
        self.init_new_stocks_scroll_area()
        self.init_add_stock_field()
        
        self.init_weighting_method_label()
        self.init_weighting_method_buttons()

        self.init_weight_label()
        self.init_weight()

        self.init_name_label()
        self.init_name_field()

        self.init_cancel_basket_message_box()
        self.init_cancel_basket_button()

        self.init_confirm_basket_message_box()
        self.init_create_basket_button()

        self.grid.addWidget(self.new_basket_header, 0, 0, 1, 4)
        self.grid.addWidget(self.add_stock_label, 1, 0)
        self.grid.addWidget(self.add_stock_field, 1, 1)
        # self.grid.addWidget(self.new_stocks_label, 1, 2)
        self.grid.addWidget(self.new_stocks_scroll_area, 1, 2)
        self.grid.addWidget(self.weighting_method_label, 2, 0)
        self.grid.addWidget(self.equal_wm_btn, 2, 1)
        self.grid.addWidget(self.market_cap_wm_btn, 2, 2)
        self.grid.addWidget(self.value_wm_btn, 2, 3)
        self.grid.addWidget(self.weight_label, 3, 0)
        self.grid.addWidget(self.weight, 3, 1)
        self.grid.addWidget(self.name_label, 4, 0)
        self.grid.addWidget(self.name_field, 4, 1)
        self.grid.addWidget(self.cancel_basket_button, 5, 0, 1, 1)
        self.grid.addWidget(self.create_basket_button, 5, 1, 1, 3)

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

    def init_add_stock_field(self):
        self.add_stock_field = QLineEdit()
        self.add_stock_field.setPlaceholderText('AAPL')
        self.symbols = []
        self.add_stock_field.returnPressed.connect(self.add_symbol_to_new_stocks_label)

    def init_new_stocks_label(self):
        # self.new_stocks_label = QLabel('Stocks added:\n') # TODO: Make a new label for 'Stocks Added:'
        self.new_stocks_label = QLabel('')
        self.new_stocks_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )
        hbox_layout = QHBoxLayout()
        self.new_stocks_label.setLayout(hbox_layout)

    def init_new_stocks_scroll_area(self):
        self.new_stocks_scroll_area = QScrollArea()
        self.new_stocks_scroll_area.setFixedHeight(100)
        self.new_stocks_scroll_area.setFixedWidth(175)
        self.new_stocks_scroll_area.setWidget(self.new_stocks_label)
        # self.new_stocks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.new_stocks_scroll_area.show()

    def init_weighting_method_label(self):
        self.weighting_method_label = QLabel('Weighting Method: ')
        self.weighting_method_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_weighting_method_buttons(self):
        style_sheet = """font-family: Arial;
                    color: '#001040';
                    """
        self.weighting_method_btn_grp = QButtonGroup()
        self.equal_wm_btn = QRadioButton('Equal')
        self.equal_wm_btn.setStyleSheet(style_sheet)
        self.market_cap_wm_btn = QRadioButton('Market Cap')
        self.market_cap_wm_btn.setStyleSheet(style_sheet)
        self.value_wm_btn = QRadioButton('Value')
        self.value_wm_btn.setStyleSheet(style_sheet)
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
        self.weight.setSuffix('%')

    def add_symbol_to_new_stocks_label(self):
        self.symbols.append(self.add_stock_field.text())
        new_stocks_str = self.new_stocks_label.text() + f'{self.symbols[-1]}\n'
        self.new_stocks_label.setText(new_stocks_str)
        self.add_stock_field.setText('')

    def init_name_label(self):
        self.name_label = QLabel('Basket name: ')
        self.name_label.setStyleSheet("""
            font-family: Arial;
            color: '#001040';
            """
        )

    def init_name_field(self):
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText('S&P500 Basket')

    def init_cancel_basket_message_box(self):
        self.cancel_basket_message_box = QMessageBox()
        self.cancel_basket_message_box.setText('Are you sure you want to cancel this basket?')
        self.cancel_basket_message_box.setWindowTitle('Cancel Basket')
        self.cancel_basket_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def init_cancel_basket_button(self):
        def display_confirm_dialog():
            yes_or_no = self.cancel_basket_message_box.exec()
            if yes_or_no == QMessageBox.Yes:
                self.reset_labels_fields_and_buttons()
                self.basket_canceled.emit(True)
        self.cancel_basket_button = QPushButton('Cancel Basket')
        self.cancel_basket_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel_basket_button.setStyleSheet(_RED_BUTTON_STYLE_SHEET)
        self.cancel_basket_button.clicked.connect(display_confirm_dialog)

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
                name = self.name_field.text()
                self.create_basket(symbols, weighting_method, self.weight.value(), name)
                self.reset_labels_fields_and_buttons()
                self.basket_created.emit(True)
        self.create_basket_button = QPushButton('Create Basket')
        self.create_basket_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.create_basket_button.setStyleSheet(_BLUE_BUTTON_STYLE_SHEET)
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
        print(f'New basket: {basket}')  # TODO: Delete this line
        self.basket = basket
        return basket
    
    def reset_labels_fields_and_buttons(self):
        self.new_stocks_label.setText('Stocks added:\n')
        self.add_stock_field.setText('')

        # Weighting method buttons
        self.weighting_method_btn_grp.setExclusive(False)
        for wm_btn in self.weighting_method_btn_grp.buttons():
            if wm_btn.isChecked():
                wm_btn.setChecked(False)
        self.weighting_method_btn_grp.setExclusive(True)

        self.weight.setValue(1)
        self.name_field.setText('')


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

run()


