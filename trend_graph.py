import pyqtgraph as pg


class TrendGraph(pg.PlotWidget):

    def __init__(self, currency_1, code_currency_1, currency_2, code_currency_2, conversion):
        super().__init__()
        max_rate = next(iter(max(currency_1, currency_2)), 0) * 1.2
        days = max(len(currency_1), len(currency_2), len(conversion)) - 1
        self.setup_graph(max_rate, days)
        self.plot_graph(currency_1, code_currency_1, currency_2, code_currency_2, conversion)

    def setup_graph(self, max_rate, days):
        """
        Sets up the descriptions of the graph
        :param max_rate: Maximum value in the data
        :param days: Number of days on which data is available
        """
        self.showGrid(x=True, y=True)
        self.addLegend()
        self.setLabel('left', 'Rate')
        self.setLabel('bottom', 'Days')
        self.setXRange(0, days)
        self.setYRange(0, max_rate)

    def plot_graph(self, currency_1, code_currency_1, currency_2, code_currency_2, conversion):
        """
        Plots the lines for the data which was passed in the arguments
        :param currency_1: Array of exchange rates
        :param code_currency_1: Name of a currency used for the legend
        :param currency_2: Array of exchange rates
        :param code_currency_2: Name of a currency used for the legend
        :param conversion: Array of exchange rates
        """
        self.plot(range(0, len(currency_1)), currency_1, pen='y', symbol='x', symbolPen='y', symbolBrush=0.2,
                  name='{}/EUR'.format(code_currency_1))
        self.plot(range(0, len(currency_2)), currency_2, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2,
                  name='{}/EUR'.format(code_currency_2))
        self.plot(range(0, len(conversion)), conversion, pen='g', symbol='+', symbolPen='g', symbolBrush=0.2,
                  name='{}/{}'.format(code_currency_1, code_currency_2))
