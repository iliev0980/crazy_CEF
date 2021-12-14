from stocks.models import Stock
import sys
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from multiprocessing import Manager

USER_AGENT = UserAgent()
# CEF daily pricing URL
TICKERS_URL = 'https://www.cefconnect.com/api/v3/DailyPricing?props=Ticker,Name,DistributionRateNAV,LastUpdated,Discount,DistributionRatePrice,ReturnOnNAV,CategoryId,CategoryName,IsManagedDistribution,Price,PriceChange,NAV,NAVPublished,Cusip/&_=1626782460094'
HEADER = {'User-Agent': str(USER_AGENT.random)}

DAILY_CEF_PRICING =  requests.get(TICKERS_URL, headers=HEADER).json()

# Advanced data URL
TICKER_ADVANCED_DETAILS_URL = 'https://www.cefconnect.com/fund/'
# requests header

sys.setrecursionlimit(15000)


def get_target_soup(ticker):
    """ Get lxml data for ticker """
    url = TICKER_ADVANCED_DETAILS_URL + f'{ticker}'
    req = requests.get(url, headers=HEADER)
    return BeautifulSoup(req.content, 'lxml')


class DataCollector:

    def __init__(self, stock: Stock):
        """ Get main page json and all tickers abbreviations upon initialisation """

        self.stock = stock
        self.ticker = self.stock.ticker
        self.main_data = [d for d in DAILY_CEF_PRICING if d['Ticker'] == self.ticker][0]
        print(self.main_data)
        self.soup = get_target_soup(self.stock.ticker)

    def get_data_for_tickers(self):
        """ Main scraping controller """
        mng = Manager()
        self.get_tickers_main_data()
        print('Downloading Data...')

        try:
            resp = get_target_soup(self.stock.ticker)
            self.get_tickers_deep_data(self.stock.ticker, resp)

        except:
            pass

        try:
            self.get_after_calculations()

        except:
            pass


    def get_tickers_main_data(self):
        """ Get data from main page API """

        ticker = self.main_data['Ticker']
        self.stock.ticker = self.main_data['Ticker']
        self.stock.nav = self.main_data['NAV']
        self.stock.price = self.main_data['Price']
        self.stock.price_change = self.main_data.get('PriceChange', pd.NA)
        self.stock.current_discount = self.main_data['Discount']
        self.stock.current_yield = self.main_data['DistributionRatePrice']
        self.stock.fund_sponsor = self.main_data['Name']
        self.stock.category = self.main_data['CategoryName']

    def get_tickers_deep_data(self, ticker, soup):
        """ Deep data scraping controller """

        self.get_nav_change()
        self.get_52_week()
        # self.get_div(ticker, soup)
        self.get_distribution_frequency()
        self.get_distribution_rate()
        self.get_fiscal_year_end()
        self.get_z_score()
        self.get_updated_date()

    def get_after_calculations(self):
        """ Pandas data calculations controller """

        self.get_avg_minus_current_discount()
        self.get_price_change_minus_nav_change()
        self.get_cents_to_avg()
        self.is_updated_today()

    """__________________________________________SCRAPE_ADVANCED_DATA_______________________________________________"""

    def get_nav_change(self):
        """ Sends request to the API and calculating nav change of the last market close """
        nav_url = f'https://www.cefconnect.com/api/v3/pricinghistory/{self.ticker}/1Y'
        req = requests.get(nav_url, headers=HEADER).json()

        try:
            nav_1_days_ago = req['Data']['PriceHistory'][-1].get('NAVData', None)

        except IndexError:
            nav_1_days_ago = None

        try:
            nav_2_days_ago = req['Data']['PriceHistory'][-2].get('NAVData', None)

        except IndexError:
            nav_2_days_ago = None

        if not nav_2_days_ago == None and not nav_1_days_ago == None:
            nav_change = round(nav_1_days_ago - nav_2_days_ago, 2)
            self.stock.nav_change = nav_change

    def get_52_week(self):

        """ scraping for 52 weeks data and excepting in case of missing data """

        target = self.soup.find('table', 'cefconnect-table-1').find_all('td')

        try:
            wk_52_avg = float(target[7].string[:-1])
            self.stock.average_52w = wk_52_avg

        except ValueError:
            pass

        try:
            wk_52_high = float(target[11].string[:-1])
            self.stock.high_52w = wk_52_high

        except ValueError:
            pass

        try:
            wk_52_low = float(target[15].string[:-1])
            self.stock.low_52w = wk_52_low

        except ValueError:
            pass

    def get_distribution_frequency(self):
        """ scraping for 'Distribution frequency' and excepting in case of missing data """

        try:
            distribution_frequency = \
                self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_DistrDetails").find_all('td')[7].string
            self.stock.distribution_frequency = distribution_frequency

        except ValueError:
            pass

    def get_distribution_rate(self):
        """ scraping for distribution rate and excepting in case of missing data """

        try:
            current_yield = float(
                self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_DistrDetails").find_all('td')[3].string[:-1])
            self.stock.current_yield = current_yield

        except ValueError:
            pass

    def get_fiscal_year_end(self):
        """ scraping for fiscal year end value"""

        fiscal_y_end = self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_ucFundBasics_dvFB2").find_all('td')[
            21].string

        self.stock.fiscal_year_end = fiscal_y_end

    def get_z_score(self):
        """ scraping for z scores and excepting in case of missing data """

        try:
            z_score_3_month = float(
                self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_ucPricing_ZScoreGridView").find_all('td')[
                    1].string)

            self.stock.z_score_3 = z_score_3_month

        except ValueError:
            pass

        try:
            z_score_6_month = float(
                self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_ucPricing_ZScoreGridView").find_all('td')[
                    3].string)

            self.stock.z_score_6 = z_score_6_month

        except ValueError:
            pass

        try:
            z_score_1_year = float(
                self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_ucPricing_ZScoreGridView").find_all('td')[
                    5].string)

            self.stock.z_score_12 = z_score_1_year

        except ValueError:
            pass

    def get_updated_date(self):
        """ Get last update date """

        try:
            last_update = self.soup.find(id="ContentPlaceHolder1_cph_main_cph_main_AsOfLabel").string[6:]
            self.stock.last_update = last_update

        except ValueError:
            pass

    """_________________________________________________CALCULATIONS_______________________________________________"""

    def get_avg_minus_current_discount(self):
        """ Calculating 'avg - current' """

        try:
            self.stock.average_minus_current = self.stock.average_52w - self.stock.current_discount

        except:
            pass

    def get_price_change_minus_nav_change(self):
        """ price - nav calculation """

        try:
            self.stock.price_minus_nav = (self.stock.price_change - self.stock.nav_change)

        except:
            pass

    def get_cents_to_avg(self):
        """ Calculating 'cents to average' """

        try:
            self.stock.cents_to_average = (self.stock.average_minus_current * self.stock.nav) / 100

        except:
            pass

    def is_updated_today(self):

        """ Calculate if ticker is updated today """

        try:
            self.stock.is_updated = self.compare_date(self.stock.last_update)
            print('is updated')

        except:
            pass

    def compare_date(self, last_update):

        """ calculate if data for ticker is updated today """

        try:
            current_member = pd.Timestamp(last_update)
            timestamp_now = pd.Timestamp(datetime.datetime.now())

        except:
            return False

        if timestamp_now.weekday() == 0:  # ToDo condition if it is first day of the new year
            if timestamp_now.day == 1:
                return current_member.day == (datetime.datetime.now() - datetime.timedelta(
                    days=3)).day and current_member.month == timestamp_now.month - 1 and current_member.year == timestamp_now.year

            return current_member.day == timestamp_now.day - 3 and current_member.month == timestamp_now.month and current_member.year == timestamp_now.year

        else:
            if timestamp_now.day == 1:
                return current_member.day == (datetime.datetime.now() - datetime.timedelta(
                    days=1)).day and current_member.month == timestamp_now.month - 1 and current_member.year == timestamp_now.year

            return current_member.day == timestamp_now.day - 1 and current_member.month == timestamp_now.month and current_member.year == timestamp_now.year

    def save(self):
        print('saved')
        self.stock.save(force_update=True)


# def daily_update():

# for ticker, data in main_data.items:
for stock in Stock.objects.filter(is_updated=False):
    target_stock = DataCollector(stock)
    target_stock.get_data_for_tickers()
    target_stock.save()

