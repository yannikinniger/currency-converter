import datetime
from urllib.request import urlretrieve
import zipfile
from bisect import bisect_right


class CurrencyDataProvider:

    def __init__(self):
        file = self.download_unzip()
        self.data = self.extract_exchange_rates(file)

    def get_latest_rate(self, currency):
        """
        Gets the latest available exchange rate for the passed currency to EUR
        :param currency: Code for the currency
        :return: Exchange rate to EUR as a float
        """
        rates = self.data[currency]
        print(next(iter(rates)))
        print(rates[next(iter(rates))])
        return rates[next(iter(rates))]

    def get_rates_for_period(self, currency, start, end):
        """
        Gets the exchange rate for one currency in between two dates
        :param currency: Code for the currency
        :param start: Start of the desired time period
        :param end: End of the desired time period
        :return: Array of the available exchange rates in between the passed dates
        """
        available_dates = sorted(self.data[currency].keys())
        left_index = self.get_closest_date(available_dates, start)
        right_index = self.get_closest_date(available_dates, end)
        dates_with_rates = available_dates[left_index:right_index + 1]  # add 1 to include the end too
        selected_rates = []
        for date in dates_with_rates:
            selected_rates.append(self.data[currency][date])
        return selected_rates

    @staticmethod
    def get_closest_date(available_dates, date):
        """
        Checks if the passed date is in the list of desired dates and returns the closest one if the desired is
        not available
        :param available_dates: List of available dates
        :param date: Desired date
        :return: Desired date or closest date after the desired date
        """
        try:
            return available_dates.index(date)
        except ValueError:
            return bisect_right(available_dates, date)

    @staticmethod
    def extract_exchange_rates(file):
        """
        Extracts all the exchange rates from the file passed and associates them with the currency code
        :param file: Downloaded file from the url https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip
        :return: Dictionary of currency codes which holds another dictionary with the exchange rates sorted by date
        """
        data = {}
        file_lines = file.split('\n')
        header_line = file_lines[0].split(',')
        for currency_code in header_line[1:]:
            data[currency_code] = {}

        rate_lines = file_lines[1:]
        for rate_line in rate_lines:
            splitted_line = rate_line.split(',')
            date = datetime.datetime.strptime(splitted_line[0], '%Y-%m-%d').date()
            rates = splitted_line[1:]
            for currency, rate in zip(data.keys(), rates):
                if rate != 'N/A' and len(rate) != 0:
                    data[currency][date] = float(rate)
        return data

    @staticmethod
    def download_unzip():
        """
        Downloads a zip file containing currency conversion rates and extracts it
        :return: String of the extracted file
        """
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'
        file, _ = urlretrieve(url)
        zip_file_object = zipfile.ZipFile(file, 'r')
        first_file = zip_file_object.namelist()[0]
        file = zip_file_object.open(first_file)
        return file.read().decode('utf-8')
