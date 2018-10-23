from PyQt5.QtWidgets import *
from data_provider.currency_data_provider import CurrencyDataProvider
from trend_graph import TrendGraph


class Converter(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_provider = CurrencyDataProvider()

        self.from_label = QLabel('From Currency:')
        self.from_currency = QComboBox()
        self.to_label = QLabel('To Currency:')
        self.to_currency = QComboBox()
        self.amount_label = QLabel('Amount:')
        self.amount = QDoubleSpinBox()
        self.converted_label = QLabel('Result based on most recent rate:')
        self.amount_converted = QLabel('1.00')
        self.from_date = QCalendarWidget()
        self.to_date = QCalendarWidget()

        self.initialize_parts()
        self.layout = self.layout_parts()
        self.setup_bindings()
        self.update_graph()
        self.setLayout(self.layout)

    def initialize_parts(self):
        """
        Configures the Widgets which need special configuration
        """
        self.from_currency.addItems(self.data_provider.data.keys())
        self.to_currency.addItems(self.data_provider.data.keys())
        self.amount.setRange(0.01, 10_000_000.00)
        self.amount.setValue(1.00)

    def layout_parts(self):
        """
        Adds all the parts to the grid and returns it
        :return: Grid populated with all initialized Widgets
        """
        grid = QGridLayout()
        grid.addWidget(self.from_label, 0, 0)
        grid.addWidget(self.from_currency, 0, 1)
        grid.addWidget(self.amount_label, 0, 2)
        grid.addWidget(self.amount, 0, 3)
        grid.addWidget(self.to_label, 1, 0)
        grid.addWidget(self.to_currency, 1, 1)
        grid.addWidget(self.converted_label, 1, 2)
        grid.addWidget(self.amount_converted, 1, 3)
        grid.addWidget(self.from_date, 3, 0, 1, 2)
        grid.addWidget(self.to_date, 3, 2, 1, 2)
        return grid

    def setup_bindings(self):
        """
        Sets up the bindings to process changes on the UI
        """
        self.from_currency.currentIndexChanged.connect(self.update_ui)
        self.to_currency.currentIndexChanged.connect(self.update_ui)
        self.amount.valueChanged.connect(self.update_ui)
        self.from_date.clicked.connect(self.update_graph)
        self.to_date.clicked.connect(self.update_graph)

    def update_ui(self):
        """
        Gets all possible input values, calculates the new conversion and updates it on the UI
        """
        from_currency_code = self.from_currency.currentText()
        to_currency_code = self.to_currency.currentText()
        from_rate = self.data_provider.get_latest_rate(from_currency_code)
        to_rate = self.data_provider.get_latest_rate(to_currency_code)
        amount = float(self.amount.value())
        conversion = amount / from_rate * to_rate
        self.amount_converted.setText("%.06f" % conversion)
        self.update_graph()

    def update_graph(self):
        """
        Gets the input data from the UI and updates the graph according to the new data
        """
        start_date = self.from_date.selectedDate().toPyDate()
        end_date = self.to_date.selectedDate().toPyDate()

        from_currency_code = self.from_currency.currentText()
        from_currency_rates = self.data_provider.get_rates_for_period(from_currency_code, start_date, end_date)
        to_currency_code = self.to_currency.currentText()
        to_currency_rates = self.data_provider.get_rates_for_period(to_currency_code, start_date, end_date)

        conversion = []
        for currency_1, currency_2 in zip(from_currency_rates, to_currency_rates):
            conversion.append(self.convert(currency_1, currency_2, 1))
        graph = TrendGraph(from_currency_rates, from_currency_code, to_currency_rates, to_currency_code, conversion)
        self.layout.addWidget(graph, 4, 0, 1, 4)

    @staticmethod
    def convert(from_rate, to_rate, amount):
        """
        Calculates the a specified amount to another currency
        :param from_rate: Exchange rate for the initial currency to EUR
        :param to_rate: Exchange rate for the target currency to EUR
        :param amount: Amount in the initial currency to be converted
        :return: Converted amount
        """
        return amount / from_rate * to_rate

